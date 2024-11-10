import numpy as np
import matplotlib.pyplot as plt
import math
import random
import sys
import cv2

import vstarstack.library.common
import vstarstack.library.loaders.classic
import vstarstack.library.data
import vstarstack.library.merge
import vstarstack.library.image_process.normalize

def SNR(signal, tested):
    noise = tested - signal
    #print(np.amin(noise), np.amax(noise))
    return np.median((signal / noise)**2)

def show_hist(image, fig, nbins=None):
    if nbins is None:
        maxv = int(np.amax(image))
        minv = int(np.amin(image))
        nbins = (maxv-minv+1)
    hist, bins = np.histogram(image, bins=nbins)
    fig.bar(bins[:-1], hist, width=(bins[-1]-bins[0])/(len(bins)))

def noise_image(image, peak : float, num_points : int):
    op = np.amax(image)
    image = np.random.poisson(image / op * peak) / peak * op
    w = image.shape[1]
    h = image.shape[0]
    for _ in range(num_points):
        x = int(random.random() * w)
        y = int(random.random() * h)
        image[y, x] = 1
    image = image + np.random.normal(0, size=image.shape)*0.1
    image = np.clip(image, 0.00001, 1)
    return image

original_image = next(vstarstack.library.loaders.classic.readjpeg("pleyades.png"))
print(original_image.params)
original_image = vstarstack.library.image_process.normalize.normalize(original_image)
orc = original_image.get_channel("L")[0]
original_image.replace_channel(np.clip(orc / np.amax(orc), 0.001, 1), "L")

N = 144
peak = 4

images = [original_image.copy()]
for _ in range(N-1):
    images.append(original_image.copy())

chns = []

for image in images:
    channel, _ = image.get_channel("L")
    channel = noise_image(channel, peak, 2500)
    image.replace_channel(channel, "L")
    chns.append(channel)

orig = original_image.get_channel("L")[0]
noised = images[0].get_channel("L")[0]



med = np.median(chns, axis=0)
src = vstarstack.library.common.ListImageSource(images)
mean = vstarstack.library.merge.simple_mean(src)
ks = vstarstack.library.merge.kappa_sigma(src, 3, 3, 4)

meaned = mean.get_channel("L")[0]
sigma_clip = ks.get_channel("L")[0]

fig, axs = plt.subplots(2, 3)
fig.patch.set_facecolor('#222222')
axs[0,0].imshow(orig, cmap='gray')
axs[0,1].imshow(noised, cmap='gray')
axs[1,0].imshow(med, cmap='gray')
axs[1,1].imshow(meaned, cmap='gray')
axs[1,2].imshow(sigma_clip, cmap='gray')
plt.show()

ry = int(orig.shape[0]/2)
rx = int(orig.shape[1]/2)

cy = int(orig.shape[0]/2)
cx = int(orig.shape[1]/2)
mask = np.zeros(orig.shape)
cv2.ellipse(mask, (cx, cy), (rx, ry), 0, 0, 360, 1, -1)
plt.imshow(mask)
plt.show()

orig_fft = np.fft.fftshift(np.fft.fft2(orig))
noised_fft = np.fft.fftshift(np.fft.fft2(noised))
med_fft = np.fft.fftshift(np.fft.fft2(med))
meaned_fft = np.fft.fftshift(np.fft.fft2(meaned))
sigma_clip_fft = np.fft.fftshift(np.fft.fft2(sigma_clip))

fig, axs = plt.subplots(2, 3)
fig.patch.set_facecolor('#222222')
axs[0,0].imshow(np.log(abs(orig_fft)), cmap='gray')
axs[0,1].imshow(np.log(abs(noised_fft)), cmap='gray')
axs[1,0].imshow(np.log(abs(med_fft)), cmap='gray')
axs[1,1].imshow(np.log(abs(meaned_fft)), cmap='gray')
axs[1,2].imshow(np.log(abs(sigma_clip_fft)), cmap='gray')

plt.show()


orig_f = np.fft.ifft2(np.fft.ifftshift(orig_fft * mask))
noised_f = np.fft.ifft2(np.fft.ifftshift(noised_fft * mask))
med_f = np.fft.ifft2(np.fft.ifftshift(med_fft * mask))
meaned_f = np.fft.ifft2(np.fft.ifftshift(meaned_fft * mask))
sigma_clip_f = np.fft.ifft2(np.fft.ifftshift(sigma_clip_fft * mask))

fig, axs = plt.subplots(2, 3)
fig.patch.set_facecolor('#222222')
axs[0,0].imshow(np.log(abs(orig_f)), cmap='gray')
axs[0,1].imshow(np.log(abs(noised_f)), cmap='gray')
axs[1,0].imshow(np.log(abs(med_f)), cmap='gray')
axs[1,1].imshow(np.log(abs(meaned_f)), cmap='gray')
axs[1,2].imshow(np.log(abs(sigma_clip_f)), cmap='gray')

plt.show()


fig, axs = plt.subplots(2,3)
fig.patch.set_facecolor('#222222')
show_hist(orig, axs[0,0], 256)
show_hist(noised, axs[0,1], 256)
show_hist(med, axs[1,0], 256)
show_hist(meaned, axs[1,1], 256)
show_hist(sigma_clip, axs[1,2], 256)
plt.show()

print()
print("noised: ", SNR(orig, noised))
print("median: ", SNR(orig, med))
print("mean: ", SNR(orig, meaned))
print("kappa sigma: ", SNR(orig, sigma_clip))

