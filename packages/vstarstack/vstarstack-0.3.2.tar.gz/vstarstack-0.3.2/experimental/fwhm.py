import vstarstack.library.data
import vstarstack.library.stars.detect
import matplotlib.pyplot as plt
import numpy as np

def get_profile(image):
    y = int(image.shape[0]/2)
    x = int(image.shape[1]/2)
    profile1 = image[y,:]
    profile2 = image[:,x]
    return (profile1 + profile2)/2

def get_star(image, x, y, r):
    w = image.shape[1]
    h = image.shape[0]
    x1 = x - r
    x2 = x + r + 1
    y1 = y - r
    y2 = y + r + 1
    if x < r or y < r:
        return None
    if x > w-r-1 or y > h-r-1:
        return None
    return image[y1:y2, x1:x2]

def interpolate(v1, v2, v):
    return (v - v1)/(v2-v1)

def get_width2(profile):
    size = profile.shape[0]
    part = int(size/8)
    left = profile[0:part]
    right = profile[size-part-1:size-1]
    background = np.median(list(left) + list(right))
    noback = profile - background

    maxv = np.amax(noback)
    center = int(size/2)
    for i in range(size):
        if noback[i] > noback[center]:
            center = i
    x1 = center
    while True:
        val = noback[x1]
        if val <= maxv/2:
            break
        x1 -= 1
        if x1 == 0:
            break

    x2 = center
    while True:
        val = noback[x2]
        if val <= maxv/2:
            break
        x2 += 1
        if x2 == size-1:
            break

    vl1 = noback[x1]
    vl2 = noback[x1+1]

    vr1 = noback[x2]
    vr2 = noback[x2-1]

    d = interpolate(vl1, vl2, maxv/2)
    x1 += d
    
    d = interpolate(vr1, vr2, maxv/2)
    x2 -= d

    return x2 - x1
    

df = vstarstack.library.data.DataFrame.load("example.zip")

image,_ = df.get_channel("B")

vstarstack.library.stars.detect.configure_detector(thresh_coeff=1.2)
stars = vstarstack.library.stars.detect.detect_stars(image)
print("Stars: %i" % len(stars))

widths = []
maxv = np.amax(image)
for star in stars:
    #print(star)
    r = int(star["radius"])
    si = get_star(image, star["x"], star["y"], r*8+1)
    if si is None:
        continue
    if np.amax(si) == maxv:
        continue
    profile = get_profile(si)
    width = get_width2(profile)
    print("r = %i, width = %i" % (r, width))
    widths.append(width)
    #plt.grid(True)
    #plt.plot(profile)
    #plt.show()
    
print(np.median(widths))
