import mediapy as mp
import time

filepath = '../imgs/taylor.mp4'
a = mp.open_media(filepath)
import pylab as plt

b = []
for i in range(5):
    img = a.reader.read(1)
    b.append(img[0])
fig, axes = plt.subplots(5, 1)
axes = axes.reshape(-1)
for img, ax in zip(b, axes):
    ax.imshow(img)
plt.show()
