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

# Q1: Extract power profiles for Engine 1 and Engine 3
engine1_power = filled_data['gunnerus/RVG_mqtt/Engine1/engine_load'].values  # kW
engine3_power = filled_data['gunnerus/RVG_mqtt/Engine3/engine_load'].values  # kW

# Define route indices
route_1_start = 530
route_1_finish = 1108
route_2_start = route_1_finish
route_2_finish = 2660

# Route 1: Calculate η_e for Engine 1 only
engine1_x_route_1 = 100 * (engine1_power[route_1_start:route_1_finish] / 450)  # Normalized engine 1 power
eta_e_route_1 = -0.0024 * engine1_x_route_1**2 + 0.402 * engine1_x_route_1 + 27.4382  # η_e for Engine 1 on Route 1

# Route 2: Calculate η_e for combined Engine 1 and Engine 3 power
engine_combined_x_route_2 = 100 * ((engine1_power[route_2_start:route_2_finish] + engine3_power[route_2_start:route_2_finish]) / 900)  # Normalized combined power
eta_e_route_2 = -0.0024 * engine_combined_x_route_2**2 + 0.402 * engine_combined_x_route_2 + 27.4382  # η_e for combined engines on Route 2

# Q2: Extract vectors for port and starboard load feedback
port_load_feedback = (500 / 100) * filled_data['gunnerus/RVG_mqtt/hcx_port_mp/LoadFeedback'].values
stbd_load_feedback = (500 / 100) * filled_data['gunnerus/RVG_mqtt/hcx_stbd_mp/LoadFeedback'].values

# Combine the load feedback values
combined_load_feedback = port_load_feedback + stbd_load_feedback

# Extract fuel consumption for Engine 1 and Engine 3
engine1_fuel_consumption = filled_data['gunnerus/RVG_mqtt/Engine1/fuel_consumption'].values
engine3_fuel_consumption = filled_data['gunnerus/RVG_mqtt/Engine3/fuel_consumption'].values

# Total fuel consumption in liters per hour
total_fuel_consumption_lph = engine1_fuel_consumption + engine3_fuel_consumption

# Convert liters per hour to kilograms per hour (using the density of diesel: ~0.832 Kg/L)
total_fuel_consumption_kgph = total_fuel_consumption_lph * 0.832

# Calculate total energy efficiency (ηE) in percentage
energy_density = 42 * 10**6  # Energy content of diesel fuel in J/kg
# Total energy output in Joules (Power in Watts * time in seconds)
total_energy_output_joules = combined_load_feedback * 10**3 * 3600  # J (from kW to J)
# Total energy input from fuel in Joules
total_energy_input_joules = total_fuel_consumption_kgph * energy_density  # J
# Calculate efficiency as a percentage
total_energy_efficiency = (total_energy_output_joules / total_energy_input_joules) * 100

# Calculate time in minutes from the start
time_from_start = (filled_data['timestamp'] - filled_data['timestamp'].iloc[0]).dt.total_seconds() / 60

# Data for Route 1
time_route_1 = time_from_start[route_1_start:route_1_finish]
total_energy_efficiency_route_1 = total_energy_efficiency[route_1_start:route_1_finish]

# Data for Route 2
time_route_2 = time_from_start[route_2_start:route_2_finish]
total_energy_efficiency_route_2 = total_energy_efficiency[route_2_start:route_2_finish]

# Reset the time for Route 1 and Route 2 to start at 0
time_route_1 -= time_route_1.iloc[0]
time_route_2 -= time_route_2.iloc[0]

# Plotting for Route 1: Comparing η_e (Q1) and ηE (Q2)
plt.figure(figsize=(12, 6))
plt.plot(time_route_1, eta_e_route_1, label='Q1 Calculated, Engine Efficiency (η_e) - Route 1 (Engine 1 Only)', color='blue')
plt.plot(time_route_1, total_energy_efficiency_route_1, label='Q2 Data based, Energy Efficiency (ηE) - Route 1', color='orange')
plt.title('Efficiency Comparison - Route 1')
plt.xlabel('Time (minutes from start)')
plt.ylabel('Efficiency [%]')
plt.legend()
plt.tight_layout()
plt.show()

# Plotting for Route 2: Comparing η_e (Q1) and ηE (Q2)
plt.figure(figsize=(12, 6))
plt.plot(time_route_2, eta_e_route_2, label='Q1 Calculated, Engine Efficiency (η_e) - Route 2 (Combined Engines)', color='red')
plt.plot(time_route_2, total_energy_efficiency_route_2, label='Q2 Data based, Energy Efficiency (ηE) - Route 2', color='green')
plt.title('Efficiency Comparison - Route 2')
plt.xlabel('Time (minutes from start)')
plt.ylabel('Efficiency [%]')
plt.legend()
plt.tight_layout()
plt.show()

# Combined Plot for both Routes
plt.figure(figsize=(12, 6))
plt.plot(time_route_1, eta_e_route_1, label='Q1 Calculated, Engine Efficiency (η_e) - Route 1 (Engine 1 Only)', color='blue')
plt.plot(time_route_1, total_energy_efficiency_route_1, label='Q2 Data based, Energy Efficiency (ηE) - Route 1', color='orange')
plt.plot(time_route_2 + time_route_1.iloc[-1], eta_e_route_2, label='Q1 Calculated, Engine Efficiency (η_e) - Route 2 (Combined Engines)', color='red')
plt.plot(time_route_2 + time_route_1.iloc[-1], total_energy_efficiency_route_2, label='Q2 Data based, Energy Efficiency (ηE) - Route 2', color='green')
plt.title('Efficiency Comparison - Combined Routes')
plt.xlabel('Time (minutes from start)')
plt.ylabel('Efficiency [%]')
plt.axvline(x=time_route_1.iloc[-1], color='gray', linestyle='--', label='Transition Point')
plt.legend()
plt.tight_layout()
plt.show()
