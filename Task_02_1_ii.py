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

# Extract vectors for port and starboard load feedback
port_load_feedback = (500/100)*filled_data['gunnerus/RVG_mqtt/hcx_port_mp/LoadFeedback'].values
stbd_load_feedback = (500/100)*filled_data['gunnerus/RVG_mqtt/hcx_stbd_mp/LoadFeedback'].values

# Combine the load feedback values
combined_load_feedback = port_load_feedback + stbd_load_feedback

# Slicing the vectors in half to get route 1 and route 2
half_index = len(port_load_feedback) // 2  # Use integer division to get an integer index

timestamps_route_1 = filled_data['timestamp'][:half_index]
combined_load_feedback_route_1 = combined_load_feedback[:half_index]
port_load_feedback_route_1 = port_load_feedback[:half_index]
stbd_load_feedback_route_1 = stbd_load_feedback[:half_index]

timestamps_route_2 = filled_data['timestamp'][half_index:]
combined_load_feedback_route_2 = combined_load_feedback[half_index:]
port_load_feedback_route_2 = port_load_feedback[half_index:]
stbd_load_feedback_route_2 = stbd_load_feedback[half_index:]

# Plotting Route 1
plt.figure(figsize=(12, 6))
plt.plot(timestamps_route_1, combined_load_feedback_route_1, label='Combined Load Feedback - Route 1', color='green')
plt.plot(timestamps_route_1, port_load_feedback_route_1, label='Port Load Feedback - Route 1', color='blue')
plt.plot(timestamps_route_1, stbd_load_feedback_route_1, label='Starboard Load Feedback - Route 1', color='orange')

# Formatting the plot
plt.title('Thruster Power Over Time - Route 1')
plt.xlabel('Time')
plt.ylabel('Load Feedback (kW)')
plt.legend()
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.tight_layout()

# Show the plot for Route 1
plt.show()

# Plotting Route 2
plt.figure(figsize=(12, 6))
plt.plot(timestamps_route_2, combined_load_feedback_route_2, label='Combined Load Feedback - Route 2', color='green')
plt.plot(timestamps_route_2, port_load_feedback_route_2, label='Port Load Feedback - Route 2', color='blue')
plt.plot(timestamps_route_2, stbd_load_feedback_route_2, label='Starboard Load Feedback - Route 2', color='orange')

# Formatting the plot
plt.title('Thruster Power Over Time - Route 2')
plt.xlabel('Time')
plt.ylabel('Load Feedback (kW)')
plt.legend()
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.tight_layout()

# Show the plot for Route 2
plt.show()
