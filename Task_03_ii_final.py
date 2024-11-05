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


# Convert liters per hour to kilograms per hour (using the density of diesel: ~0.820 Kg/L)
engine1_fuel_consumption_kgph = engine1_fuel_consumption_lph * 0.820
engine3_fuel_consumption_kgph = engine3_fuel_consumption_lph * 0.820

 # Total fuel flow rate (kg/h), remove any NaN values
total_fuel_flow_kgph = np.nan_to_num(engine1_fuel_consumption_kgph + engine3_fuel_consumption_kgph)

# Calculate time differences from the start in minutes
time_diff_minutes = (filled_data['timestamp'] - filled_data['timestamp'].iloc[0]).dt.total_seconds() / 60
time_diff_minutes = time_diff_minutes.diff().fillna(0)  # Remove NaNs from time differences

# Calculate cumulative fuel consumption (M_f)
total_fuel_consumption = np.cumsum(total_fuel_flow_kgph * time_diff_minutes / 60)

# Define the route indices
route_1_start = 530
route_1_finish = 1108
route_2_start = route_1_finish
route_2_finish = 2660

# Total fuel consumption for Route 1
total_fuel_consumption_route_1 = total_fuel_consumption[route_1_finish] - total_fuel_consumption[route_1_start]

# Total fuel consumption for Route 2
total_fuel_consumption_route_2 = total_fuel_consumption[route_2_finish] - total_fuel_consumption[route_2_start]

if total_fuel_consumption.size == 0 or np.isnan(total_fuel_consumption).any():
    print("Error: Cumulative fuel consumption could not be calculated due to NaN values.")
else:
    # Total fuel consumption for the entire dataset (last value of the cumulative sum)
    total_fuel_consumed_entire_dataset = total_fuel_consumption.iloc[-1]
    print(f"Total fuel consumption for the entire dataset: {total_fuel_consumed_entire_dataset:.2f} kg")

def diesel_co2(total_fuel_consumed): # in [kg]
    return total_fuel_consumed * 3.1 # in [kg]

plt.plot(filled_data['timestamp'], total_fuel_flow_kgph, label='total fuel flow l pr h')
plt.show()
# Print total fuel consumption for each route
print(f"Total fuel consumption for Route 1: {total_fuel_consumption_route_1:.2f} kg")
print(f"Total fuel consumption for Route 2: {total_fuel_consumption_route_2:.2f} kg")
# Print total fuel consumption for entire voyage
print(f'Total amount Co2 emitted for the voyage is {diesel_co2(total_fuel_consumed_entire_dataset):.2f} kg, assuming access air 1.6 times stoichiometric air-fuel ratio. (23.9:1 air-fuel ratio)')

    # Plotting total fuel consumption over time
plt.figure(figsize=(12, 6))
plt.plot(time_diff_minutes.cumsum(), total_fuel_consumption, label='Total Fuel Consumption - Entire Dataset', color='purple')
#plt.plot(time_diff_minutes.cumsum(), diesel_co2(total_fuel_consumption), label='Total CO2 emitted - Entire Dataset', color='blue')
plt.title('Total Fuel Consumption (M_f) vs Time - Entire Dataset')
plt.xlabel('Time (minutes from start)')
plt.ylabel('Total Fuel Consumption [Kg]')
plt.legend()
plt.tight_layout()
plt.show()
