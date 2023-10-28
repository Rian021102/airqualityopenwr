import requests
import pandas as pd
from datetime import datetime
import os
from google.cloud import bigquery
import pandas_gbq
# Set the path to your JSON key file as the environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "YOUR_GOOGLE_CREDENTIALS"

# Replace 'your_api_key' with the API key you've been provided
api_key = 'YOUR_API_KEY'

# Define the start and end dates as Unix timestamps
start_date = datetime(2019, 1, 1, 0, 0).timestamp()  # January 1, 2019
end_date = datetime(2023, 10, 27, 23, 59).timestamp()  # September 30, 2023

# Replace the latitude and longitude with Jakarta's coordinates
url = f'http://api.openweathermap.org/data/2.5/air_pollution/history?lat=-1.2676&lon=116.8270&start={int(start_date)}&end={int(end_date)}&appid={api_key}'

# Send a GET request to the API
response = requests.get(url)


def processdata(df):

    # Create a mapping for main.aqi values to air quality labels
    air_quality_mapping = {1: 'Good', 2: 'Fine', 3: 'Medium', 4: 'Poor', 5: 'Very Poor'}
    
    # Create the 'air_quality' column using the mapping
    df['air_quality'] = df['main.aqi'].map(air_quality_mapping)

    # Convert 'dt' to datetime
    df['dt'] = pd.to_datetime(df['dt'], unit='s')

    # Change column names from components.co to co, components.no to no, and so on
    df = df.rename(columns={'components.co': 'co', 'components.no': 'no', 'components.no2': 'no2', 'components.o3': 'o3',
                            'components.so2': 'so2', 'components.pm2_5': 'pm2_5', 'components.pm10': 'pm10',
                            'components.nh3': 'nh3'})
    # Drop the 'main.aqi' column
    df.drop(columns=['main.aqi'], axis=1, inplace=True)

    # Remove no, pm10, dt, and nh3 columns if they exist
    columns_to_remove = ['no', 'pm10','nh3']
    df.drop(columns=columns_to_remove, axis=1, inplace=True, errors='ignore')

    return df




# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()

    # Transform the JSON data into a DataFrame
    df = pd.json_normalize(data['list'])

    df=processdata(df)

    
    # Initialize a BigQuery client
    client = bigquery.Client()

    # Define the BigQuery dataset and table where you want to load the data
    project_id = 'intricate-idiom-379506'
    table_id = 'balikpapanairquality.balikpapanpollution'

    table_schema=[
    {'name': 'dt', 'type': 'TIMESTAMP'},
    {'name': 'co', 'type': 'FLOAT64'},  # Adjust the data types for other columns as needed
    {'name': 'no2', 'type': 'FLOAT64'},
    {'name': 'o3', 'type': 'FLOAT64'},
    {'name': 'so2', 'type': 'FLOAT64'},
    {'name': 'pm2_5', 'type': 'FLOAT64'},
    {'name': 'air_quality', 'type': 'STRING'},
    ]
    

    # Load the DataFrame into BigQuery with "append" mode
    pandas_gbq.to_gbq(df,table_id,project_id,if_exists='replace',table_schema=table_schema)
    # Process the DataFrame as needed
    print(df)
    
else:
    # If the request was not successful, print an error message
    print(f"Error: {response.status_code} - {response.text}")
