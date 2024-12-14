# src/data_loader.py

import pandas as pd

def load_data(FILEPATH):
    # Load CSV file
    water_data = pd.read_csv(FILEPATH)
    # Set the date column to datetime
    water_data['date'] = pd.to_datetime(water_data['date'], format='%Y-%m-%d')
    return water_data