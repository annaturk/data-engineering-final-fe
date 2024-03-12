import streamlit as st
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt

import re

from datetime import datetime
from datetime import timezone

import prophet
from prophet import Prophet
from prophet.diagnostics import cross_validation
from prophet.diagnostics import performance_metrics
from prophet.plot import plot_cross_validation_metric
from prophet.plot import plot_plotly, plot_components_plotly

conn = psycopg2.connect(
    host='localhost',
    database='chicago_business_intelligence',
    user='postgres',
    password='root'
)

def get_data(conn):
    cursor = conn.cursor()

    sql = "SELECT * FROM taxi_trips;"

    cursor.execute(sql)
    taxi_trips = cursor.fetchall()

    columns = [d[0] for d in cursor.description]
    df = pd.DataFrame(taxi_trips, columns=columns)

trip_df = get_data(conn)

trip_df['trip_start_timestamp'] = pd.to_datetime(trip_df['trip_start_timestamp'], utc=True)
trip_df['trip_end_timestamp'] = pd.to_datetime(trip_df['trip_end_timestamp'], utc=True)
trip_df['trip_date'] = trip_df['trip_start_timestamp'].dt.date
trip_df['trip_year'] = trip_df['trip_start_timestamp'].dt.year
trip_df['trip_month'] = trip_df['trip_start_timestamp'].dt.month
trip_df['trip_day'] = trip_df['trip_start_timestamp'].dt.day
trip_df['trip_week'] = trip_df['trip_start_timestamp'].dt.weekofyear
trip_df['trip_day_of_week'] = trip_df['trip_start_timestamp'].dt.dayofweek

start_trip_count = trip_df.groupby(['pickup_zip_code'])['trip_id'].count().reset_index(name ='Total_Trips')
start_trip_count.plot.bar(x='pickup_zip_code', y='Total_Trips', rot=60)

end_trip_count = trip_df.groupby(['dropoff_zip_code'])['trip_id'].count().reset_index(name ='Total_Dropoff_Trips')
end_trip_count.plot.bar(x='dropoff_zip_code', y='Total_Dropoff_Trips', rot=60)

trip_count = pd.merge(start_trip_count, end_trip_count, left_on='pickup_zip_code', right_on='dropoff_zip_code', how='outer')
trip_count.fillna(0, inplace=True)
trip_count.drop(columns=['dropoff_zip_code'], inplace=True)
ax1 = trip_count.plot.bar(x='pickup_zip_code', y=['Total_Trips', 'Total_Dropoff_Trips'], rot=60, figsize=(15, 4))

daily_df = trip_df.groupby(['trip_date',
                         'pickup_zip_code'])['trip_id'].count().reset_index(name ='Total_trips_per_month')
daily_df
daily_dropoff_df = trip_df.groupby(['trip_date',
                         'dropoff_zip_code'])['trip_id'].count().reset_index(name ='Total_dropoff_trips_per_month')
daily_dropoff_df

df_trip_count=trip_df.groupby(['trip_date'])['trip_id'].count().reset_index(name='total_trips')
df_trip_count = df_trip_count.rename(columns = {'trip_date': 'ds',
                                'total_trips': 'y'})
 
model = Prophet(yearly_seasonality=True, daily_seasonality=True)
model.fit(df_trip_count) 
future_dates = model.make_future_dataframe(periods = 50, freq='W')
forecast = model.predict(future_dates)

model.plot(forecast)

