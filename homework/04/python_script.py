#!/usr/bin/env python
# coding: utf-8
import json
import pickle
import pandas as pd
import os
import sys
import warnings
import boto3

warnings.filterwarnings('ignore')

year = int(sys.argv[1])  # 2023
month = int(sys.argv[2])  # 05
input_file = f'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{year:04d}-{month:02d}.parquet'
output_file = f'output/yellow_tripdata_{year:04d}-{month:02d}.parquet'
MODEL_FILE = os.getenv('MODEL_FILE', 'model.bin')

with open(MODEL_FILE, 'rb') as f_in:
    dv, model = pickle.load(f_in)

categorical = ['PULocationID', 'DOLocationID']


def read_data(filename):
    df = pd.read_parquet(filename)

    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df['duration'] = df.duration.dt.total_seconds() / 60

    df = df[(df.duration >= 1) & (df.duration <= 60)].copy()

    df[categorical] = df[categorical].fillna(-1).astype('int').astype('str')

    return df


df = read_data(input_file)
dicts = df[categorical].to_dict(orient='records')
X_val = dv.transform(dicts)
y_pred = model.predict(X_val)

print("The predicted standard deviation is : ", y_pred.std())
print("The predicted mean duration is: ", y_pred.mean())

df['ride_id'] = f'{year:04d}/{month:02d}_' + df.index.astype('str')

df_result = pd.DataFrame()
df_result['ride_id'] = df['ride_id']
df_result['predicted_duration'] = y_pred


# Bonus: upload the result to the cloud (Not graded)
f = open("aws_cred.txt", "r")
lines = f.readlines()
ACCESS_SECRET_KEY = lines[0].strip()
ACCESS_KEY_ID = lines[1].strip()
BUCKET_NAME = lines[2].strip()
f.close()
print("connect to s3 bucket")

# S3 Connect
s3 = boto3.resource('s3',
                    aws_access_key_id=ACCESS_KEY_ID,
                    aws_secret_access_key=ACCESS_SECRET_KEY)

s3.Bucket(BUCKET_NAME).put_object(Key=output_file,
                                  Body=json.dumps(df_result.to_parquet(output_file,
                                                                       engine='pyarrow',
                                                                       compression=None,
                                                                       index=False)),
                                  ACL='public-read')

print("status OK")
