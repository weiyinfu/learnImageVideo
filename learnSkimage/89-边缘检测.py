import matplotlib.pyplot as plt

from skimage.data import camera
from skimage.filters import roberts, sobel, scharr, prewitt

image = camera()
edge_roberts = roberts(image)
edge_sobel = sobel(image)
edge_scharr = scharr(image)
edge_prewitt = prewitt(image)

fig, ax = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True,
                       figsize=(8, 4))

ax[0, 0].imshow(edge_roberts, cmap=plt.cm.gray)
ax[0, 0].set_title('Roberts Edge Detection')
ax[0, 0].axis('off')

ax[0, 1].imshow(edge_sobel, cmap=plt.cm.gray)
ax[0, 1].set_title('Sobel Edge Detection')
ax[0, 1].axis('off')

ax[1, 0].imshow(edge_scharr, cmap=plt.cm.gray)
ax[1, 0].set_title('Scharr Edge Detection')
ax[1, 0].axis('off')

ax[1, 1].imshow(edge_prewitt, cmap=plt.cm.gray)
ax[1, 1].set_title('Prewitt Edge Detection')
ax[1, 1].axis('off')

plt.tight_layout()
plt.show()
