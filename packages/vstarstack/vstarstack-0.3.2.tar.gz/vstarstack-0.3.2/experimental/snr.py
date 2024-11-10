M=14.0
Msky=19.0
pix=3.8
npix=16
D=70
F=420
bin=1
snr=2
qe=0.8
filter=0.3
n_dark=0.2
star_reduce=2

def photons(mag):
  N0=1e6/2
  return N0/10**(mag/2.5)

import math
s=math.pi*(D/10)**2/4
a_pix = pix*bin*1e-3/F*180/math.pi*3600

n_sky=photons(Msky)*s*npix*(a_pix)**2*qe*filter
n_star=photons(M)*s*qe*filter/star_reduce
n_dark=n_dark*npix
print(f"{n_sky:.2f}, {n_dark:.2f}, {n_star:.2f}")

snr1=(n_star)/(n_star+n_sky+n_dark)**0.5
print(f"snr 1 sec: {snr1:.2f}")

t=snr**2 * (n_star+n_sky+n_dark)/n_star**2

print(f"{t:.3f} sec")
