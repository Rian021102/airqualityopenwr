import pickle
import pandas as pd
import numpy as np
import requests
from fastapi import FastAPI
import os
import joblib
import pandas_gbq
import json
from google.oauth2 import service_account

app = FastAPI()

def processdata(df):
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

@app.post("/predict")
async def predict_air_quality():
    api_key = os.environ.get('OPENWEATHER_API_KEY')
    
    # Ensure that the GOOGLE_CREDENTIALS environment variable is set
    if "GOOGLE_CREDENTIALS" not in os.environ:
        return {"error": "GOOGLE_CREDENTIALS environment variable not set."}

    # Parse the Google Service Account JSON key
    google_credentials = json.loads(os.environ["GOOGLE_CREDENTIALS"])

    # Configure the credentials using google-auth
    credentials = service_account.Credentials.from_service_account_info(google_credentials)
    
    url = f'http://api.openweathermap.org/data/2.5/air_pollution?lat=-1.2676&lon=116.8270&appid={api_key}'
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()

        # Transform the JSON data into a DataFrame
        df = pd.json_normalize(data['list'])

        # Convert the dt column into a datetime object
        df['dt'] = pd.to_datetime(df['dt'], unit='s')

        df = processdata(df)
        df2 = df.copy()
        df2.drop(columns=['dt'], axis=1, inplace=True)

        # Load the model
        model = model = joblib.load("model.pkl")

        # Make predictions
        predictions = model.predict(df2)

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

        # Define the BigQuery dataset and table where you want to load the data
        project_id = 'intricate-idiom-379506'
        table_id = 'balikpapanairquality.balikpapanpollution'

        table_schema = [
            {'name': 'dt', 'type': 'TIMESTAMP'},
            {'name': 'co', 'type': 'FLOAT64'},
            {'name': 'no2', 'type': 'FLOAT64'},
            {'name': 'o3', 'type': 'FLOAT64'},
            {'name': 'so2', 'type': 'FLOAT64'},
            {'name': 'pm2_5', 'type': 'FLOAT64'},
            {'name': 'air_quality', 'type': 'STRING'},
        ]

        # Load the DataFrame into BigQuery with "append" mode
        pandas_gbq.to_gbq(df, table_id, project_id, if_exists='append', table_schema=table_schema, credentials=credentials)

        return df.to_dict(orient='records')

if __name__ == "__main__":
    import uvicorn

    # Use uvicorn to run the FastAPI application on 127.0.0.1 and port 8000
    uvicorn.run("app:app", host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
