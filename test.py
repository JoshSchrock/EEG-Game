import numpy as np
x = np.array([[0.5+.7j, 0.2+.3j], [0.3+.2j, 0.8+.2j]])
y = x - x[0]
print(y)