import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV data with proper delimiter
csv_file = "C:/GitHub/Gunnerus/data.csv"
df = pd.read_csv(csv_file, delimiter=';', header=None, names=['timestamp', 'sensor', 'value', 'unit'])

# Convert the 'timestamp' column to datetime format (handle time zones)
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Drop rows where the timestamp could not be parsed
df = df.dropna(subset=['timestamp'])

# Pivot the DataFrame to get sensors as columns
pivoted_data = df.pivot(index='timestamp', columns='sensor', values='value')

# Fill missing values using the forward fill method
filled_data = pivoted_data.fillna(method='ffill')

# Reset the index to get timestamps as a column again
filled_data.reset_index(inplace=True)

# Extract fuel consumption for engine 1 and 3
df_fuel_cons_eng1 = filled_data['gunnerus/RVG_mqtt/Engine1/fuel_consumption']
df_fuel_cons_eng3 = filled_data['gunnerus/RVG_mqtt/Engine3/fuel_consumption']

#Extract the starboard and portside powerconsuption given in [%]
df_port_power = filled_data['gunnerus/RVG_mqtt/hcx_port_mp/LoadFeedback']
df_starboard_power = filled_data['gunnerus/RVG_mqtt/hcx_stbd_mp/LoadFeedback']

# Extract engine load for Engine 1 and Engine 3 in [kW]
engine1_load = filled_data['gunnerus/RVG_mqtt/Engine1/engine_load'] #.values
engine3_load = filled_data['gunnerus/RVG_mqtt/Engine3/engine_load'] #.values

# Combine engine loads (Combined Engine Power) in [kW]
combined_engine_load = engine1_load + engine3_load

# Calculate total fuel consumption (for engine 1 and engine 3)
total_fuel_consumption_lph = df_fuel_cons_eng1 + df_fuel_cons_eng3

# Energy content of diesel fuel in J/kg (heating value of diesel)
Q_hs = 45.4 # MJ/kg 
V_d = np.pi * (0.127 / 2)**2 * 0.154  # Volume of the cylinder [m^3]

# Function to convert fuel consumption from L/h to g/s
def fuel_consumption_to_g_per_s(l_per_h):
    return l_per_h * 820 / 3600

# Calculate fuel mass flow rate for each engine (in g/s)
fuel_mass_flow_eng1 = fuel_consumption_to_g_per_s(df_fuel_cons_eng1)
fuel_mass_flow_eng3 = fuel_consumption_to_g_per_s(df_fuel_cons_eng3)

def sfc(fuel_mass_flow, power): #[g/s  /  kW] #spesific fuel consumption
    return fuel_mass_flow / power

sfc1 = sfc(fuel_mass_flow_eng1, engine1_load)
sfc2 = sfc(fuel_mass_flow_eng3, engine3_load)

# Calculate thermal efficiency for the engines (assuming power is in kW) in persent
thermal_efficiency_eng1 = 1 / (Q_hs * sfc1) * 100 #%
thermal_efficiency_eng3 = 1 / (Q_hs * sfc2) * 100

# Smooth thermal efficiency data using a moving average
window_size = 25  # Set this to adjust smoothing level
smoothed_thermal_efficiency_eng1 = thermal_efficiency_eng1.rolling(window=window_size, min_periods=1).mean()
smoothed_thermal_efficiency_eng3 = thermal_efficiency_eng3.rolling(window=window_size, min_periods=1).mean()


#Minimum and maximum thermal efficiensis
print(f' minimum thermal eff. at datapoint nr: {thermal_efficiency_eng1.idxmin()}')
print(f' maximum thermal eff. at datapoint nr: {thermal_efficiency_eng1.idxmax()}')

min_thermal_efficiency_eng1 = thermal_efficiency_eng1.min()
max_thermal_efficiency_eng1 = thermal_efficiency_eng1.max()

#Engine torque and BMEP
def Torque(power, rpm): #N = rpm/60 = crank shaft rotational speed (rev/sec)
    return (power * 1000) / (2*np.pi * (rpm/60))

def BMEP(power, rpm):
    return (power*1000*2)/(V_d*8 * (rpm/60)) #times 8 as there is 8 cyinders


#prints of torque and BMPE
print(thermal_efficiency_eng1[2706])
print(f'Torque at max thermal efficiency: {Torque(engine1_load[2706], 1800):.3f} Nm')
print(f'Torque at minimum thermal efficiency: {Torque(engine1_load[5307], 1800):.3f} Nm')
print(f' BMEP at max efficitency: {BMEP(engine1_load[2706], 1800)*10**(-5):.3f} Bar')
print(f' BMEP at minimum efficitency: {BMEP(engine1_load[5307], 1800)*10**(-5):.3f} Bar')
# Plot thermal efficiency over time
plt.figure(figsize=(10, 6))
plt.plot(filled_data['timestamp'], smoothed_thermal_efficiency_eng1, label='Thermal Efficiency Engine 1')
plt.plot(filled_data['timestamp'], smoothed_thermal_efficiency_eng3, label='Thermal Efficiency Engine 3')
plt.xlabel('Time')
plt.ylabel('Thermal Efficiency (%)')
plt.title('Thermal Efficiency of Engines Over Time')
plt.legend()
plt.grid(True)
plt.show()