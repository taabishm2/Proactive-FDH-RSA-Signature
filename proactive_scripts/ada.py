import matplotlib.pyplot as plt
import numpy as np

# Generate data...
x = np.random.random(100)
y = np.random.random(100)
z = np.random.random(100)

plt.scatter(x, y, c=z, s=10, cmap='viridis')
plt.show()
