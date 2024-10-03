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

# Plot propulsion power for port, starboard, and total propulsion power
plt.figure(figsize=(10, 6))
plt.plot(merged_power_df['timestamp'], merged_power_df['value_port'], label='Port Propulsion Power', color='blue')
plt.plot(merged_power_df['timestamp'], merged_power_df['value_stbd'], label='Starboard Propulsion Power', color='green')
plt.plot(merged_power_df['timestamp'], merged_power_df['total_power'], label='Total Propulsion Power', color='red')

# Customize the plot
plt.title('Propulsion Power (Port and Starboard) vs Time')
plt.xlabel('Time')
plt.ylabel('Power (kW)')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Save and show the plot
#plt.savefig('propulsion_power_plot.png')
plt.show()

# -------------------
# Power Efficiency Calculation (Sample Calculation)

# Assume we have genset power data and calculate efficiency:
# efficiency = propulsion_power / genset_power * 100
# For simplicity, let's assume genset power is constant for now (e.g., 1000 kW).

genset_power = 1000  # Replace this with actual genset power data if available
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

# -------------------
# Fuel Consumption (Sample Calculation)

# Extract fuel consumption data for the engines (assuming sensor names)
df_fuel_consumption1 = df[df['sensor'].str.contains('Engine1/fuel_consumption')]
df_fuel_consumption3 = df[df['sensor'].str.contains('Engine3/fuel_consumption')]

# Sum up fuel consumption from both engines
total_fuel_consumption = df_fuel_consumption1['value'].values + df_fuel_consumption3['value'].values

# Plot fuel consumption
plt.figure(figsize=(10, 6))
plt.plot(df_fuel_consumption1['timestamp'], total_fuel_consumption, label='Total Fuel Consumption', color='orange')
plt.title('Fuel Consumption vs Time')
plt.xlabel('Time')
plt.ylabel('Fuel Consumption (Kg/h)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Save and show the plot
plt.savefig('/mnt/data/fuel_consumption_plot.png')
plt.show()

# -------------------
# Energy Efficiency Calculation (Sample Calculation)

# Energy efficiency is generally fuel energy used for propulsion. 
# A simple calculation can be total_propulsion_power / fuel_consumed (energy equivalent) * 100
# For now, we assume a fixed energy per kg of fuel for the calculations

fuel_energy_per_kg = 42.8  # MJ/kg (can vary based on fuel type)
total_fuel_energy = total_fuel_consumption * fuel_energy_per_kg  # MJ

# Calculate total energy efficiency
energy_efficiency = (merged_power_df['total_power'] / total_fuel_energy) * 100

# Plot total energy efficiency
plt.figure(figsize=(10, 6))
plt.plot(merged_power_df['timestamp'], energy_efficiency, label='Energy Efficiency', color='cyan')
plt.title('Total Energy Efficiency vs Time')
plt.xlabel('Time')
plt.ylabel('Energy Efficiency (%)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Save and show the plot
plt.savefig('/mnt/data/energy_efficiency_plot.png')
plt.show()
