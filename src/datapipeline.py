import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(pathfile):
    df = pd.read_csv(pathfile)
    
    # Create a mapping for main.aqi values to air quality labels
    air_quality_mapping = {1: 'Good', 2: 'Fine', 3: 'Medium', 4: 'Poor', 5: 'Very Poor'}
    
    # Create the 'air_quality' column using the mapping
    df['air_quality'] = df['main.aqi'].map(air_quality_mapping)
    
    # Change column names from components.co to co, components.no to no, and so on
    df = df.rename(columns={'components.co': 'co', 'components.no': 'no', 'components.no2': 'no2', 'components.o3': 'o3',
                            'components.so2': 'so2', 'components.pm2_5': 'pm2_5', 'components.pm10': 'pm10',
                            'components.nh3': 'nh3'})
    #replace negative values on o3 with mode
    df['o3'] = df['o3'].replace(-9999.000000, df['o3'].mode()[0])

    # Convert 'dt' to datetime
    df['dt'] = pd.to_datetime(df['dt'])

    # Drop the 'main.aqi' column
    df.drop(columns=['main.aqi'], axis=1, inplace=True)
    
    # Split the data into X (features) and y (target)
    X = df.drop(columns=['air_quality'])
    y = df['air_quality']
    
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    return X_train, X_test, y_train, y_test

def eda(X_train, y_train):
    # Concatenate X_train and y_train and sort by date
    eda_train = pd.concat([X_train, y_train], axis=1)
    eda_train = eda_train.sort_values(by='dt')
    eda_train = eda_train.reset_index(drop=True)

    # Print missing values
    print(eda_train.isnull().sum())
    print(eda_train.info())
    print(eda_train.describe())
    print(eda_train.columns)

    # Plot countplot of air_quality
    plt.figure(figsize=(10, 5))
    sns.countplot(x='air_quality', data=eda_train)
    plt.show()

    #plot countplot for each year of air_quality where the X axis is the year
    eda_train['year'] = eda_train['dt'].dt.year
    plt.figure(figsize=(10, 5))
    sns.countplot(x='year', hue='air_quality', data=eda_train)
    plt.show()

    # Create function to plot as time series all components
    for i in eda_train.columns[1:9]:
        plt.figure(figsize=(10, 5))
        sns.lineplot(x='dt', y=i, data=eda_train)
        plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
        plt.show()

    # Plot boxplot of all components
    for i in eda_train.columns[1:9]:
        plt.figure(figsize=(10, 5))
        sns.boxplot(x='air_quality', y=i, data=eda_train)
        plt.show()

    # Plot correlation heatmap
    plt.figure(figsize=(10, 5))
    sns.heatmap(eda_train.corr(), annot=True)
    plt.show()

    return eda_train


    