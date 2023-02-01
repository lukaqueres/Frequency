import numpy as np
import matplotlib.pyplot as plt

# Seed for reproducibility
np.random.seed(80)

# Data simulation
x = np.random.normal(0, 1, 1000)
y = 2 * x + 4 * np.random.normal(0, 1, 1000)

# Hexbin chart
fig, ax = plt.subplots()
ax.hexbin(x=x, y=y, gridsize=20, bins="log")
plt.show()
