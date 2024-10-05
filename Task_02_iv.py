import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data import sensor_data  # Importing the sensor_data dictionary from data.py

# Define the sensors for fuel consumption
genset_1_fuel_sensor = 'gunnerus/RVG_mqtt/Engine1/fuel_consumption'
genset_3_fuel_sensor = 'gunnerus/RVG_mqtt/Engine3/fuel_consumption'

# Check if the required sensors are available in the sensor data
if genset_1_fuel_sensor in sensor_data and genset_3_fuel_sensor in sensor_data:
    # Extract timestamps and values for fuel consumption
    timestamps_fuel_1 = sensor_data[genset_1_fuel_sensor]['timestamps']
    timestamps_fuel_3 = sensor_data[genset_3_fuel_sensor]['timestamps']

    genset_1_fuel = sensor_data[genset_1_fuel_sensor]['values']
    genset_3_fuel = sensor_data[genset_3_fuel_sensor]['values']

    # Calculate total genset fuel consumption, handling NoneType values
    genset_tot_fuel = np.zeros(len(genset_1_fuel))
    for i in range(len(genset_1_fuel)):
        genset_1_value = genset_1_fuel[i] if genset_1_fuel[i] is not None else 0
        genset_3_value = genset_3_fuel[i] if genset_3_fuel[i] is not None else 0
        genset_tot_fuel[i] = genset_1_value + genset_3_value

    # Convert timestamps to a suitable format for plotting
    timestamps_fuel_1 = pd.to_datetime(timestamps_fuel_1)
    timestamps_fuel_3 = pd.to_datetime(timestamps_fuel_3)

    # Plotting fuel consumption against time
    plt.figure(figsize=(14, 7))

    # Plot Total Fuel Consumption for Gensets
    plt.plot(timestamps_fuel_1, genset_1_fuel, label='Genset 1 Fuel Consumption [L/h]', color='blue')
    plt.plot(timestamps_fuel_3, genset_3_fuel, label='Genset 3 Fuel Consumption [L/h]', color='orange')
    plt.plot(timestamps_fuel_1, genset_tot_fuel, label='Total Genset Fuel Consumption [L/h]', color='green')

    plt.title('Genset Fuel Consumption Over Time')
    plt.xlabel('Time')
    plt.ylabel('Fuel Consumption [L/h]')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

else:
    print("One or more of the required fuel consumption sensors are not found in the data.")
