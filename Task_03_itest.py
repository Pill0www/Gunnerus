import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data with proper delimiter
csv_file = "data.csv"
df = pd.read_csv(csv_file, delimiter=';', header=None, names=['timestamp', 'sensor', 'value', 'unit'])

# Convert the 'timestamp' column to datetime format (handle time zones)
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Drop rows where the timestamp could not be parsed
df = df.dropna(subset=['timestamp'])

# Extract the fuel consumption and power feedback for engines and thrusters
df_fuel_cons_eng1 = df[df['sensor'].str.contains('Engine1/fuel_consumption')][['timestamp', 'value']].rename(columns={'value': 'fuel_cons_eng1'})
df_fuel_cons_eng3 = df[df['sensor'].str.contains('Engine3/fuel_consumption')][['timestamp', 'value']].rename(columns={'value': 'fuel_cons_eng3'})

df_port_power = df[df['sensor'].str.contains('port_mp/LoadFeedback')][['timestamp', 'value']].rename(columns={'value': 'power_eng1'})
df_starboard_power = df[df['sensor'].str.contains('stbd_mp/LoadFeedback')][['timestamp', 'value']].rename(columns={'value': 'power_eng2'})

# Merge fuel consumption data for Engine 1 and Engine 3
df_merged = pd.merge(df_fuel_cons_eng1, df_fuel_cons_eng3, on='timestamp', how='outer')

# Merge power data for port and starboard engines
merged_power_df = pd.merge(df_port_power, df_starboard_power, on='timestamp', how='outer')

# Merge the fuel and power data into one dataframe
df_merged = pd.merge(df_merged, merged_power_df, on='timestamp', how='outer')

# Drop rows with missing values
df_merged.dropna(inplace=True)

# Given fuel energy content (MJ/kg)
Q_hs = 45.4

# Function to convert fuel consumption from liters per hour (l/h) to kg/s
def fuel_consumption_to_kg_per_s(l_per_h):
    return l_per_h * 820 / 3600  # Diesel density 0.820 kg/L

# Calculate the fuel mass flow rate (kg/s) for each engine
df_merged['fuel_mass_flow_eng1'] = df_merged['fuel_cons_eng1'].apply(fuel_consumption_to_kg_per_s)
df_merged['fuel_mass_flow_eng3'] = df_merged['fuel_cons_eng3'].apply(fuel_consumption_to_kg_per_s)

# Calculate the thermal efficiency for each engine
df_merged['thermal_efficiency_eng1'] = df_merged['power_eng1'] / (Q_hs * df_merged['fuel_mass_flow_eng1'])
df_merged['thermal_efficiency_eng2'] = df_merged['power_eng2'] / (Q_hs * df_merged['fuel_mass_flow_eng3'])

# Plot the thermal efficiency of both engines over time
plt.figure(figsize=(10, 6))
plt.plot(df_merged['timestamp'], df_merged['thermal_efficiency_eng1'], label='Thermal Efficiency Engine 1')
plt.plot(df_merged['timestamp'], df_merged['thermal_efficiency_eng2'], label='Thermal Efficiency Engine 2')
plt.xlabel('Time')
plt.ylabel('Thermal Efficiency')
plt.title('Thermal Efficiency of Engines Over Time')
plt.legend()
plt.grid(True)
plt.show()
