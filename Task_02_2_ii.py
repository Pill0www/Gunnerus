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

# Extract fuel consumption for Engine 1 and Engine 3
engine1_fuel_consumption_lph = filled_data['gunnerus/RVG_mqtt/Engine1/fuel_consumption'].values  # Liters per hour
engine3_fuel_consumption_lph = filled_data['gunnerus/RVG_mqtt/Engine3/fuel_consumption'].values  # Liters per hour

# Convert liters per hour to kilograms per hour (using the density of diesel: ~0.832 Kg/L)
engine1_fuel_consumption_kgph = engine1_fuel_consumption_lph * 0.832
engine3_fuel_consumption_kgph = engine3_fuel_consumption_lph * 0.832

# Total fuel flow rate (kg/h)
total_fuel_flow_kgph = engine1_fuel_consumption_kgph + engine3_fuel_consumption_kgph

# Calculate time in minutes from the start
time_from_start = (filled_data['timestamp'] - filled_data['timestamp'].iloc[0]).dt.total_seconds() / 60

# Define indices for Route 1 and Route 2
route_1_start = 530
route_1_finish = 1108
route_2_start = route_1_finish
route_2_finish = 2660

# Data for Route 1
time_route_1 = time_from_start[route_1_start:route_1_finish] - time_from_start[route_1_start]  # Start at 0
engine1_fuel_route_1 = engine1_fuel_consumption_kgph[route_1_start:route_1_finish]
engine3_fuel_route_1 = engine3_fuel_consumption_kgph[route_1_start:route_1_finish]
total_fuel_flow_route_1 = total_fuel_flow_kgph[route_1_start:route_1_finish]

# Data for Route 2
time_route_2 = time_from_start[route_2_start:route_2_finish] - time_from_start[route_2_start]  # Start at 0
engine1_fuel_route_2 = engine1_fuel_consumption_kgph[route_2_start:route_2_finish]
engine3_fuel_route_2 = engine3_fuel_consumption_kgph[route_2_start:route_2_finish]
total_fuel_flow_route_2 = total_fuel_flow_kgph[route_2_start:route_2_finish]

# Plotting fuel flow rate for Route 1
plt.figure(figsize=(12, 6))
plt.plot(time_route_1, engine1_fuel_route_1, label='Engine 1 Fuel Flow - Route 1', color='blue')
plt.plot(time_route_1, engine3_fuel_route_1, label='Engine 3 Fuel Flow - Route 1', color='orange')
plt.plot(time_route_1, total_fuel_flow_route_1, label='Total Fuel Flow - Route 1', color='green')

# Formatting the plot
plt.title('Fuel Flow Rate (Qf) vs Time - Route 1')
plt.xlabel('Time (minutes from start)')
plt.ylabel('Fuel Flow Rate [Kg/h]')
plt.legend()
plt.tight_layout()

# Show the plot for Route 1
plt.show()

# Plotting fuel flow rate for Route 2
plt.figure(figsize=(12, 6))
plt.plot(time_route_2, engine1_fuel_route_2, label='Engine 1 Fuel Flow - Route 2', color='blue')
plt.plot(time_route_2, engine3_fuel_route_2, label='Engine 3 Fuel Flow - Route 2', color='orange')
plt.plot(time_route_2, total_fuel_flow_route_2, label='Total Fuel Flow - Route 2', color='green')

# Formatting the plot
plt.title('Fuel Flow Rate (Qf) vs Time - Route 2')
plt.xlabel('Time (minutes from start)')
plt.ylabel('Fuel Flow Rate [Kg/h]')
plt.legend()
plt.tight_layout()

# Show the plot for Route 2
plt.show()
