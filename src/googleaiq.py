import requests
import pandas as pd

# Define the request data as a dictionary
request_data = {
    "universalAqi": True,
    "location": {
        "latitude": -6.2088,
        "longitude": 106.8456
    },
    "extraComputations": [
        "POLLUTANT_CONCENTRATION",
        "POLLUTANT_ADDITIONAL_INFO"
    ],
    "languageCode": "en"
}

# Define the API key
api_key = 'AIzaSyBh7EFE14EfrBZfab_fcXXZoOJlRuCgJRM'

# Define the API endpoint
url = 'https://airquality.googleapis.com/v1/currentConditions:lookup?key=' + api_key

# Send a POST request using the requests library
response = requests.post(url, json=request_data, headers={'Content-Type': 'application/json'})

# Check if the request was successful
if response.status_code == 200:
    data = response.json()
    # Convert the data to a DataFrame
    df = pd.json_normalize(data)
    print(df)
    df.to_csv('/Users/rianrachmanto/pypro/project/Jakarta-Air-Quality-Prediction/data/raw/googleapi.csv', index=False)
else:
    print(f"Request failed with status code {response.status_code}")
    print(response.text)
