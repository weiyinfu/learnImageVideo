from PIL import Image
import os

imgs = []
xsize = 0
print(type(os.listdir()))
for i in sorted(os.listdir("全景图")):
    print(i)
    img = Image.open("全景图/" + i)
    imgs.append(img)
    xsize += img.size[0]
print(xsize, imgs[0].size[1])
a = Image.new(imgs[0].mode, (xsize, imgs[0].size[1]))
xsize = 0
for i in imgs:
    print(imgs.index(i), i.size)
    a.paste(i, (xsize, 0, xsize + i.size[0], 0 + i.size[1]))
    xsize += i.size[0]
a.thumbnail((a.size[0] // 2, a.size[1] // 2))
a.save("haha.jpg")
