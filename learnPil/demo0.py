from PIL import Image

img = Image.open("haha.jpg")
print(img.size, img.format, img.mode)
img.thumbnail((img.size[0] // 2, img.size[1] // 2))
rec=(img.size[0] // 3, img.size[1] // 3, img.size[0] * 2 // 3, img.size[1] * 2 // 3)
box = img.crop(rec)
box=box.transpose(Image.ROTATE_180)
img.paste(box,rec)
img=img.convert("1")
img.show()
