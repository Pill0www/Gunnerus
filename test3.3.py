import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV data with proper delimiter
csv_file = "C:/GitHub/Gunnerus/data.csv"
df = pd.read_csv(csv_file, delimiter=';', header=None, names=['timestamp', 'sensor', 'value', 'unit'])

# Convert the 'timestamp' column to datetime format
df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')

# Drop rows where the timestamp could not be parsed
df = df.dropna(subset=['timestamp'])

# Pivot the DataFrame to get sensors as columns
pivoted_data = df.pivot(index='timestamp', columns='sensor', values='value')

# Fill missing values using forward fill
filled_data = pivoted_data.fillna(method='ffill').reset_index()

# Extract fuel consumption data for engines
df_fuel_cons_eng1 = filled_data['gunnerus/RVG_mqtt/Engine1/fuel_consumption'].astype(float)
df_fuel_cons_eng3 = filled_data['gunnerus/RVG_mqtt/Engine3/fuel_consumption'].astype(float)

# Convert liters per hour to kg per hour
fuel_density = 0.820  # Diesel density in kg/L
engine1_fuel_consumption_kgph = df_fuel_cons_eng1 * fuel_density
engine3_fuel_consumption_kgph = df_fuel_cons_eng3 * fuel_density

# Total fuel flow rate (kg/h), handling any NaN values
total_fuel_flow_kgph = np.nan_to_num(engine1_fuel_consumption_kgph + engine3_fuel_consumption_kgph)

# Calculate cumulative fuel consumption (in kg)
time_diff_hours = (filled_data['timestamp'] - filled_data['timestamp'].iloc[0]).dt.total_seconds() / 3600
cumulative_fuel_consumption = np.cumsum(total_fuel_flow_kgph * np.diff(np.insert(time_diff_hours.values, 0, 0)))

# Define the route indices
route_1_start = 530
route_1_finish = 1108
route_2_start = route_1_finish
route_2_finish = 2660

# Total fuel consumption for Route 1
total_fuel_consumption_route_1 = cumulative_fuel_consumption[route_1_finish] - cumulative_fuel_consumption[route_1_start]

# Total fuel consumption for Route 2
total_fuel_consumption_route_2 = cumulative_fuel_consumption[route_2_finish] - cumulative_fuel_consumption[route_2_start]

window_size = 20
# Plot the running average fuel consumption
plt.figure(figsize=(10, 6))
plt.plot(filled_data['timestamp'], engine1_fuel_consumption_kgph.rolling(window=window_size, min_periods=1).mean(), label='Engine 1')
plt.plot(filled_data['timestamp'], engine3_fuel_consumption_kgph.rolling(window=window_size, min_periods=1).mean(), label='Engine 3')
plt.xlabel('Time')
plt.ylabel('Fuel Consumption (kg/h)')
plt.title('Average Fuel Consumption')
plt.legend()
plt.grid(True)
plt.show()
