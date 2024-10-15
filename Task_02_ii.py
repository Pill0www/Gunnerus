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
a = 500/100
port_load_feedback = a*filled_data['gunnerus/RVG_mqtt/hcx_port_mp/LoadFeedback'].values
stbd_load_feedback = a*filled_data['gunnerus/RVG_mqtt/hcx_stbd_mp/LoadFeedback'].values

# Combine the load feedback values
combined_load_feedback = port_load_feedback + stbd_load_feedback

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(filled_data['timestamp'], port_load_feedback, label='Port Load Feedback', color='blue')
plt.plot(filled_data['timestamp'], stbd_load_feedback, label='Starboard Load Feedback', color='orange')
plt.plot(filled_data['timestamp'], combined_load_feedback, label='Combined Load Feedback', color='green')

# Formatting the plot
plt.title('Thruster Power Over Time')
plt.xlabel('Time')
plt.ylabel('Load Feedback (%)')
plt.legend()
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.tight_layout()

# Show the plot
plt.show()
