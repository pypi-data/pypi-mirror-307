import cv2
import matplotlib.pyplot as plt
import numpy as np

import vstarstack.library.loaders.classic

blur_size = 21
BRIGHTNESS_OVER_AREA=1


def threshold(image, radius, ratio):
    kernel = np.zeros((2*radius+1, 2*radius+1))
    cv2.circle(kernel, (radius, radius), radius, 1, -1)
    kernel = kernel / np.sum(kernel)
    filtered = cv2.filter2D(image, ddepth=-1, kernel=kernel)
    mask = (image > filtered*ratio).astype('uint8')
    return mask

df = next(vstarstack.library.loaders.classic.readjpeg("star_006.png"))
image = df.get_channel("R")[0]
image = cv2.GaussianBlur(image, (3, 3), 0)

gray = (image/np.amax(image)*255).astype('uint8')
thresh = threshold(image, 31, 1.2)

kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2,2))
blob = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
blob = cv2.morphologyEx(blob, cv2.MORPH_CLOSE, kernel)

cnts = cv2.findContours(blob, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
big_contour = max(cnts, key=cv2.contourArea)

fig, axs = plt.subplots(1, 3)
fig.patch.set_facecolor('#222222')
axs[0].imshow(image, cmap='gray')
axs[1].imshow(thresh, cmap='gray')
axs[2].imshow(blob, cmap='gray')

plt.show()
