## Homework

The goal of this homework is to familiarize users with monitoring for ML batch services, using PostgreSQL database to store metrics and Grafana to visualize them.



## Q1. Prepare the dataset

Start with `baseline_model_nyc_taxi_data.ipynb`. Download the March 2024 Green Taxi data. We will use this data to simulate a production usage of a taxi trip duration prediction service.

What is the shape of the downloaded data? How many rows are there?


![Alt text](images/Screenshot%202024-08-26%20at%2014.34.58.png)

* 57457



## Q2. Metric

Let's expand the number of data quality metrics we’d like to monitor! Please add one metric of your choice and a quantile value for the `"fare_amount"` column (`quantile=0.5`).

Hint: explore evidently metric `ColumnQuantileMetric` (from `evidently.metrics import ColumnQuantileMetric`) 

What metric did you choose?


`ColumnQuantileMetric` and `ColumnDriftMetric`

![Alt text](images/Screenshot%202024-08-26%20at%2018.56.59.png)

## Q3. Monitoring

Let’s start monitoring. Run expanded monitoring for a new batch of data (March 2024). 

What is the maximum value of metric `quantile = 0.5` on the `"fare_amount"` column during March 2024 (calculated daily)?

* 14.2 

![Alt text](images/Screenshot%202024-08-26%20at%2018.43.26.png)




## Q4. Dashboard

Finally, let’s add panels with new added metrics to the dashboard. After we customize the  dashboard let's save a dashboard config, so that we can access it later. Hint: click on “Save dashboard” to access JSON configuration of the dashboard. This configuration should be saved locally.

Where to place a dashboard config file?

* `project_folder/dashboards`  (05-monitoring/dashboards)

![Alt text](images/Screenshot%202024-08-26%20at%2019.03.43.png)



## Submit the results

* Submit your answers here: https://courses.datatalks.club/mlops-zoomcamp-2024/homework/hw5
