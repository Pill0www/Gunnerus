import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#import Task_02_ii

# Load the CSV data with proper delimiter
csv_file = "data.csv"
df = pd.read_csv(csv_file, delimiter=';', header=None, names=['timestamp', 'sensor', 'value', 'unit'])

# Convert the 'timestamp' column to datetime format (handle time zones)
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Drop rows where the timestamp could not be parsed
df = df.dropna(subset=['timestamp'])

# Extract the port and starboard propulsion power using relevant sensors
df_fuel_cons_eng1 = df[df['sensor'].str.contains('Engine1/fuel_consumption')]
df_fuel_cons_eng3 = df[df['sensor'].str.contains('Engine3/fuel_consumption')]

df_port_power = df[df['sensor'].str.contains('port_mp/LoadFeedback')]
df_starboard_power = df[df['sensor'].str.contains('stbd_mp/LoadFeedback')]

df_merged = pd.merge(df_fuel_cons_eng1, df_fuel_cons_eng3, on='timestamp', how='outer')

df_merged.dropna(inplace=True)

Q_hs = 45.4 #[MJ/kg]
V_d = np.pi*(0.127/2)**2*0.154  #Volum cylinder [m^3]

merged_power_df = pd.merge(df_port_power[['timestamp', 'value']], 
                           df_starboard_power[['timestamp', 'value']], 
                           on='timestamp', suffixes=('_port', '_stbd'))

def fuel_consumption_to_kg_per_s(l_per_h):
    return l_per_h * 0.820 / 3600

# Calculate the fuel mass flow rate (kg/s) for each engine
df_merged['fuel_mass_flow_eng1'] = df_merged['fuel_cons_eng1'].apply(fuel_consumption_to_kg_per_s)
df_merged['fuel_mass_flow_eng3'] = df_merged['fuel_cons_eng3'].apply(fuel_consumption_to_kg_per_s)

# Calculate the thermal efficiency for each engine
df_merged['thermal_efficiency_eng1'] = 1/(Q_hs * (df_merged['fuel_mass_flow_eng1']) / df_merged['power_eng1'])
df_merged['thermal_efficiency_eng2'] = 1/(Q_hs * (df_merged['fuel_mass_flow_eng2']) / df_merged['power_eng2'])

def BMEP(power, RPM):
    return (power * 2)/(V_d * RPM)

plt.figure(figsize=(10, 6))
plt.plot(df_merged['timestamp'], df_merged['thermal_efficiency_eng1'], label='Thermal Efficiency Engine 1')
plt.plot(df_merged['timestamp'], df_merged['thermal_efficiency_eng2'], label='Thermal Efficiency Engine 2')
plt.xlabel('Time')
plt.ylabel('Thermal Efficiency')
plt.title('Thermal Efficiency of Engines Over Time')
plt.legend()
plt.grid(True)
plt.show()