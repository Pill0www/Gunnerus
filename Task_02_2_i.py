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

# Extract engine load for Engine 1 and Engine 3
engine1_load = filled_data['gunnerus/RVG_mqtt/Engine1/engine_load'].values
engine3_load = filled_data['gunnerus/RVG_mqtt/Engine3/engine_load'].values

# Combine engine loads
combined_engine_load = (engine1_load + engine3_load)

# Calculate time in minutes from the start
time_from_start = (filled_data['timestamp'] - filled_data['timestamp'].iloc[0]).dt.total_seconds() / 60

# Define route indices
route_1_start = 530
route_1_finish = 1108
route_2_start = route_1_finish
route_2_finish = 2660

# Data for Route 1
time_route_1 = time_from_start[route_1_start:route_1_finish] - time_from_start[route_1_start]  # Start at 0
engine1_load_route_1 = engine1_load[route_1_start:route_1_finish]
engine3_load_route_1 = engine3_load[route_1_start:route_1_finish]
combined_load_route_1 = combined_engine_load[route_1_start:route_1_finish]

# Data for Route 2
time_route_2 = time_from_start[route_2_start:route_2_finish] - time_from_start[route_2_start]  # Start at 0
engine1_load_route_2 = engine1_load[route_2_start:route_2_finish]
engine3_load_route_2 = engine3_load[route_2_start:route_2_finish]
combined_load_route_2 = combined_engine_load[route_2_start:route_2_finish]

# Plotting Route 1
plt.figure(figsize=(12, 6))
plt.plot(time_route_1, engine1_load_route_1, label='Engine 1 Load - Route 1', color='blue')
plt.plot(time_route_1, engine3_load_route_1, label='Engine 3 Load - Route 1', color='orange')
plt.plot(time_route_1, combined_load_route_1, label='Total Supply Power - Route 1', color='green')

# Formatting the plot for Route 1
plt.title('Generated Power by Each DG and Total Supply Power - Route 1')
plt.xlabel('Time (minutes from start)')
plt.ylabel('Power [kW]')
plt.legend()
plt.tight_layout()
plt.show()

# Plotting Route 2
plt.figure(figsize=(12, 6))
plt.plot(time_route_2, engine1_load_route_2, label='Engine 1 Load - Route 2', color='blue')
plt.plot(time_route_2, engine3_load_route_2, label='Engine 3 Load - Route 2', color='orange')
plt.plot(time_route_2, combined_load_route_2, label='Total Supply Power - Route 2', color='green')

# Formatting the plot for Route 2
plt.title('Generated Power by Each DG and Total Supply Power - Route 2')
plt.xlabel('Time (minutes from start)')
plt.ylabel('Power [kW]')
plt.legend()
plt.tight_layout()
plt.show()
