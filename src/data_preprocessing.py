# src/data_preprocessing.py

from numpy import mean
import pandas as pd

class Tank:
    def __init__(self, water_data, DATA):
        # Copy variables into self
        self.water_data = water_data
        self.SITE = DATA.SITE
        self.YEAR = DATA.YEAR
        self.AREA_ROOF_M2 = DATA.AREA_ROOF_M2
        self.VOLUME_TANK_L = DATA.VOLUME_TANK_L
        self.VOLUME_USERS_L = DATA.VOLUME_USERS_L
    
    def preprocess_data(self):
        # Filter by year and site
        self.filter_year_site()
        # Call inlet
        self.compute_inlet()
        # Call outlet
        self.compute_outlet()
        # Call difference two times
        # First time: set the start value to half the tank and run
        volume_stored_init_l = self.VOLUME_TANK_L / 2
        volume_difference_l = self.compute_difference(volume_stored_init_l)
        # Second time: set the start value to the mean of all the values of the first run
        volume_stored_init_l = mean(volume_difference_l)
        volume_difference_l = self.compute_difference(volume_stored_init_l)
        # Write the result in the volume_difference_l column
        self.water_data['volume_difference_l'] = volume_difference_l
        return self.water_data
    
    def filter_year_site(self):
            # Filter water_data by the selected year
            self.water_data = self.water_data[self.water_data['date'].dt.year == self.YEAR]
            # Filter water_data by the selected site
            self.water_data = self.water_data[self.water_data['site'] == self.SITE]
            # Reset index to get it continuous
            self.water_data = self.water_data.reset_index(drop=True)
            
    def compute_inlet(self):
        # Compute the volume of rain using the size of the roof and write in in the volume_inlet_l column
        self.water_data['volume_inlet_l'] = self.AREA_ROOF_M2 * self.water_data['rainfall']

    def compute_outlet(self):
        # Write the consumption in the volume_outlet_l column 
        self.water_data['volume_outlet_l'] = self.VOLUME_USERS_L

    def compute_difference(self, volume_stored_init_l):
        volume_difference_l = [volume_stored_init_l for _ in range(len(self.water_data))]
        for index in range(1, len(self.water_data)):
            # Compute difference (not saturated yet)
            volume_difference_l_index = volume_difference_l[index - 1] + self.water_data.iloc[index]['volume_inlet_l'] - self.water_data.iloc[index]['volume_outlet_l']
            # Compute the saturation (between 0 and VOLUME_TANK_L)
            if volume_difference_l_index < 0:
                volume_difference_l[index] = 0
            elif volume_difference_l_index > self.VOLUME_TANK_L:
                volume_difference_l[index] = self.VOLUME_TANK_L
            else:
                volume_difference_l[index] = volume_difference_l_index
        return volume_difference_l