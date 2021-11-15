import matplotlib.pyplot as plt
from skimage import measure, data, color

# 生成二值测试图像
img = color.rgb2gray(data.horse())

print(img.shape)
# 检测所有图形的轮廓
contours = measure.find_contours(img, 0.5)
print(type(contours), len(contours))
# 绘制轮廓
fig, axes = plt.subplots(1, 3, figsize=(8, 8))
ax_original, ax0, ax1 = axes.ravel()
ax_original.imshow(data.horse())
ax_original.set_title('original')

ax0.imshow(img, plt.cm.gray)
ax0.set_title('original image')

rows, cols = img.shape
ax1.axis([0, rows, cols, 0])
for n, contour in enumerate(contours):
    ax1.plot(contour[:, 1], contour[:, 0], linewidth=2)
ax1.axis('image')
ax1.set_title('contours')
plt.show()
