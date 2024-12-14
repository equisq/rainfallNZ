# app.py

from src.config import *
import src.data_loader as dl
import src.data_preprocessing as dp
import src.data_visualization as dv

# Load the csv file into a pandas DataFrame
water_data = dl.load_data(FILEPATH)

# Get the inputs with get_settings
DATA = dv.get_settings(water_data, DEFAULT_DATA)

# Preprocess the data, creating an instance of the Tank class
Tank = dp.Tank(water_data, DATA)
water_data = Tank.preprocess_data()

# Plot the graphs
dv.visualize_data(water_data, DATA.VOLUME_TANK_L)