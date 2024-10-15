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

# Slicing the vectors in half to get route 1 and route 2
half_index = len(port_load_feedback) // 2  # Use integer division to get an integer index

# Data for Route 1
timestamps_route_1 = filled_data['timestamp'][:half_index]
total_energy_efficiency_route_1 = total_energy_efficiency[:half_index]

# Data for Route 2
timestamps_route_2 = filled_data['timestamp'][half_index:]
total_energy_efficiency_route_2 = total_energy_efficiency[half_index:]

# Plotting Route 1
plt.figure(figsize=(12, 6))
plt.plot(timestamps_route_1, total_energy_efficiency_route_1, label='Total Energy Efficiency - Route 1', color='blue')
plt.plot(timestamps_route_2, total_energy_efficiency_route_2, label='Total Energy Efficiency - Route 2', color='green')
plt.axhline(100, color='red', linestyle='--', label='100% Efficiency')
plt.title('Total Energy Efficiency Over Time')
plt.xlabel('Time')
plt.ylabel('Energy Efficiency [%]')
plt.legend()
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.tight_layout()

# Show the plot for Route 1
plt.show()

# Plotting Route 2
plt.figure(figsize=(12, 6))
plt.plot(timestamps_route_2, total_energy_efficiency_route_2, label='Total Energy Efficiency - Route 2', color='green')
plt.axhline(100, color='red', linestyle='--', label='100% Efficiency')
plt.title('Total Energy Efficiency Over Time - Route 2')
plt.xlabel('Time')
plt.ylabel('Energy Efficiency [%]')
plt.legend()
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.tight_layout()

# Show the plot for Route 2
plt.show()
