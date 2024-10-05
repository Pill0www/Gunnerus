import pandas as pd
import matplotlib.pyplot as plt
from data import sensor_data  # Importing the sensor_data dictionary from data.py

# Define the sensors for Port and Starboard propulsion power
port_power_sensor = 'gunnerus/RVG_mqtt/hcx_port_mp/LoadFeedback'
starboard_power_sensor = 'gunnerus/RVG_mqtt/hcx_stbd_mp/LoadFeedback'

# Check if the required sensors are available in the sensor data
if port_power_sensor in sensor_data and starboard_power_sensor in sensor_data:
    # Extract timestamps and values
    timestamps = sensor_data[port_power_sensor]['timestamps']
    port_power = sensor_data[port_power_sensor]['values']
    starboard_power = sensor_data[starboard_power_sensor]['values']

    # Create DataFrames for the power data
    power_df = pd.DataFrame({
        'timestamp': timestamps,
        'P_PMI': pd.to_numeric(port_power, errors='coerce'),
        'P_SMI': pd.to_numeric(starboard_power, errors='coerce')
    })

    # Fill forward missing values
    power_df.fillna(method='ffill', inplace=True)

    # Calculate total propulsion power
    power_df['P_TOT'] = power_df['P_PMI'] + power_df['P_SMI']

    # Plotting
    plt.figure(figsize=(14, 7))

    # Plot Propulsion Power for each motor
    plt.plot(power_df['timestamp'], power_df['P_PMI'], label='Port Motor Power [kW]', color='blue')
    plt.plot(power_df['timestamp'], power_df['P_SMI'], label='Starboard Motor Power [kW]', color='orange')
    plt.plot(power_df['timestamp'], power_df['P_TOT'], label='Total Power [kW]', color='green')

    plt.title('Vessel Propulsion Power')
    plt.xlabel('Time')
    plt.ylabel('Power [kW]')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

else:
    print("One or both of the required sensors are not found in the data.")
