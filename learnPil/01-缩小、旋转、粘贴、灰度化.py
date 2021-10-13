from PIL import Image
"""
给定一张图片，执行以下步骤：
1. 把图片缩小为原来的二分之一
2. 把图片中心1/3~2/3处旋转180度
3. 把图片灰度化
"""
img = Image.open("../imgs/1.jpg")
print(img.size, img.format, img.mode)
img.thumbnail((img.size[0] // 2, img.size[1] // 2))  # 将图片的长度和宽度缩小为原来的二分之一
rec = (img.size[0] // 3, img.size[1] // 3, img.size[0] * 2 // 3, img.size[1] * 2 // 3)
box = img.crop(rec)# 裁剪1/3-2/3处的矩形
box = box.transpose(Image.ROTATE_180)
img.paste(box, rec)
img = img.convert("1")
img.show()
