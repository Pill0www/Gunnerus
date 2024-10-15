import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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

# Split the data in half for Route 1 and Route 2
half_index = len(filled_data) // 2

# Data for Route 1
timestamps_route_1 = filled_data['timestamp'][:half_index]
engine1_fuel_route_1 = engine1_fuel_consumption_kgph[:half_index]
engine3_fuel_route_1 = engine3_fuel_consumption_kgph[:half_index]
total_fuel_flow_route_1 = total_fuel_flow_kgph[:half_index]

# Data for Route 2
timestamps_route_2 = filled_data['timestamp'][half_index:]
engine1_fuel_route_2 = engine1_fuel_consumption_kgph[half_index:]
engine3_fuel_route_2 = engine3_fuel_consumption_kgph[half_index:]
total_fuel_flow_route_2 = total_fuel_flow_kgph[half_index:]

# Plotting fuel flow rate for Route 1
plt.figure(figsize=(12, 6))
plt.plot(timestamps_route_1, engine1_fuel_route_1, label='Engine 1 Fuel Flow - Route 1', color='blue')
plt.plot(timestamps_route_1, engine3_fuel_route_1, label='Engine 3 Fuel Flow - Route 1', color='orange')
plt.plot(timestamps_route_1, total_fuel_flow_route_1, label='Total Fuel Flow - Route 1', color='green')

# Formatting the plot
plt.title('Fuel Flow Rate (Qf) vs Time - Route 1')
plt.xlabel('Time')
plt.ylabel('Fuel Flow Rate [Kg/h]')
plt.legend()
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.tight_layout()

# Show the plot for Route 1
plt.show()

# Plotting fuel flow rate for Route 2
plt.figure(figsize=(12, 6))
plt.plot(timestamps_route_2, engine1_fuel_route_2, label='Engine 1 Fuel Flow - Route 2', color='blue')
plt.plot(timestamps_route_2, engine3_fuel_route_2, label='Engine 3 Fuel Flow - Route 2', color='orange')
plt.plot(timestamps_route_2, total_fuel_flow_route_2, label='Total Fuel Flow - Route 2', color='green')

# Formatting the plot
plt.title('Fuel Flow Rate (Qf) vs Time - Route 2')
plt.xlabel('Time')
plt.ylabel('Fuel Flow Rate [Kg/h]')
plt.legend()
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.tight_layout()

# Show the plot for Route 2
plt.show()
