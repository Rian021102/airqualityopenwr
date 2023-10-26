import pickle
import pandas as pd
import numpy as np
import requests



def processdata(df):
    
    
    # Change column names from components.co to co, components.no to no, and so on
    df = df.rename(columns={'components.co': 'co', 'components.no': 'no', 'components.no2': 'no2', 'components.o3': 'o3',
                            'components.so2': 'so2', 'components.pm2_5': 'pm2_5', 'components.pm10': 'pm10',
                            'components.nh3': 'nh3'})
    # Drop the 'main.aqi' column
    df.drop(columns=['main.aqi'], axis=1, inplace=True)

    #remove no, pm10, dt and nh3
    df = df.drop(columns=['no','pm10','dt','nh3'], axis=1, inplace=False)

    return df

api_key = 'your_api_key'

url=f'http://api.openweathermap.org/data/2.5/air_pollution?lat=-1.2676&lon=116.8270&appid={api_key}'

response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    data = response.json()
    
    # Transform the JSON data into a DataFrame
    df = pd.json_normalize(data['list'])

    # Convert the dt column into a datetime object
    df['dt'] = pd.to_datetime(df['dt'], unit='s')
    
    df = processdata(df)
    
    # Load the model

    model = pickle.load(open('/Users/rianrachmanto/pypro/project/BalikpapanAirQ/model/model.pkl', 'rb'))

    # Make predictions
    predictions = model.predict(df)

    #if prediction 0,1,2,3,4 then replace with Good, Fine, Medium, Poor, Very Poor
    if predictions == 0:
        predictions = 'Good'
    elif predictions == 1:
        predictions = 'Fine'
    elif predictions == 2:
        predictions = 'Medium'
    elif predictions == 3:
        predictions = 'Poor'
    else:
        predictions = 'Very Poor'

    df['air_quality'] = predictions

    print(df)

