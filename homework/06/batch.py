import pickle
import pandas as pd
import os
import sys

S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')


def get_input_path(year, month):
    default_input_pattern = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
    input_pattern = os.getenv('INPUT_FILE_PATTERN', default_input_pattern)
    return input_pattern.format(year=year, month=month)


def get_output_path(year, month):
    default_output_pattern = 's3://nyc-duration/taxi_type=fhv/year={year:04d}/month={month:02d}/predictions.parquet'
    output_pattern = os.getenv('OUTPUT_FILE_PATTERN', default_output_pattern)
    return output_pattern.format(year=year, month=month)


def read_data(filename):
    """
    Read taxi trip data from a Parquet file, supporting Localstack S3.
    Checks if S3_ENDPOINT_URL is set, and if it is, uses it for reading
    otherwise uses the usual way
    :param filename: The path to the Parquet file containing the taxi trip data.
    :return: A pandas DataFrame with taxi trip data.
    """
    options = {
        'client_kwargs': {
            'endpoint_url': S3_ENDPOINT_URL
        }
    }
    try:
        os.getenv(S3_ENDPOINT_URL)
        df = pd.read_parquet(filename, storage_options=options)
    except (NameError, ValueError):
        df = pd.read_parquet(filename)
    return df


def prepare_data(df, categorical):
    """
    Preprocess taxi trip data.

    :param df: A pandas DataFrame with taxi trip data.
    :param categorical: List of column names to treat as categorical.
    :return: A pandas DataFrame with preprocessed taxi trip data.
    """
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()
    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')
    return df


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


def main(year, month):
    input_file = get_input_path(year, month)
    output_file = get_output_path(year, month)

    with open('model.bin', 'rb') as f_in:
        dv, lr = pickle.load(f_in)

    categorical = ['PULocationID', 'DOLocationID']
    df = read_data(input_file)
    df = prepare_data(df, categorical)
    df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

    dicts = df[categorical].to_dict(orient='records')
    X_val = dv.transform(dicts)
    y_pred = lr.predict(X_val)

    print('predicted mean duration:', y_pred.mean())
    print('the sum of predicted durations: ',y_pred.sum())

    df_result = pd.DataFrame()
    df_result['ride_id'] = df['ride_id']
    df_result['predicted_duration'] = y_pred
    save_data(year, month, df_result)
    return output_file


if __name__ == "__main__":
    if len(sys.argv) > 3:
        print("Usage: python script.py <year> <month>")
        sys.exit(1)
    year = int(sys.argv[1])
    month = int(sys.argv[2])
    main(year, month)
