import matplotlib.pyplot as plt
import numpy as np
sectors = [0 for i in range(100)]
with open('C:\sector700.txt', 'r') as file:
    for line in file:
        sectors[int(line) - 1] = sectors[int(line) - 1] + 1
sectors = np.reshape(sectors, (-1,10))
print(sectors)
plt.imshow(sectors, cmap='hot', interpolation='nearest')
plt.show()
