import numpy as np
import matplotlib.pyplot as plt

# Defining the velocity profile function
def velocity_profile(eta, Lambda):
    return 2 * eta - 2 * eta**3 + eta**4 + (Lambda / 6) * eta * (1 - eta)**3

# Define the range of η values
eta_values = np.linspace(0, 1, 100)

# Values of Λ to plot
Lambda_values = [12, 0, -12, -18]
colors = ['blue', 'lightblue', 'orange', 'red']
labels = [r'$\Lambda = 12$', r'$\Lambda = 0$', r'$\Lambda = -12$', r'$\Lambda = -18$']

# Plot each Λ in a separate window
for Lambda, color, label in zip(Lambda_values, colors, labels):
    u_U = velocity_profile(eta_values, Lambda)
    
    # Create a new figure for each Λ value
    plt.figure(figsize=(6, 7))  # Increase figure height to stretch vertically
    plt.plot(u_U, eta_values, color=color, label=label)  # Swap x and y
    
    # Formatting the plot
    plt.ylabel(r'$\eta$ (Non-dimensional distance from wall)')
    plt.xlabel(r'$\frac{u}{U}$ (Non-dimensional velocity)')
    plt.title(f'Velocity Profile for {label}')
    
    # Add vertical dashed line as a reference point
    plt.axvline(x=0, color='gray', linestyle='--')
    
    # Setting y-axis limits with 0 at the top and 1 at the bottom
    plt.ylim(0, 1)
    plt.xlim(-0.2, 1.2)
    
    # Adding legend and grid
    plt.legend(loc='upper right')
    plt.grid(True)
    
    # Show each figure separately
    plt.show()
