from skimage import filters, data, viewer, io, color
import matplotlib.pyplot as plt

"""
sobel算子只能处理二维数组（即只能直接处理灰度图）
"""
coins = data.coins()
img = color.rgb2gray(io.imread("haha.jpg"))
viewer.CollectionViewer([coins, filters.sobel(coins), img, filters.sobel(img)]).show()
