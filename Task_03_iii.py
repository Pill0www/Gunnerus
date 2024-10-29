import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV data with proper delimiter
csv_file = "C:/GitHub/Gunnerus/data.csv"
df = pd.read_csv(csv_file, delimiter=';', header=None, names=['timestamp', 'sensor', 'value', 'unit'])

# Convert the 'timestamp' column to datetime format (handle time zones)
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Drop rows where the timestamp could not be parsed
df = df.dropna(subset=['timestamp'])

# Pivot the DataFrame to get sensors as columns
pivoted_data = df.pivot(index='timestamp', columns='sensor', values='value')

# Fill missing values using the backward fill method
filled_data = pivoted_data.bfill()

# Reset the index to get timestamps as a column again
filled_data.reset_index(inplace=True)

# Extract fuel consumption for Engine 1 and Engine 3 in liters per hour

engine1_fuel_consumption_lph = filled_data['gunnerus/RVG_mqtt/Engine1/fuel_consumption'].astype(float).values  # Liters per hour
engine3_fuel_consumption_lph = filled_data['gunnerus/RVG_mqtt/Engine3/fuel_consumption'].astype(float).values  # Liters per hour


# Convert liters per hour to kilograms per hour (using the density of diesel: ~0.832 Kg/L)
engine1_fuel_consumption_kgph = engine1_fuel_consumption_lph * 0.832
engine3_fuel_consumption_kgph = engine3_fuel_consumption_lph * 0.832

 # Total fuel flow rate (kg/h), remove any NaN values
total_fuel_flow_kgph = np.nan_to_num(engine1_fuel_consumption_kgph + engine3_fuel_consumption_kgph)

# Calculate time differences from the start in minutes
time_diff_minutes = (filled_data['timestamp'] - filled_data['timestamp'].iloc[0]).dt.total_seconds() / 60
time_diff_minutes = time_diff_minutes.diff().fillna(0)  # Remove NaNs from time differences

# Calculate cumulative fuel consumption (M_f)
total_fuel_consumption = np.cumsum(total_fuel_flow_kgph * time_diff_minutes / 60)

Average_fuel_consumption = (1/len(total_fuel_flow_kgph))*total_fuel_flow_kgph.sum()

fuel_capacity = 60 # [m^3]
density = 820 # [kg/m^3]

total_fuel = fuel_capacity * density # kg diesel

# Print average fuel consumption in kg/h
print(f'Average fuel consumption for the voyage: {Average_fuel_consumption:.2f} kg per. hour')

Total_sailtime = total_fuel/Average_fuel_consumption # [kg] / [kg/t] = [t]

print(f'Total sailtime is {(Total_sailtime):.2f} hours, assuing the vessle runs on two engines only')
print(f'Which mean the ship could sail for {(Total_sailtime)/24:.0f} days')

print(total_fuel_flow_kgph.max())