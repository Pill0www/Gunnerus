import numpy as np
import matplotlib.pyplot as plt

# Given values
C = 20e-6  # Capacitance in Farads (20 μF)
V_s = 10  # Source voltage in Volts
R_values = [0.1e3, 1e3, 10e3]  # Resistor values in Ohms (0.1 kΩ, 1 kΩ, 10 kΩ)
t = np.linspace(0, 0.1, 500)  # Time in seconds (0 to 0.1 seconds)

# Function to compute voltage across capacitor V_O(t)
def voltage_across_capacitor(t, R, C, V_s):
    return V_s * (1 - np.exp(-t / (R * C)))

# Plotting the voltage for each R value
plt.figure(figsize=(8, 6))

for R in R_values:
    V_O_t = voltage_across_capacitor(t, R, C, V_s)
    plt.plot(t, V_O_t, label=f'R = {R/1e3} kΩ')

# Adding plot details
plt.title('Voltage Across Capacitor V_O(t) for Different Resistor Values')
plt.xlabel('Time (seconds)')
plt.ylabel('Voltage V_O(t) (Volts)')
plt.grid(True)
plt.legend()
plt.show()
