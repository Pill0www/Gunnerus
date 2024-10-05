import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV data with proper delimiter
csv_file = "20240910082627.csv"
df = pd.read_csv(csv_file, delimiter=';', header=None, names=['timestamp', 'sensor', 'value', 'unit'])

# Convert the 'timestamp' column to datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Drop rows where the timestamp could not be parsed
df = df.dropna(subset=['timestamp'])

# Extract relevant sensor data for fuel consumption and power output for both engines
df_fuel_cons_eng1 = df[df['sensor'].str.contains('Engine1/fuel_consumption')][['timestamp', 'value']]
df_fuel_cons_eng1.rename(columns={'value': 'fuel_cons_eng1'}, inplace=True)

df_fuel_cons_eng2 = df[df['sensor'].str.contains('Engine3/fuel_consumption')][['timestamp', 'value']]
df_fuel_cons_eng2.rename(columns={'value': 'fuel_cons_eng2'}, inplace=True)

df_power_eng1 = df[df['sensor'].str.contains('Engine1/power')][['timestamp', 'value']]
df_power_eng1.rename(columns={'value': 'power_eng1'}, inplace=True)

df_power_eng2 = df[df['sensor'].str.contains('Engine2/power')][['timestamp', 'value']]
df_power_eng2.rename(columns={'value': 'power_eng2'}, inplace=True)

# Merge dataframes on the 'timestamp' column to align fuel consumption and power output data
df_merged = pd.merge(df_fuel_cons_eng1, df_fuel_cons_eng2, on='timestamp', how='outer')
df_merged = pd.merge(df_merged, df_power_eng1, on='timestamp', how='outer')
df_merged = pd.merge(df_merged, df_power_eng2, on='timestamp', how='outer')

# Drop rows with missing data
df_merged.dropna(inplace=True)

# Convert values to numeric, as they might be read as strings
df_merged[['fuel_cons_eng1', 'fuel_cons_eng2', 'power_eng1', 'power_eng2']] = df_merged[['fuel_cons_eng1', 'fuel_cons_eng2', 'power_eng1', 'power_eng2']].apply(pd.to_numeric)

# Define constants (LHV of diesel fuel in MJ/kg)
LHV_diesel = 42.6  # MJ/kg

# Assuming fuel consumption is in liters/hour and converting to kg/s (1 liter of diesel ≈ 0.832 kg)
def fuel_consumption_to_kg_per_s(l_per_h):
    return l_per_h * 0.832 / 3600

# Calculate the fuel mass flow rate (kg/s) for each engine
df_merged['fuel_mass_flow_eng1'] = df_merged['fuel_cons_eng1'].apply(fuel_consumption_to_kg_per_s)
df_merged['fuel_mass_flow_eng2'] = df_merged['fuel_cons_eng2'].apply(fuel_consumption_to_kg_per_s)

# Calculate the thermal efficiency for each engine
df_merged['thermal_efficiency_eng1'] = df_merged['power_eng1'] / (df_merged['fuel_mass_flow_eng1'] * LHV_diesel * 1000)
df_merged['thermal_efficiency_eng2'] = df_merged['power_eng2'] / (df_merged['fuel_mass_flow_eng2'] * LHV_diesel * 1000)

# Plot the thermal efficiency over time
plt.figure(figsize=(10, 6))
plt.plot(df_merged['timestamp'], df_merged['thermal_efficiency_eng1'], label='Thermal Efficiency Engine 1')
plt.plot(df_merged['timestamp'], df_merged['thermal_efficiency_eng2'], label='Thermal Efficiency Engine 2')
plt.xlabel('Time')
plt.ylabel('Thermal Efficiency')
plt.title('Thermal Efficiency of Engines Over Time')
plt.legend()
plt.grid(True)
plt.show()