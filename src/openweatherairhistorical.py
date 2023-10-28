import requests
import pandas as pd
from datetime import datetime

# Replace 'your_api_key' with the API key you've been provided
api_key = 'e86609410bde86678446df12a768d48e'

# Define the start and end dates as Unix timestamps
start_date = datetime(2019, 1, 1, 0, 0).timestamp()  # January 1, 2019
end_date = datetime(2023, 11, 27, 23, 59).timestamp()  # September 30, 2023

# Replace the latitude and longitude with Jakarta's coordinates
url = f'http://api.openweathermap.org/data/2.5/air_pollution/history?lat=-1.2676&lon=116.8270&start={int(start_date)}&end={int(end_date)}&appid={api_key}'


# Send a GET request to the API
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()
    
    # Transform the JSON data into a DataFrame
    df = pd.json_normalize(data['list'])

    # Convert the dt column into a datetime object
    df['dt'] = pd.to_datetime(df['dt'], unit='s')

    df.to_csv('/Users/rianrachmanto/pypro/project/BalikpapanAirQ/data/Balikpapan_air_q.csv',index=False)
    
    # Process the DataFrame as needed
    print(df)
    
else:
    # If the request was not successful, print an error message
    print(f"Error: {response.status_code} - {response.text}")
