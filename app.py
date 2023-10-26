import pickle
import pandas as pd
import numpy as np
import requests
from fastapi import FastAPI
import os
import joblib
app = FastAPI()

def processdata(df):
    # Change column names from components.co to co, components.no to no, and so on
    df = df.rename(columns={'components.co': 'co', 'components.no': 'no', 'components.no2': 'no2', 'components.o3': 'o3',
                            'components.so2': 'so2', 'components.pm2_5': 'pm2_5', 'components.pm10': 'pm10',
                            'components.nh3': 'nh3'})
    # Drop the 'main.aqi' column
    df.drop(columns=['main.aqi'], axis=1, inplace=True)

    # Remove no, pm10, dt, and nh3 columns if they exist
    columns_to_remove = ['no', 'pm10', 'dt', 'nh3']
    df.drop(columns=columns_to_remove, axis=1, inplace=True, errors='ignore')

    return df

@app.post("/predict")
async def predict_air_quality():
    api_key = os.environ.get('OPENWEATHER_API_KEY')
    url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat=-6.2088&lon=106.8456&appid={api_key}'
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
        model = model = joblib.load("model.pkl")

        # Make predictions
        predictions = model.predict(df)

        # Map numeric predictions to air quality categories
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

        return df.to_dict(orient='records')

if __name__ == "__main__":
    import uvicorn

    # Use uvicorn to run the FastAPI application on 127.0.0.1 and port 8000
    uvicorn.run("app:app", host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
