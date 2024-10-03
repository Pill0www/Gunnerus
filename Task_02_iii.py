import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data with proper delimiter
csv_file = "20240910082627.csv"
df = pd.read_csv(csv_file, delimiter=';', header=None, names=['timestamp', 'sensor', 'value', 'unit'])

# Convert the 'timestamp' column to datetime format (handle time zones)
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Drop rows where the timestamp could not be parsed
df = df.dropna(subset=['timestamp'])

# Extract the port and starboard propulsion power using relevant sensors
df_port_power = df[df['sensor'].str.contains('port_mp/LoadFeedback')]
df_starboard_power = df[df['sensor'].str.contains('stbd_mp/LoadFeedback')]

# Merge dataframes on the 'timestamp' column, to align the data points based on time
merged_power_df = pd.merge(df_port_power[['timestamp', 'value']], 
                           df_starboard_power[['timestamp', 'value']], 
                           on='timestamp', suffixes=('_port', '_stbd'))

# Calculate total propulsion power (Port + Starboard)
merged_power_df['total_power'] = merged_power_df['value_port'] + merged_power_df['value_stbd']

# Assuming genset power is constant for simplicity (replace with actual data if available)
# You might extract this from the CSV similarly to how you extracted propulsion power
genset_power = 1000  # kW, replace with actual genset data if available

# Calculate power efficiency
merged_power_df['power_efficiency'] = (merged_power_df['total_power'] / genset_power) * 100

# Plot power efficiency
plt.figure(figsize=(10, 6))
plt.plot(merged_power_df['timestamp'], merged_power_df['power_efficiency'], label='Power Efficiency', color='purple')
plt.title('Power Efficiency vs Time')
plt.xlabel('Time')
plt.ylabel('Efficiency (%)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Save and show the plot
plt.savefig('/mnt/data/power_efficiency_plot.png')
plt.show()