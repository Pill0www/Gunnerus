import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates  # Importing mdates for time formatting
from data import sensor_data  # Importing the sensor_data dictionary from data.py

# Define the sensors for Port and Starboard propulsion power
port_power_sensor = 'gunnerus/RVG_mqtt/hcx_port_mp/LoadFeedback'
starboard_power_sensor = 'gunnerus/RVG_mqtt/hcx_stbd_mp/LoadFeedback'

# Check if the required sensors are available in the sensor data
if port_power_sensor in sensor_data and starboard_power_sensor in sensor_data:
    # Extract timestamps and values
    timestamps_port = sensor_data[port_power_sensor]['timestamps']
    port_power = sensor_data[port_power_sensor]['values']
    
    timestamps_starboard = sensor_data[starboard_power_sensor]['timestamps']
    starboard_power = sensor_data[starboard_power_sensor]['values']
    
    # Create DataFrames for the power data
    df_port = pd.DataFrame({'timestamp': timestamps_port, 'P_PMI': pd.to_numeric(port_power, errors='coerce')})
    df_starboard = pd.DataFrame({'timestamp': timestamps_starboard, 'P_SMI': pd.to_numeric(starboard_power, errors='coerce')})
    
    # Convert timestamps to datetime format
    df_port['timestamp'] = pd.to_datetime(df_port['timestamp'])
    df_starboard['timestamp'] = pd.to_datetime(df_starboard['timestamp'])
    
    # Merge both DataFrames on timestamp without filling missing data
    power_df = pd.merge(df_port, df_starboard, on='timestamp', how='outer')

    # Calculate total propulsion power only where data is present for both motors
    power_df['P_TOT'] = (power_df['P_PMI'] + power_df['P_SMI'])

    # Plotting
    plt.figure(figsize=(14, 7))

    # Plot Propulsion Power for each motor
    plt.plot(power_df['timestamp'], (500/100)*power_df['P_PMI'], label='Port Motor Power [kW]', color='blue')
    plt.plot(power_df['timestamp'], (500/100)*power_df['P_SMI'], label='Starboard Motor Power [kW]', color='orange')
    plt.plot(power_df['timestamp'], (500/100)*power_df['P_TOT'], label='Total Power [kW]', color='green')

    # Format the x-axis to show only the time (hours and minutes)
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

    plt.title('Vessel Propulsion Power')
    plt.xlabel('Time')
    plt.ylabel('Power [kW]')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
    plt.show()

else:
    print("One or both of the required sensors are not found in the data.")
