import pandas as pd
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

# Extract vectors for port and starboard load feedback
port_load_feedback = (500 / 100) * filled_data['gunnerus/RVG_mqtt/hcx_port_mp/LoadFeedback'].values
stbd_load_feedback = (500 / 100) * filled_data['gunnerus/RVG_mqtt/hcx_stbd_mp/LoadFeedback'].values

# Combine the load feedback values
combined_load_feedback = port_load_feedback + stbd_load_feedback

# Extract fuel consumption for Engine 1 and Engine 3
engine1_fuel_consumption = filled_data['gunnerus/RVG_mqtt/Engine1/fuel_consumption'].values
engine3_fuel_consumption = filled_data['gunnerus/RVG_mqtt/Engine3/fuel_consumption'].values

# Total fuel consumption in liters per hour
total_fuel_consumption_lph = engine1_fuel_consumption + engine3_fuel_consumption

# Convert liters per hour to kilograms per hour (using the density of diesel: ~0.832 Kg/L)
total_fuel_consumption_kgph = total_fuel_consumption_lph * 0.832

# Calculate total energy efficiency (ηE) in percentage
energy_density = 42 * 10**6  # Energy content of diesel fuel in J/kg
# Total energy output in Joules (Power in Watts * time in seconds)
total_energy_output_joules = combined_load_feedback * 10**3 * 3600  # J (from kW to J)
# Total energy input from fuel in Joules
total_energy_input_joules = total_fuel_consumption_kgph * energy_density  # J
# Calculate efficiency as a percentage
total_energy_efficiency = (total_energy_output_joules / total_energy_input_joules) * 100

# Calculate time in minutes from the start
time_from_start = (filled_data['timestamp'] - filled_data['timestamp'].iloc[0]).dt.total_seconds() / 60

# Define indices for Route 1 and Route 2
route_1_start = 530
route_1_finish = 1108
route_2_start = route_1_finish
route_2_finish = 2660

# Data for Route 1
time_route_1 = time_from_start[route_1_start:route_1_finish]
total_energy_efficiency_route_1 = total_energy_efficiency[route_1_start:route_1_finish]

# Data for Route 2
time_route_2 = time_from_start[route_2_start:route_2_finish] - time_from_start[route_2_start]  # Adjust to start at 0
total_energy_efficiency_route_2 = total_energy_efficiency[route_2_start:route_2_finish]

# Reset the time for Route 1 to start at 0
time_route_1 -= time_route_1.iloc[0]

# Reset the time for Route 2 to start at 0
time_route_2 -= time_route_2.iloc[0]


# Calculate average energy efficiency for Route 1 and Route 2
avg_eta_route_1 = total_energy_efficiency_route_1.mean()
avg_eta_route_2 = total_energy_efficiency_route_2.mean()

# Output average results
print(f'Average Total Energy Efficiency for Route 1: {avg_eta_route_1:.2f} [%]')
print(f'Average Total Energy Efficiency for Route 2: {avg_eta_route_2:.2f} [%]')
