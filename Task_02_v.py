import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data import sensor_data  # Importing the sensor_data dictionary from data.py

# Define the sensors for fuel consumption and propulsion power output
genset_1_fuel_sensor = 'gunnerus/RVG_mqtt/Engine1/fuel_consumption'
genset_3_fuel_sensor = 'gunnerus/RVG_mqtt/Engine3/fuel_consumption'
port_power_sensor = 'gunnerus/RVG_mqtt/hcx_port_mp/LoadFeedback'
starboard_power_sensor = 'gunnerus/RVG_mqtt/hcx_stbd_mp/LoadFeedback'

# Check if the required sensors are available in the sensor data
if genset_1_fuel_sensor in sensor_data and genset_3_fuel_sensor in sensor_data and port_power_sensor in sensor_data and starboard_power_sensor in sensor_data:
    # Extract timestamps
    timestamps_port = sensor_data[port_power_sensor]['timestamps']
    port_power = sensor_data[port_power_sensor]['values']
    
    timestamps_starboard = sensor_data[starboard_power_sensor]['timestamps']
    starboard_power = sensor_data[starboard_power_sensor]['values']
    # Fuel consumption data
    genset_1_fuel = sensor_data[genset_1_fuel_sensor]['values']
    genset_3_fuel = sensor_data[genset_3_fuel_sensor]['values']

    # Ensure all arrays are the same length
    max_length = max(len(port_power), len(starboard_power))
    
    # Pad arrays with 0 to make them the same length
    port_power = np.pad(port_power, (0, max_length - len(port_power)), 'constant', constant_values=0)
    starboard_power = np.pad(starboard_power, (0, max_length - len(starboard_power)), 'constant', constant_values=0)
    
    # Replace None with 0 in port and starboard power arrays
    port_power = np.array([value if value is not None else 0 for value in port_power])
    starboard_power = np.array([value if value is not None else 0 for value in starboard_power])
    
    # Combine propulsion power from both motors
    total_propulsion_power = port_power + starboard_power

    # Ensure all arrays are the same length
    max_length = max(len(genset_1_fuel), len(genset_3_fuel), len(total_propulsion_power))
    
    # Pad arrays with 0 to make them the same length
    genset_1_fuel = np.pad(genset_1_fuel, (0, max_length - len(genset_1_fuel)), 'constant', constant_values=0)
    genset_3_fuel = np.pad(genset_3_fuel, (0, max_length - len(genset_3_fuel)), 'constant', constant_values=0)
    propulsion_power = np.pad(total_propulsion_power, (0, max_length - len(total_propulsion_power)), 'constant', constant_values=0)
    
    # Replace None with 0 in genset fuel arrays
    genset_1_fuel = np.array([value if value is not None else 0 for value in genset_1_fuel])
    genset_3_fuel = np.array([value if value is not None else 0 for value in genset_3_fuel])
    
    # Calculate total genset fuel consumption
    genset_tot_fuel = genset_1_fuel + genset_3_fuel

    # Convert fuel consumption to power input (1 L of diesel ≈ 36.6 MJ)
    # Assuming density of diesel ≈ 0.85 kg/L and efficiency of engine ≈ 0.4 (40%)
    fuel_to_power_conversion = 36.6 * 1e6 * 0.85 * 0.4  # Convert L to J

    # Calculate total power input (kW)
    genset_tot_power = genset_tot_fuel * fuel_to_power_conversion / 3600  # Convert to kW

    # Replace None with 0 in propulsion power for calculation
    propulsion_power = np.array([value if value is not None else 0 for value in propulsion_power])

    # Calculate total energy efficiency, ensuring no division by zero
    energy_efficiency = np.where(genset_tot_power > 0, (propulsion_power / genset_tot_power) * 100, 0)

    # Convert timestamps to a suitable format for plotting
    timestamps = pd.to_datetime(timestamps_port)

    # Plotting
    plt.figure(figsize=(14, 7))

    # Plot Energy Efficiency
    plt.plot(timestamps, energy_efficiency, label='Total Energy Efficiency [%]', color='purple')

    plt.title('Total Energy Efficiency from Fuel to Propulsion Motors Over Time')
    plt.xlabel('Time')
    plt.ylabel('Energy Efficiency [%]')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

else:
    print("One or more of the required sensors (fuel consumption or propulsion power) are not found in the data.")
