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

# Extract power profiles for Engine 1 and Engine 3
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

# Calculate time in minutes from the start
time_from_start = (filled_data['timestamp'] - filled_data['timestamp'].iloc[0]).dt.total_seconds() / 60

# Time data for Route 1 and Route 2, adjusted to start at 0 for each route
time_route_1 = time_from_start[route_1_start:route_1_finish] - time_from_start[route_1_start]
time_route_2 = time_from_start[route_2_start:route_2_finish] - time_from_start[route_2_start]

# Combine time and efficiency data for both routes
combined_time = list(time_route_1) + list(time_route_2 + time_route_1.iloc[-1])  # Add last time of Route 1 to Route 2
combined_eta_e = list(eta_e_route_1) + list(eta_e_route_2)  # Combine η_e values

# Plotting η_e for Route 1 (Engine 1 only)
plt.figure(figsize=(12, 6))
plt.plot(time_route_1, eta_e_route_1, label='Engine Efficiency (η_e) - Route 1 (Engine 1 Only)', color='blue')
plt.title('Engine Efficiency (η_e) vs Time - Route 1 (Engine 1 Only)')
plt.xlabel('Time (minutes from start)')
plt.ylabel('Efficiency η_e [%]')
plt.legend()
plt.tight_layout()
plt.show()

# Plotting η_e for Route 2 (Combined Engines 1 and 3)
plt.figure(figsize=(12, 6))
plt.plot(time_route_2, eta_e_route_2, label='Engine Efficiency (η_e) - Route 2 (Combined Engines 1 and 3)', color='red')
plt.title('Engine Efficiency (η_e) vs Time - Route 2 (Combined Engines 1 and 3)')
plt.xlabel('Time (minutes)')
plt.ylabel('Efficiency η_e [%]')
plt.legend()
plt.tight_layout()
plt.show()

# Plotting η_e for Route 1 (Engine 1 only)
plt.figure(figsize=(12, 6))
plt.plot(time_route_1, eta_e_route_1, label='Engine Efficiency (η_e) - Route 1 (Engine 1 Only)', color='blue')
plt.plot(time_route_2 + time_route_1.iloc[-1], eta_e_route_2, label='Engine Efficiency (η_e) - Route 2 (Combined Engines 1 and 3)', color='red')
plt.title('Engine Efficiency (η_e) vs Time (Combined Routes)')
plt.xlabel('Time (minutes from start)')
plt.ylabel('Efficiency η_e [%]')
plt.axvline(x=time_route_1.iloc[-1], color='gray', linestyle='--', label='Transition Point')
plt.legend()
plt.tight_layout()
plt.show()

