from PIL import Image

folder = "../zijing"
import os

files = list(os.listdir(folder))
# files.sort(key=lambda  x:os.stat(folder+"/"+x).st_ctime)
files.sort(key=lambda x: int(x[:x.index('.')]))
print(files)
cnt = 0
for i in files:
    print(i)
    img = Image.open("{}/{}".format(folder, i))
    w = 400
    img.thumbnail(size=(w, w * img.height / img.width))
    img.save("{}.jpg".format(cnt))
    cnt += 1
