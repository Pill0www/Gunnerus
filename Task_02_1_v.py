import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file
file_path = '/Users/frithoftangen/Library/CloudStorage/OneDrive-NTNU/PSM/Prosjekt/Gunnerus/data.csv'
data = pd.read_csv(file_path, sep=';', header=None, names=['timestamp', 'sensor', 'value', 'unit'])

# Convert the timestamp to datetime
data['timestamp'] = pd.to_datetime(data['timestamp'])

# Pivot the DataFrame to get sensors as columns
pivoted_data = data.pivot(index='timestamp', columns='sensor', values='value')

# Fill missing values using the forward fill method
filled_data = pivoted_data.fillna(method='ffill')

# Reset the index to get timestamps as a column again
filled_data.reset_index(inplace=True)

# Extract power profiles for Engine 1 and Engine 3
engine1_power = filled_data['gunnerus/RVG_mqtt/Engine1/engine_load'].values  # kW
engine3_power = filled_data['gunnerus/RVG_mqtt/Engine3/engine_load'].values  # kW

# Normalize power to calculate x(t) for each engine
engine1_x = 100 * (engine1_power / 450)  # Normalized engine 1 power
engine3_x = 100 * (engine3_power / 450)  # Normalized engine 3 power

# Calculate η_e for each engine using the given function
engine1_eta_e = -0.0024 * engine1_x**2 + 0.402 * engine1_x + 27.4382
engine3_eta_e = -0.0024 * engine3_x**2 + 0.402 * engine3_x + 27.4382

# Calculate combined efficiency η_e as a weighted average of η_e1 and η_e3
total_power = engine1_power + engine3_power
combined_eta_e = (engine1_eta_e * engine1_power + engine3_eta_e * engine3_power) / total_power

# Calculate total power efficiency η_p by multiplying with constant efficiencies
eta_g = 0.96
eta_VSD = 0.97
eta_SW = 0.99
eta_p = combined_eta_e * eta_g * eta_VSD * eta_SW * 0.97  # Total η_p

# Constants
LHV = 42 * 10**6  # Lower Heating Value in J/kg
seconds_per_hour = 3600  # Number of seconds in an hour

# Convert power to watts
engine1_power_watts = engine1_power * 1000  # kW to W
engine3_power_watts = engine3_power * 1000  # kW to W

# Calculate fuel consumption M_f as a function of time
total_power_watts = engine1_power_watts + engine3_power_watts
M_f = total_power_watts * 3600 / (eta_p / 100 * LHV)

# Calculate time in minutes from the start
time_from_start = (filled_data['timestamp'] - filled_data['timestamp'].iloc[0]).dt.total_seconds() / 60

# Define indices for Route 1 and Route 2
route_1_start = 530
route_1_finish = 1108
route_2_start = route_1_finish
route_2_finish = 2660

# Data for Route 1
time_route_1 = time_from_start[route_1_start:route_1_finish]
M_f_route_1 = M_f[route_1_start:route_1_finish]

# Data for Route 2
time_route_2 = time_from_start[route_2_start:route_2_finish] - time_from_start[route_2_start]  # Adjust to start at 0
M_f_route_2 = M_f[route_2_start:route_2_finish]

# Calculate the total load energy for each route
E_load_route_1 = np.trapz(M_f_route_1, time_route_1)  # Integral of fuel consumption for Route 1
E_load_route_2 = np.trapz(M_f_route_2, time_route_2)  # Integral of fuel consumption for Route 2

# Calculate the total energy supplied for each route
# Assuming we use average η_p over each route for simplicity
avg_eta_p_route_1 = np.mean(eta_p[route_1_start:route_1_finish])
avg_eta_p_route_2 = np.mean(eta_p[route_2_start:route_2_finish])

E_total_route_1 = E_load_route_1 / (avg_eta_p_route_1 / 100)  # Energy supplied for Route 1
E_total_route_2 = E_load_route_2 / (avg_eta_p_route_2 / 100)  # Energy supplied for Route 2

# Calculate energy efficiencies
eta_E_route_1 = (E_load_route_1 / E_total_route_1) * 100  # Energy efficiency for Route 1
eta_E_route_2 = (E_load_route_2 / E_total_route_2) * 100  # Energy efficiency for Route 2

print(f"Total Energy Efficiency (η_E) for Route 1: {eta_E_route_1:.2f}%")
print(f"Total Energy Efficiency (η_E) for Route 2: {eta_E_route_2:.2f}%")

