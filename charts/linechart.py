import numpy as np
import matplotlib.pyplot as plt

# Data
x = np.linspace(0, 10, 25)
y = np.sin(x) + x/2

# Line chart
fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()
