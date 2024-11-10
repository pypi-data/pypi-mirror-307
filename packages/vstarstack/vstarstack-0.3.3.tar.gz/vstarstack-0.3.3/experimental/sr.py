import numpy as np
import matplotlib.pyplot as plt
import cv2
import random

import vstarstack.library.loaders.classic
import vstarstack.library.common

from skimage import color, data, restoration


def SNR(reference, img):
    reference = reference[10:-10,10:-10]
    img = img[10:-10,10:-10]
    noise = abs(img - reference)
    nsr = noise / reference
    return 1 / np.mean(nsr[np.where(np.isfinite(nsr))])

def getpixel(img, y, x):
    return vstarstack.library.common.getpixel(img, y, x)[1]

def prepare_image(img, delta):
    h = img.shape[0]
    w = img.shape[1]
    sh = np.zeros(img.shape)
    for y in range(h):
        for x in range(w):
            ny = y-delta[1]
            nx = x-delta[0]
            if ny >= 0 and nx >= 0 and ny < h and nx < w:
                sh[y,x] = getpixel(img, ny, nx)
    sh = cv2.resize(sh, dsize=(int(h/k), int(w/k)), interpolation=cv2.INTER_LINEAR)
    sh = cv2.resize(sh, dsize=(h, w), interpolation=cv2.INTER_NEAREST)
    return sh

def shift_image_back(img, delta):
    sh = np.zeros(img.shape)
    for y in range(img.shape[0]):
        for x in range(img.shape[1]):
            ny = y+delta[1]
            nx = x+delta[0]
            if ny >= 0 and nx >= 0 and ny < img.shape[0] and nx < img.shape[1]:
                sh[y,x] = getpixel(img, ny, nx)
    return sh

random.seed(1)

N = 40
deltas = []
s = 1
k = 2
for _ in range(N):
    delta = ((random.random()*2-1)*s, (random.random()*2-1)*s)
    deltas.append(delta)
shifted = []

img_orig = next(vstarstack.library.loaders.classic.readjpeg('moon.png')).get_channel('R')[0]

img_orig = img_orig / np.amax(img_orig)
frame = None
for i in range(len(deltas)):
    delta = deltas[i]
    sh = prepare_image(img_orig, delta)
    #plt.imshow(sh)
    #plt.show()
    frame = sh
    sh = shift_image_back(sh, delta)
    shifted.append(sh)

s = np.zeros(img_orig.shape)
for i in range(len(shifted)):
    s = s + shifted[i]
s = s / len(shifted)


psf = np.zeros((5, 5))
cv2.circle(psf, (2,2), 2, 1, -1)
psf[2,2]=2
psf = psf / np.sum(psf)
deconvolved = restoration.richardson_lucy(s, psf, num_iter=30)

fig, axs = plt.subplots(2, 3)

axs[0,0].imshow(img_orig)
axs[0,1].imshow(frame)
axs[1,0].imshow(s)
axs[1,1].imshow(deconvolved)
axs[1,2].imshow(deconvolved / img_orig)

plt.show()


print(SNR(img_orig, frame))
print(SNR(img_orig, s))
print(SNR(img_orig, deconvolved))
