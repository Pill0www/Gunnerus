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

# Extract fuel consumption for Engine 1 and Engine 3
engine1_fuel_consumption = filled_data['gunnerus/RVG_mqtt/Engine1/fuel_consumption'].values
engine3_fuel_consumption = filled_data['gunnerus/RVG_mqtt/Engine3/fuel_consumption'].values

# Total fuel consumption in liters per hour
total_fuel_consumption_lph = engine1_fuel_consumption + engine3_fuel_consumption

# Convert liters per hour to kilograms per hour (using the density of diesel: ~0.832 Kg/L)
total_fuel_consumption_kgph = total_fuel_consumption_lph * 0.832

# Plotting
plt.figure(figsize=(12, 6))

# Plot total fuel consumption in Kg vs time
plt.plot(filled_data['timestamp'], total_fuel_consumption_kgph, label='Total Fuel Consumption (Kg)', color='green')

# Formatting the plot
plt.title('Total Fuel Consumption vs. Time')
plt.xlabel('Time')
plt.ylabel('Fuel Consumption [Kg/h]')
plt.legend()
plt.xticks(rotation=45)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
plt.tight_layout()

# Show the plot
plt.show()
