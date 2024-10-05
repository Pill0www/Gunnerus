import pandas as pd

# Load the CSV file using semicolon as a delimiter
file_path = '/Users/frithoftangen/Library/CloudStorage/OneDrive-NTNU/PSM/Prosjekt/Gunnerus/data.csv'  # Update this path to the correct location of your file
data = pd.read_csv(file_path, delimiter=';', names=['timestamp', 'sensor_name', 'value', 'unit'])

# Convert the timestamp column to datetime format
data['timestamp'] = pd.to_datetime(data['timestamp'], errors='coerce')

# Drop rows with invalid timestamps (NaT)
data = data.dropna(subset=['timestamp'])

# List of sensors to extract
sensors_of_interest = [
    'gunnerus/RVG_mqtt/hcx_port_mp/LoadFeedback',
    'gunnerus/RVG_mqtt/hcx_port_mp/RPMFeedback',
    'gunnerus/RVG_mqtt/hcx_stbd_mp/LoadFeedback',
    'gunnerus/RVG_mqtt/Engine1/engine_load',
    'gunnerus/RVG_mqtt/Engine3/engine_load',
    'gunnerus/RVG_mqtt/Engine1/exhaust_temperature1',
    'gunnerus/RVG_mqtt/Engine3/exhaust_temperature2',
    'gunnerus/RVG_mqtt/Engine1/fuel_consumption',
    'gunnerus/RVG_mqtt/Engine3/fuel_consumption',
    'gunnerus/RVG_mqtt/Engine3/engine_speed',
    'gunnerus/RVG_mqtt/Engine1/boost_pressure',
    'gunnerus/RVG_mqtt/Engine2/exhaust_temperature1',
]

# Initialize a dictionary to hold the arrays
sensor_data = {}
timestamps = data['timestamp'].unique()

#Extract data for specified sensors
for sensor in sensors_of_interest:
    sensor_values = data[data['sensor_name'] == sensor]['value'].values
    # Align the sensor values with the timestamps
    aligned_values = [sensor_values[i] if i < len(sensor_values) else None for i in range(len(timestamps))]
    sensor_data[sensor] = {
        'timestamps': timestamps,
        'values': aligned_values
    }

# Accessing sensor data
# for sensor in sensors_of_interest:
#     if sensor in sensor_data:
#         sensor_timestamps = sensor_data[sensor]['timestamps']
#         sensor_values = sensor_data[sensor]['values']
#         print(f"Timestamps for {sensor}: {sensor_timestamps}")
#         print(f"Values for {sensor}: {sensor_values}")

# The sensor_data dictionary now holds all the sensor values aligned with timestamps
# You can now plot the data using libraries such as matplotlib or seaborn