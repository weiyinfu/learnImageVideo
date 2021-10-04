from skimage import feature, data, viewer, filters, morphology
import numpy as np
import scipy.ndimage as ndi

img = data.coins()
elevation_map = filters.sobel(img)
markers = np.zeros_like(img)
markers[img < 30] = 1
markers[img > 150] = 2
segmentation = morphology.watershed(elevation_map, markers)
segmentation = ndi.binary_fill_holes(segmentation - 1)
labels, label_cnt = ndi.label(segmentation)
viewer.CollectionViewer([elevation_map, segmentation]).show()
