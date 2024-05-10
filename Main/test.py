import matplotlib.pyplot as plt

# EV values and corresponding average energy
ev_values = [15, 17, 21, 26, 30]
average_energy = [7,9,12,15,17]

# Plotting the data
plt.plot(ev_values, average_energy, marker='o', linestyle='-')
plt.xlabel('Number of EVs')
plt.ylabel('Average Energy Consumption (kWh)')
plt.title('Average Energy Consumption vs Number of EVs')
plt.grid(True)
plt.show()

