import matplotlib.pyplot as plt
import numpy as np
x1points=np.array([23,100,89,56])
y1points=np.array([150,200,90,110])
plt.plot(x1points,y1points,marker='o',ms=20,mec='r',mfc='r');
plt.grid()
plt.show()
