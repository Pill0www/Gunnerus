import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data import sensor_data  # Importing the sensor_data dictionary from data.py

# Define the sensors for power input (genset) and power output (propulsion motors)
genset_1_power_sensor = 'gunnerus/RVG_mqtt/Engine1/engine_load'
genset_3_power_sensor = 'gunnerus/RVG_mqtt/Engine3/engine_load'  
port_power_sensor = 'gunnerus/RVG_mqtt/hcx_port_mp/LoadFeedback'
starboard_power_sensor = 'gunnerus/RVG_mqtt/hcx_stbd_mp/LoadFeedback'

# Check if the required sensors are available in the sensor data
if  genset_1_power_sensor in sensor_data and genset_3_power_sensor in sensor_data and port_power_sensor in sensor_data and starboard_power_sensor in sensor_data:
    # Extract timestamps and values for input and output powers
    timestamps_input = sensor_data[genset_1_power_sensor]['timestamps']
    genset_1_power = sensor_data[genset_1_power_sensor]['values']
    genset_3_power = sensor_data[genset_3_power_sensor]['values']

    timestamps_port = sensor_data[port_power_sensor]['timestamps']
    port_power = sensor_data[port_power_sensor]['values']
    
    timestamps_starboard = sensor_data[starboard_power_sensor]['timestamps']
    starboard_power = sensor_data[starboard_power_sensor]['values']
    
    # Create DataFrames for genset power input and propulsion power output
    df_input = pd.DataFrame({'timestamp': timestamps_input, 
                             'P_input': pd.to_numeric(genset_1_power, errors='coerce')})
    df_port = pd.DataFrame({'timestamp': timestamps_port, 
                            'P_PMI': pd.to_numeric(port_power, errors='coerce')})
    df_starboard = pd.DataFrame({'timestamp': timestamps_starboard, 
                                  'P_SMI': pd.to_numeric(starboard_power, errors='coerce')})

    # Merge DataFrames on timestamp without filling missing data
    power_df = pd.merge(df_input, pd.merge(df_port, df_starboard, on='timestamp', how='outer'), 
                        on='timestamp', how='outer')

    # Calculate total propulsion power output
    power_df['P_output'] = power_df['P_PMI'] + power_df['P_SMI']

    # Calculate total genset power, handling NoneType values
    genset_tot_power = np.zeros(len(genset_1_power))
    for i in range(len(genset_1_power)):
        genset_1_value = genset_1_power[i] if genset_1_power[i] is not None else 0
        genset_3_value = genset_3_power[i] if genset_3_power[i] is not None else 0
        genset_tot_power[i] = genset_1_value + genset_3_value

    # Plotting power output and genset total power against time
    plt.figure(figsize=(14, 7))

    # Convert timestamps to a suitable format for plotting if necessary
    power_df['timestamp'] = pd.to_datetime(power_df['timestamp'])

    # Plot Power Output
    plt.plot(power_df['timestamp'], power_df['P_output'], label='Propulsion Power Output [kW]', color='blue')

    # Plot Total Genset Power
    plt.plot(power_df['timestamp'], genset_tot_power, label='Total Genset Power [kW]', color='orange')

    plt.title('Propulsion Power Output vs Total Genset Power Over Time')
    plt.xlabel('Time')
    plt.ylabel('Power [kW]')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

else:
    print("One or more of the required sensors (genset, port motor, starboard motor) are not found in the data.")
