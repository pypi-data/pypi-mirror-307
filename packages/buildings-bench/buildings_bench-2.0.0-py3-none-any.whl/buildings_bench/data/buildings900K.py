import torch
import numpy as np
from pathlib import Path
import pyarrow.parquet as pq
import buildings_bench.transforms as transforms
from buildings_bench.transforms import BoxCoxTransform, StandardScalerTransform
import pandas as pd
from typing import List
from buildings_bench.utils import get_puma_county_lookup_table
import datetime


class Buildings900K(torch.utils.data.Dataset):
    r"""This is an indexed dataset for the Buildings-900K dataset.
    It uses an index file to quickly load a sub-sequence from a time series in a multi-building
    Parquet file. The index file is a tab separated file with the following columns:

    0. Building-type-and-year (e.g., comstock_tmy3_release_1)
    1. Census region (e.g., by_puma_midwest)
    2. PUMA ID
    3. Building ID
    4. Hour of year pointer (e.g., 0070)

    The sequence pointer is used to extract the slice
    [pointer - context length : pointer + pred length] for a given building ID.
    
    The time series are not stored chronologically and must be sorted by timestamp after loading.

    Each dataloader worker has its own file pointer to the index file. This is to avoid
    weird multiprocessing errors from sharing a file pointer. We 'seek' to the correct
    line in the index file for random access.
    """
    def __init__(self, 
                dataset_path: Path,
                index_file: str,
                context_len: int = 168,
                pred_len: int = 24,
                apply_scaler_transform: str = '',
                scaler_transform_path: Path = None,
                weather_inputs: List[str] = None):
        """
        Args:
            dataset_path (Path): Path to the pretraining dataset.
            index_file (str): Name of the index file
            context_len (int, optional): Length of the context. Defaults to 168. 
                The index file has to be generated with the same context length.
            pred_len (int, optional): Length of the prediction horizon. Defaults to 24.
                The index file has to be generated with the same pred length.
            apply_scaler_transform (str, optional): Apply a scaler transform to the load. Defaults to ''.
            scaler_transform_path (Path, optional): Path to the scaler transform. Defaults to None.
            weather_inputs (List[str]): list of weather features to use. Default: None.
        """
        self.dataset_path = dataset_path / 'Buildings-900K' / 'end-use-load-profiles-for-us-building-stock' / '2021'
        self.metadata_path = dataset_path / 'metadata'
        self.context_len = context_len
        self.pred_len = pred_len
        self.building_type_and_year = ['comstock_tmy3_release_1',
                                       'resstock_tmy3_release_1',
                                       'comstock_amy2018_release_1',
                                       'resstock_amy2018_release_1']
        self.census_regions = ['by_puma_midwest', 'by_puma_south', 'by_puma_northeast', 'by_puma_west']
        self.index_file = self.metadata_path / index_file
        self.index_fp = None
        self.__read_index_file(self.index_file)
        self.weather_inputs = weather_inputs
        self.time_transform = transforms.TimestampTransform()
        self.spatial_transform = transforms.LatLonTransform()
        self.apply_scaler_transform = apply_scaler_transform
        if self.apply_scaler_transform == 'boxcox':
            self.load_transform = BoxCoxTransform()
            self.load_transform.load(scaler_transform_path)
        elif self.apply_scaler_transform == 'standard':
            self.load_transform = StandardScalerTransform()
            self.load_transform.load(scaler_transform_path)

        if self.weather_inputs: # build a puma-county lookup table
            self.lookup_df = get_puma_county_lookup_table(self.metadata_path)
            self.weather_transforms = []           
            for col in self.weather_inputs:
                self.weather_transforms += [ StandardScalerTransform() ]
                self.weather_transforms[-1].load(self.metadata_path / 'transforms' / 'weather' / col)

    def init_fp(self):
        """Each worker needs to open its own file pointer to avoid 
        weird multiprocessing errors from sharing a file pointer.

        This is not called in the main process.
        This is called in the DataLoader worker_init_fn.
        The file is opened in binary mode which lets us disable buffering.
        """
        self.index_fp = open(self.index_file, 'rb', buffering=0)
        self.index_fp.seek(0)

    def __read_index_file(self, index_file: Path) -> None:
        """Extract metadata from index file.
        """
        # Fast solution to get the number of time series in index file
        # https://pynative.com/python-count-number-of-lines-in-file/
        def _count_generator(reader):
            b = reader(1024 * 1024)
            while b:
                yield b
                b = reader(1024 * 1024)

        with open(index_file, 'rb') as fp:
            c_generator = _count_generator(fp.raw.read)
            # count each \n
            self.num_time_series = sum(buffer.count(b'\n') for buffer in c_generator)
        
        # Count the number of chars per line
        with open(index_file, 'rb', buffering=0) as fp:
            first_line = fp.readline()
            self.chunk_size = len(first_line)
        
        #print(f'Counted {self.num_time_series} indices in index file.')

    def __del__(self):
        if self.index_fp:
            self.index_fp.close()

    def __len__(self):
        return self.num_time_series

    def __getitem__(self, idx):
        # Open file pointer if not already open
        if not self.index_fp:
           self.index_fp = open(self.index_file, 'rb', buffering=0)
           self.index_fp.seek(0)

        # Get the index of the time series
        self.index_fp.seek(idx * self.chunk_size, 0)
        ts_idx = self.index_fp.read(self.chunk_size).decode('utf-8')

        # Parse the index
        ts_idx = ts_idx.strip('\n').split('\t')

        # strip loading zeros
        seq_ptr = ts_idx[-1]
        seq_ptr = int(seq_ptr.lstrip('0')) if seq_ptr != '0000' else 0
        # Building ID
        bldg_id = ts_idx[3].lstrip('0')

        # Select timestamp and building column
        df = pq.read_table(str(self.dataset_path / self.building_type_and_year[int(ts_idx[0])]
                           / 'timeseries_individual_buildings' / self.census_regions[int(ts_idx[1])]
                           / 'upgrade=0' / f'puma={ts_idx[2]}'), columns=['timestamp', bldg_id])

        # Order by timestamp
        df = df.to_pandas().sort_values(by='timestamp')
        # Slice each column from seq_ptr-context_len : seq_ptr + pred_len
        time_features = self.time_transform.transform(df['timestamp'].iloc[seq_ptr-self.context_len : seq_ptr+self.pred_len ])
        # Running faiss on CPU is  slower than on GPU, so we quantize loads later after data loading.
        load_features = df[bldg_id].iloc[seq_ptr-self.context_len : seq_ptr+self.pred_len ].values.astype(np.float32)  # (context_len+pred_len,)
        # For BoxCox transform
        if self.apply_scaler_transform != '':
            load_features = self.load_transform.transform(load_features)
        latlon_features = self.spatial_transform.transform(ts_idx[2]).repeat(self.context_len + self.pred_len, axis=0) 
        
        # residential = 0 and commercial = 1
        building_features = np.ones((self.context_len + self.pred_len,1), dtype=np.int32) * int(int(ts_idx[0]) % 2 == 0)

        sample = {
            'latitude': latlon_features[:, 0][...,None],
            'longitude': latlon_features[:, 1][...,None],
            'day_of_year': time_features[:, 0][...,None],
            'day_of_week': time_features[:, 1][...,None],
            'hour_of_day': time_features[:, 2][...,None],
            'building_type': building_features,
            'load': load_features[...,None]
        }

        if self.weather_inputs is None:
            return sample
        else:
            ## Append weather features

            # get county ID
            county = self.lookup_df.loc[ts_idx[2]]['nhgis_2010_county_gisjoin']
            # load corresponding weather files
            weather_df = pd.read_csv(self.dataset_path / self.building_type_and_year[int(ts_idx[0])] / 'weather' / f'{county}.csv')

            # This is assuming that the file always starts from January 1st (ignoring the year)
            assert datetime.datetime.strptime(weather_df['date_time'].iloc[0], '%Y-%m-%d %H:%M:%S').strftime('%m-%d') == '01-01',\
                "The weather file does not start from Jan 1st"
            
            weather_df.columns = ['timestamp'] + self.weather_inputs 
            weather_df = weather_df[['timestamp'] + self.weather_inputs]
            #weather_df = weather_df.iloc[:-1] # remove last hour to align with load data


            # TODO: At test time, I think we are removing a row from the DF. Make sure these are the same.
            # add -1 because the file starts from 01:00:00
            weather_df = weather_df.iloc[seq_ptr-self.context_len-1 : seq_ptr+self.pred_len -1] 
            
            # convert temperature to fahrenheit (note: keep celsius for now)
            # weather_df['temperature'] = weather_df['temperature'].apply(lambda x: x * 1.8 + 32) 

            # transform
            for idx,col in enumerate(weather_df.columns[1:]):
                ## WARNING: CONVERTS TO TORCH FROM NUMPY AUTOMATICALLY
                sample.update({col : self.weather_transforms[idx].transform(
                    weather_df[col].to_numpy())[0][...,None] })

            return sample
    
    def collate_fn(self):
        """Returns a function taking only one argument (the list of items to be batched).
        """
        def _collate(samples):
            batch = {
                'latitude': torch.stack([torch.from_numpy(s['latitude']) for s in samples]).float(),
                'longitude': torch.stack([torch.from_numpy(s['longitude']) for s in samples]).float(),
                'building_type': torch.stack([torch.from_numpy(s['building_type']) for s in samples]).long(),
                'day_of_year': torch.stack([torch.from_numpy(s['day_of_year']) for s in samples]).float(),
                'day_of_week': torch.stack([torch.from_numpy(s['day_of_week']) for s in samples]).float(),
                'hour_of_day': torch.stack([torch.from_numpy(s['hour_of_day']) for s in samples]).float(),
                'load': torch.stack([torch.from_numpy(s['load']) for s in samples]).float(),
            }
            if self.weather_inputs:
                for w in self.weather_inputs:
                    batch[w] = torch.stack([s[w] for s in samples]).float()

            return batch

        return _collate


if __name__ == '__main__':
    import os 

    dataset_path = Path(os.environ.get('BUILDINGS_BENCH', ''))
    index_file = 'train_weekly.idx'
    context_len = 168
    pred_len = 24
    apply_scaler_transform = 'boxcox'
    scaler_transform_path =  dataset_path / 'metadata' / 'transforms'
    weather_inputs = ['temperature', 'humidity', 'wind_speed', 'wind_direction', 'global_horizontal_radiation', 
                      'direct_normal_radiation', 'diffuse_horizontal_radiation']
    dataset = Buildings900K(dataset_path, index_file, context_len, pred_len, apply_scaler_transform, scaler_transform_path, weather_inputs)
    
    print(f'Number of time series: {len(dataset)}')
    print(f'First sample: {dataset[0]}')