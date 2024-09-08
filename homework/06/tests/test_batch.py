import pandas as pd
from datetime import datetime

from batch import prepare_data


def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)


def test_prepare_data():
    data = [
        (None, None, dt(1, 1), dt(1, 10)),
        (1, 1, dt(1, 2), dt(1, 10)),
        (1, None, dt(1, 2, 0), dt(1, 2, 59)),
        (3, 4, dt(1, 2, 0), dt(2, 2, 1)),
    ]
    columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
    df = pd.DataFrame(data, columns=columns)
    categorical = ['PULocationID', 'DOLocationID']
    processed_df = prepare_data(df, categorical)

    expected_data = [
        {'PULocationID': '-1', 'DOLocationID': '-1', 'duration': 9.0},
        {'PULocationID': '1', 'DOLocationID': '1', 'duration': 8.0},

    ]
    expected_df = pd.DataFrame(expected_data)
    print('expected_df\n',expected_df)

    # Select only the relevant columns for comparison
    processed_df = processed_df[['PULocationID', 'DOLocationID', 'duration']]
    print("processed_df\n",processed_df)
    pd.testing.assert_frame_equal(processed_df.reset_index(drop=True), expected_df.reset_index(drop=True))


# Run the test
if __name__ == "__main__":
    test_prepare_data()

