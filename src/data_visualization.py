# src/data_visualization.py

import pandas as pd
import streamlit as st
from math import pi

def get_settings(water_data, DEFAULT_DATA):
    st.sidebar.header("Settings")

    # Write the default variables in the cache
    st.session_state.update(DEFAULT_DATA)
    
    # Get the sites, drop duplicated, convert into a list and create a selectbox in the sidebar
    sites = water_data['site'].drop_duplicates().tolist()
    st.session_state.SITE = st.sidebar.selectbox("Select a site:", sites, sites.index(st.session_state.SITE))

    # Get the years, drop duplicated, convert into a list and create a selectbox in the sidebar
    years = water_data['date'].dt.year.drop_duplicates().tolist()
    st.session_state.YEAR = st.sidebar.selectbox("Select a year:", years, years.index(st.session_state.YEAR))

    # Get the area of the roof
    st.session_state.WIDTH_ROOF_M = st.sidebar.number_input("Choose the width of your roof (Metres):", 1, 100, st.session_state.WIDTH_ROOF_M)
    st.session_state.LENGTH_ROOF_M = st.sidebar.number_input("Choose the length of your roof (Metres):", 1, 100, st.session_state.LENGTH_ROOF_M)
    st.session_state.AREA_ROOF_M2 = st.session_state.WIDTH_ROOF_M * st.session_state.LENGTH_ROOF_M

    # Get the volume of the tank
    st.session_state.DIAM_INT_TANK_M = st.sidebar.number_input("Choose the diameter of your tank (Metres):", 1, 10, st.session_state.DIAM_INT_TANK_M)
    st.session_state.HEIGHT_INT_TANK_M = st.sidebar.number_input("Choose the height of your tank (Metres):", 1, 10, st.session_state.HEIGHT_INT_TANK_M)
    st.session_state.VOLUME_TANK_M3 = pi * (st.session_state.DIAM_INT_TANK_M / 2) ** 2 * st.session_state.HEIGHT_INT_TANK_M
    st.session_state.VOLUME_TANK_L = st.session_state.VOLUME_TANK_M3 * 1000

    # Get the consumption
    st.session_state.NUMBER_USERS = st.sidebar.number_input("Choose the number of users in your house:", 1, 10, st.session_state.NUMBER_USERS)
    st.session_state.VOLUME_PER_DAY_PER_PERSON_L = st.sidebar.number_input("Choose the volume of water used by a single person:", 1, 1000, st.session_state.VOLUME_PER_DAY_PER_PERSON_L)
    st.session_state.VOLUME_USERS_L = st.session_state.NUMBER_USERS * st.session_state.VOLUME_PER_DAY_PER_PERSON_L
    
    # Return DATA for preprocessing
    return st.session_state

def visualize_data(water_data, VOLUME_TANK_L):
    st.title("RainFall NZ")

    # Print a line chart with the rainfall, the consumption and the water level
    visualize_data_rcw(water_data, VOLUME_TANK_L)

    # Print a bar chart of the days per month when the tank is empty
    visualize_data_empty_tank(water_data)

    # Print a bar chart of the days per month when the tank overflows
    visualize_overflow_tank(water_data, VOLUME_TANK_L)

def visualize_data_rcw(water_data, VOLUME_TANK_L):
    # Create an expander for better visibility
    with st.expander("Graph showing the rainfall, the consumption, and the water level in the tank"):
        # Jump a line because the fullscreen button of the graph protrudes from the chart frame
        st.write('\n')

        # Rename the columns because streamlit is not able to rename the legends
        water_data_st = water_data.rename(columns={'volume_inlet_l': 'Rainfall', 'volume_outlet_l': 'Consumption', 'volume_difference_l': 'Water level'})
        water_data_st['Tank Minimum'] = 0
        water_data_st['Tank Maximum'] = VOLUME_TANK_L

        # Plot the line chart
        st.line_chart(
            water_data_st,
            x='date',
            y=['Rainfall', 'Consumption', 'Water level', 'Tank Minimum', 'Tank Maximum'],
            x_label='Time range',
            y_label='Amount of water (Liters)'
        )

def visualize_data_empty_tank(water_data):
    # Create an expander for better visibility
    with st.expander("Graph showing the days per month when the tank is empty"):
        # Compute the number of days per month when the tank is empty
        empty_tank_df = (water_data[water_data['volume_difference_l'] == 0]
                          .groupby(water_data['date'].dt.to_period('M'))
                          .size()
                          .reset_index(name='Count'))
        empty_tank_df.rename(columns={'date': 'Month'}, inplace=True)
        empty_tank_df['Month'] = empty_tank_df['Month'].dt.to_timestamp()
        empty_tank_df.set_index('Month', inplace=True)
    
        if empty_tank_df.empty:
            # If the tank is never empty, write it
            st.success("The tank is never empty.")
        else:
            # Compute and print the number of days per years when the tank is empty
            total_empty_days = empty_tank_df['Count'].sum()
            st.error(f"The tank is empty for {total_empty_days} days a year.")
            
            # Jump a line because the fullscreen button of the graph protrudes from the chart frame
            st.write('\n')

            # Plot the bar chart
            st.bar_chart(
                empty_tank_df['Count'],
                x_label='Time range',
                y_label='Number of days per month'
            )

def visualize_overflow_tank(water_data, VOLUME_TANK_L):
    # Create an expander for better visibility
    with st.expander("Graph showing the days per month when the tank overflows"):
        # Compute the number of days per month when the tank overflows
        overflow_tank_df = (water_data[water_data['volume_difference_l'] == VOLUME_TANK_L]
                          .groupby(water_data['date'].dt.to_period('M'))
                          .size()
                          .reset_index(name='Count'))
        
        overflow_tank_df.rename(columns={'date': 'Month'}, inplace=True)
        overflow_tank_df['Month'] = overflow_tank_df['Month'].dt.to_timestamp()
        overflow_tank_df.set_index('Month', inplace=True)
    
        if overflow_tank_df.empty:
            # If the tank never overflows, write it
            st.success("The tank never overflows.")
        else:
            # Compute and print the number of days per years when the tank overflows
            total_overflow_days = overflow_tank_df['Count'].sum()
            st.error(f"The tank overflows for {total_overflow_days} days a year.")

            # Jump a line because the fullscreen button of the graph protrudes from the chart frame
            st.write('\n')

            # Plot the bar chart
            st.bar_chart(
                overflow_tank_df['Count'],
                x_label='Time range',
                y_label='Number of days per month'
            )