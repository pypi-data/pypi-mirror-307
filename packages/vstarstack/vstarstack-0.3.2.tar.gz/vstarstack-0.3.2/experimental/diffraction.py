F=420e-3
l1=405e-9
l2=900e-9
a=0.1e-3
pix=3.8e-6

x1=l1*F/a
x2=l2*F/a
n1 = x1/pix
n2 = x2/pix

N = int(n2-n1)

print(f"Spectrum width from {l1*1e9} to {l2*1e9} nm = {N} pixels")
print(f"{(l2-l1)*1e9/N} nm/pix")
