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

# Fill missing values using the backward fill method
filled_data = pivoted_data.bfill()

# Reset the index to get timestamps as a column again
filled_data.reset_index(inplace=True)

# Extract fuel consumption for Engine 1 and Engine 3 in liters per hour

engine1_fuel_consumption_lph = filled_data['gunnerus/RVG_mqtt/Engine1/fuel_consumption'].astype(float).values  # Liters per hour
engine3_fuel_consumption_lph = filled_data['gunnerus/RVG_mqtt/Engine3/fuel_consumption'].astype(float).values  # Liters per hour


# Convert liters per hour to kilograms per hour (using the density of diesel: ~0.832 Kg/L)
engine1_fuel_consumption_kgph = engine1_fuel_consumption_lph * 0.820
engine3_fuel_consumption_kgph = engine3_fuel_consumption_lph * 0.820

# Calculate time differences from the start in minutes
time_diff_minutes = (filled_data['timestamp'] - filled_data['timestamp'].iloc[0]).dt.total_seconds() / 60
time_diff_minutes = time_diff_minutes.diff().fillna(0)  # Remove NaNs from time differences

# Total fuel flow rate (kg/h), remove any NaN values
total_fuel_flow_kgph = np.nan_to_num(engine1_fuel_consumption_kgph + engine3_fuel_consumption_kgph)

# Calculate cumulative fuel consumption (M_f)
total_fuel_consumption = np.cumsum(total_fuel_flow_kgph * time_diff_minutes / 60)

# Calculate the running average fuel consumption
running_avg_fuel_consumption = np.cumsum(total_fuel_flow_kgph) / np.arange(1, len(total_fuel_flow_kgph) + 1)

# Define the route indices for Route 1 and 2
route_1_start = 530
route_1_finish = 1108
route_2_finish = min(2660, len(total_fuel_consumption)-30)

# Print average fuel consumption in kg/h for the voyage
average_fuel_consumption = (np.mean(total_fuel_flow_kgph[route_1_finish:route_2_finish]) + np.mean(total_fuel_flow_kgph[route_1_start:route_1_finish]))/2
average_fuel_consumption_tot = np.mean(total_fuel_flow_kgph)
print(f'Average fuel consumption for Route 1 and Route 2: {average_fuel_consumption:.2f} kg per hour')
print(f'Average fuel consumption for Total trip: {average_fuel_consumption_tot:.2f} kg per hour')

Total_sailtime = 49000/average_fuel_consumption # [kg] / [kg/t] = [t]

print(f'Total sailtime is {(Total_sailtime):.2f} hours, assuing the vessle runs on two engines only')
print(f'Which mean the ship could sail for {(Total_sailtime)/24:.0f} days')

#print(total_fuel_flow_kgph.max())

plt.figure(figsize=(12, 6))
plt.plot(time_diff_minutes.cumsum(), total_fuel_consumption, label='Total Fuel Consumption', color='blue')

# Plot formatting
plt.title('Total Fuel Consumption vs Time for the Entire Trip')
plt.xlabel('Time (minutes from start)')
plt.ylabel('Total Fuel Consumption [Kg]')
plt.legend()
plt.tight_layout()

# Running average fuel consumption over time
plt.plot(time_diff_minutes.cumsum(), running_avg_fuel_consumption, label='Running Average Fuel Consumption', color='orange', linestyle='--')

# Plot formatting
plt.title('Total and Running Average Fuel Consumption Over Time')
plt.xlabel('Time (minutes from start)')
plt.ylabel('Fuel Consumption [Kg]')
plt.legend()
plt.tight_layout()

# Plotting fuel consumption for Route 2
plt.figure(figsize=(12, 6))
plt.plot(time_diff_minutes.cumsum()[route_1_finish:route_2_finish], 
         total_fuel_consumption[route_1_finish:route_2_finish], 
         label='Fuel Consumption - Route 2', color='green')

# Plot formatting
plt.title('Fuel Consumption vs Time - Route 2')
plt.xlabel('Time (minutes from start)')
plt.ylabel('Total Fuel Consumption [Kg]')
plt.legend()
plt.tight_layout()
plt.show()