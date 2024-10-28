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

# Calculate time in minutes from the start
time_from_start = (filled_data['timestamp'] - filled_data['timestamp'].iloc[0]).dt.total_seconds() / 60

# Define route indices
route_1_start = 530
route_1_finish = 1108
route_2_start = route_1_finish
route_2_finish = min(2660, len(time_from_start))  # Ensure the finish index doesn't exceed dataset length

# Data for Route 1 (with time reset to start from 0)
time_route_1 = time_from_start[route_1_start:route_1_finish] - time_from_start[route_1_start]
combined_load_feedback_route_1 = combined_load_feedback[route_1_start:route_1_finish]
port_load_feedback_route_1 = port_load_feedback[route_1_start:route_1_finish]
stbd_load_feedback_route_1 = stbd_load_feedback[route_1_start:route_1_finish]

# Data for Route 2 (with time reset to start from 0)
time_route_2 = time_from_start[route_2_start:route_2_finish] - time_from_start[route_2_start]
combined_load_feedback_route_2 = combined_load_feedback[route_2_start:route_2_finish]
port_load_feedback_route_2 = port_load_feedback[route_2_start:route_2_finish]
stbd_load_feedback_route_2 = stbd_load_feedback[route_2_start:route_2_finish]

# Plotting Route 1
plt.figure(figsize=(12, 6))
plt.plot(time_route_1, combined_load_feedback_route_1, label='Combined Load Feedback - Route 1', color='green')
plt.plot(time_route_1, port_load_feedback_route_1, label='Port Load Feedback - Route 1', color='blue')
plt.plot(time_route_1, stbd_load_feedback_route_1, label='Starboard Load Feedback - Route 1', color='orange')

# Formatting the plot for Route 1
plt.title('Thruster Power Over Time - Route 1')
plt.xlabel('Time (minutes from start)')
plt.ylabel('Load Feedback (kW)')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# Plotting Route 2
plt.figure(figsize=(12, 6))
plt.plot(time_route_2, combined_load_feedback_route_2, label='Combined Load Feedback - Route 2', color='green')
plt.plot(time_route_2, port_load_feedback_route_2, label='Port Load Feedback - Route 2', color='blue')
plt.plot(time_route_2, stbd_load_feedback_route_2, label='Starboard Load Feedback - Route 2', color='orange')

# Formatting the plot for Route 2
plt.title('Thruster Power Over Time - Route 2')
plt.xlabel('Time (minutes from start)')
plt.ylabel('Load Feedback (kW)')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
