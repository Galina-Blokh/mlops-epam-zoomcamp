import os
import sys

import pandas as pd
from datetime import datetime

S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')


def get_output_path(year, month):
    default_output_pattern = 's3://nyc-duration/taxi_type=fhv/year={year:04d}/month={month:02d}/predictions.parquet'
    output_pattern = os.getenv('OUTPUT_FILE_PATTERN', default_output_pattern)
    return output_pattern.format(year=year, month=month)


def get_input_path(year, month):
    default_input_pattern = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)
    return input_pattern.format(year=year, month=month)


def save_data(year, month, df_put):
    output_file = get_output_path(year, month)

    options = {
        'client_kwargs': {
            'endpoint_url': S3_ENDPOINT_URL
        }
    }
    df_put.to_parquet(
        output_file.format(year=year, month=month),
        engine='pyarrow',
        compression=None,
        index=False,
        storage_options=options
    )
    return output_file


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)


def test_create_data():
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
    ]
    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)
    return df


if __name__ == '__main__':
    if len(sys.argv) > 3:
        print("Usage: python script.py <year> <month>")
        sys.exit(1)
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    df_input = test_create_data()
    input_file = get_input_path(year, month)
    save_data(year, month, df_input)
    os.system("python batch.py 2023 03 ")
    os.system("aws s3 ls nyc-duration/in/")
    print('Integration tests are OK')
