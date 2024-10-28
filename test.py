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
filled_data.reset_index(inplace=True)

# Extract power profiles for Engine 1 and Engine 3
engine1_power = filled_data['gunnerus/RVG_mqtt/Engine1/engine_load'].values
engine3_power = filled_data['gunnerus/RVG_mqtt/Engine3/engine_load'].values

# Normalize power to calculate x(t) for each engine
engine1_x = 100 * (engine1_power / 450)
engine3_x = 100 * (engine3_power / 450)

# Calculate η_e for each engine
engine1_eta_e = -0.0024 * engine1_x**2 + 0.402 * engine1_x + 27.4382
engine3_eta_e = -0.0024 * engine3_x**2 + 0.402 * engine3_x + 27.4382

# Calculate combined efficiency η_e as weighted average
total_power = engine1_power + engine3_power
combined_eta_e = (engine1_eta_e * engine1_power + engine3_eta_e * engine3_power) / total_power

# Calculate total power efficiency η_p
eta_g = 0.96
eta_VSD = 0.97
eta_SW = 0.99
eta_p = combined_eta_e * eta_g * eta_VSD * eta_SW * 0.97

# Extract vectors for port and starboard load feedback
port_load_feedback = (500 / 100) * filled_data['gunnerus/RVG_mqtt/hcx_port_mp/LoadFeedback'].values
stbd_load_feedback = (500 / 100) * filled_data['gunnerus/RVG_mqtt/hcx_stbd_mp/LoadFeedback'].values
combined_load_feedback = port_load_feedback + stbd_load_feedback

# Extract fuel consumption for Engine 1 and Engine 3
engine1_fuel_consumption = filled_data['gunnerus/RVG_mqtt/Engine1/fuel_consumption'].values
engine3_fuel_consumption = filled_data['gunnerus/RVG_mqtt/Engine3/fuel_consumption'].values

# Total fuel consumption in kg per hour
total_fuel_consumption_lph = engine1_fuel_consumption + engine3_fuel_consumption
total_fuel_consumption_kgph = total_fuel_consumption_lph * 0.832

# Calculate total energy efficiency (ηE)
energy_density = 42 * 10**6
total_energy_output_joules = combined_load_feedback * 10**3 * 3600
total_energy_input_joules = total_fuel_consumption_kgph * energy_density
total_energy_efficiency = (total_energy_output_joules / total_energy_input_joules) * 100

# Calculate time in minutes from the start
time_from_start = (filled_data['timestamp'] - filled_data['timestamp'].iloc[0]).dt.total_seconds() / 60

# Split the data for Route 1 and Route 2
half_index = len(filled_data) // 2 - 360

# Data for Route 1
time_route_1 = time_from_start[:half_index]
eta_p_route_1 = eta_p[:half_index]
total_energy_efficiency_route_1 = total_energy_efficiency[:half_index]

# Plotting η_p and Total Energy Efficiency for Route 1
plt.figure(figsize=(12, 6))
plt.plot(time_route_1, eta_p_route_1, label='Power Efficiency (η_p) - Route 1', color='green')
plt.plot(time_route_1, total_energy_efficiency_route_1, label='Total Energy Efficiency - Route 1', color='blue')
plt.title('Power Efficiency (η_p) and Total Energy Efficiency for Route 1')
plt.xlabel('Time (minutes from start)')
plt.ylabel('Efficiency [%]')
plt.legend()
plt.tight_layout()
plt.show()
