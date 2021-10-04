from skimage import data, viewer, feature
from scipy import ndimage
import numpy as np

img = data.coins()
edges = feature.canny(img / 255.)
mask = ndimage.binary_fill_holes(edges)
labels, label_count = ndimage.label(mask)
sizes = np.bincount(labels.ravel())
mask = np.logical_and(sizes > 20, sizes < 5000)[labels]
viewer.CollectionViewer([mask, img]).show()
