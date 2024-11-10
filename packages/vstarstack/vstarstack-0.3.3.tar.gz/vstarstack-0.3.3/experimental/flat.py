import vstarstack.library.calibration.flat
import vstarstack.library.loaders.classic
import matplotlib.pyplot as plt
import cv2
import numpy as np

dfg = vstarstack.library.loaders.classic.readjpeg('experimental/flat.jpg')
df = next(dfg)
layer,_ = df.get_channel('L')

layer = layer.astype(np.float64)
h,w = layer.shape
minv = min(w,h)
k = 100/minv
h=int(h*k)
w=int(w*k)

layer_small = cv2.resize(layer, (w,h), interpolation=cv2.INTER_LINEAR)
plt.imshow(layer)
plt.show()

x0,y0,val0,kx,ky = vstarstack.library.calibration.flat.approximate_flat(layer_small)
x0 = x0 / k
y0 = y0 / k
kx = kx * k**2
ky = ky * k**2
print(val0)
layer_approximated = vstarstack.library.calibration.flat.generate_flat(layer.shape[1], layer.shape[0], x0, y0, val0, kx, ky)
plt.imshow(layer_approximated)
plt.show()

rel = layer_approximated / layer
plt.imshow(rel, vmin=0, vmax=2)
plt.show()
