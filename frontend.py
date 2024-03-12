import os
import streamlit as st
import pandas as pd
import psycopg2

from prophet import Prophet
from prophet.plot import plot_plotly

port = int(os.environ.get("PORT", 8501))

conn = psycopg2.connect(
    host='/cloudsql/macro-nuance-416801:us-central1:mypostgres',
    database='chicago_business_intelligence',
    user='postgres',
    password='root'
)

@st.cache_data
def get_trips(connection):
    cursor = conn.cursor()

    sql = "SELECT * FROM taxi_trips;"

    cursor.execute(sql)
    taxi_trips = cursor.fetchall()

    columns = [d[0] for d in cursor.description]
    df = pd.DataFrame(taxi_trips, columns=columns)

    trip_df['trip_start_timestamp'] = pd.to_datetime(trip_df['trip_start_timestamp'], utc=True)
    trip_df['trip_end_timestamp'] = pd.to_datetime(trip_df['trip_end_timestamp'], utc=True)
    trip_df['trip_date'] = trip_df['trip_start_timestamp'].dt.date
    trip_df['trip_year'] = trip_df['trip_start_timestamp'].dt.year
    trip_df['trip_month'] = trip_df['trip_start_timestamp'].dt.month
    trip_df['trip_day'] = trip_df['trip_start_timestamp'].dt.day
    trip_df['trip_week'] = trip_df['trip_start_timestamp'].dt.weekofyear
    trip_df['trip_day_of_week'] = trip_df['trip_start_timestamp'].dt.dayofweek

    return trip_df

def main():
    st.title('Taxi Trip Forecast in Chicago')
    
    start_trip_count = trip_df.groupby(['pickup_zip_code'])['trip_id'].count().reset_index(name ='Total_Trips')
    st.bar_chart(start_trip_count)

    end_trip_count = trip_df.groupby(['dropoff_zip_code'])['trip_id'].count().reset_index(name ='Total_Dropoff_Trips')
    st.bar_chart(end_trip_count)

    trip_count = pd.merge(start_trip_count, end_trip_count, left_on='pickup_zip_code', right_on='dropoff_zip_code', how='outer')
    trip_count.fillna(0, inplace=True)
    trip_count.drop(columns=['dropoff_zip_code'], inplace=True)
    st.bar_chart(trip_count, x="pickup_zip_code", y=['Total_Trips', 'Total_Dropoff_Trips'], color="col3")

    daily_df = trip_df.groupby(['trip_date',
                            'pickup_zip_code'])['trip_id'].count().reset_index(name ='Total_trips_per_month')
    daily_df
    daily_dropoff_df = trip_df.groupby(['trip_date',
                            'dropoff_zip_code'])['trip_id'].count().reset_index(name ='Total_dropoff_trips_per_month')
    st.dataframe(daily_df)
    st.dataframe(daily_dropoff_df)

    df_trip_count=trip_df.groupby(['trip_date'])['trip_id'].count().reset_index(name='total_trips')
    df_trip_count = df_trip_count.rename(columns = {'trip_date': 'ds',
                                    'total_trips': 'y'})
    model = Prophet(yearly_seasonality=True, daily_seasonality=True)
    model.fit(df_trip_count) 
    future_dates = model.make_future_dataframe(periods = 50, freq='W')
    forecast = model.predict(future_dates)

    fig = plot_plotly(model, forecast)
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
