import numpy as np
from skimage.restoration import richardson_lucy, unsupervised_wiener, wiener
import matplotlib.pyplot as plt
from PIL import Image
import imageio

image = np.asarray(Image.open("m92.png")).astype(np.float32)
psf = np.asarray(Image.open("psf.png")).astype(np.float32)[:,:,0]

psf = psf/np.sum(psf)

image = image/np.amax(image)

dec_R = wiener(image[:,:,0], psf, 0.5)
dec_G = wiener(image[:,:,1], psf, 0.5)
dec_B = wiener(image[:,:,2], psf, 0.5)

dec = np.zeros(image.shape)
dec[:,:,0] = dec_R
dec[:,:,1] = dec_G
dec[:,:,2] = dec_B

if np.amin(dec) < 0:
    dec = dec - np.amin(dec)
dec = dec / np.amax(dec)

dec = (dec*255).astype(np.uint8)

imageio.imwrite("m92_dec.png", dec)

#plt.imshow(dec)
#plt.show()
