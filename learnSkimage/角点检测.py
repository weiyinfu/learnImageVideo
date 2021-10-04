from skimage import feature,data,viewer,io
img=data.coins()
res=feature.corner_fast(img)
io.imshow(res)
io.show()