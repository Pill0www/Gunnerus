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

# Scale factor for load feedback
a = 500 / 100

# Extract vectors for port and starboard load feedback
port_load_feedback = a * filled_data['gunnerus/RVG_mqtt/hcx_port_mp/LoadFeedback'].values
stbd_load_feedback = a * filled_data['gunnerus/RVG_mqtt/hcx_stbd_mp/LoadFeedback'].values

# Combine the load feedback values (Combined Thruster Power)
combined_thruster_power = port_load_feedback + stbd_load_feedback

# Extract engine load for Engine 1 and Engine 3
engine1_load = filled_data['gunnerus/RVG_mqtt/Engine1/engine_load'].values
engine3_load = filled_data['gunnerus/RVG_mqtt/Engine3/engine_load'].values

# Combine engine loads (Combined Engine Power)
combined_engine_load = engine1_load + engine3_load

# Split the data in half for Route 1 and Route 2
half_index = len(filled_data) // 2

# Data for Route 1
timestamps_route_1 = filled_data['timestamp'][:half_index]
combined_thruster_power_route_1 = combined_thruster_power[:half_index]
engine1_load_route_1 = engine1_load[:half_index]
engine3_load_route_1 = engine3_load[:half_index]

# Data for Route 2
timestamps_route_2 = filled_data['timestamp'][half_index:]
combined_thruster_power_route_2 = combined_thruster_power[half_index:]
engine1_load_route_2 = engine1_load[half_index:]
engine3_load_route_2 = engine3_load[half_index:]

# Plotting Route 1
plt.figure(figsize=(12, 6))
plt.plot(timestamps_route_1, engine1_load_route_1, label='Engine 1 Load - Route 1', color='blue')
plt.plot(timestamps_route_1, engine3_load_route_1, label='Engine 3 Load - Route 1', color='orange')
plt.plot(timestamps_route_1, combined_engine_load[:half_index], label='Total Supply Power - Route 1', color='green')

# Formatting the plot
plt.title('Generated Power by Each DG and Total Supply Power - Route 1')
plt.xlabel('Time')
plt.ylabel('Power [kW]')
plt.axhline(0, color='black', linestyle='--')
plt.legend()
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.tight_layout()

# Show the plot for Route 1
plt.show()

# Plotting Route 2
plt.figure(figsize=(12, 6))
plt.plot(timestamps_route_2, engine1_load_route_2, label='Engine 1 Load - Route 2', color='blue')
plt.plot(timestamps_route_2, engine3_load_route_2, label='Engine 3 Load - Route 2', color='orange')
plt.plot(timestamps_route_2, combined_engine_load[half_index:], label='Total Supply Power - Route 2', color='green')

# Formatting the plot
plt.title('Generated Power by Each DG and Total Supply Power - Route 2')
plt.xlabel('Time')
plt.ylabel('Power [kW]')
plt.axhline(0, color='black', linestyle='--')
plt.legend()
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.tight_layout()

# Show the plot for Route 2
plt.show()
