from math import *

from PIL import Image

img = Image.open("../beauty/0.jpg")
theta = pi / 4


def f2(img, theta):
    r = img.width / 2 / tan(theta / 2)
    ans = Image.new(img.mode, size=(int(r * theta), img.height))
    max_x = 0
    min_x = 1234
    for i in range(0, img.width):
        for j in range(0, img.height):
            alpha = atan((i - img.width / 2) / r)
            x = r * (theta / 2 - alpha)
            y = img.height / 2 + (j - img.height / 2) * cos(alpha)
            if x >= 0 and y >= 0 and x < ans.width and y < ans.height:
                ans.putpixel((int(x), int(y)), img.getpixel((i, j)))
    ans.show()
    ans.save("haha.jpg")
    print(max_x, min_x, ans.width)


def f1(img, theta):
    r = img.width / 2 / tan(theta / 2)
    ans = Image.new(img.mode, size=(int(r * sin(theta / 2) * 2), img.height))
    max_x = 0
    max_y = 0
    for i in range(0, img.width):
        for j in range(0, img.height):
            k = hypot(r, img.width / 2 - i)
            x = r * sin(theta / 2) + r * sin(atan((i - img.width / 2) / r))
            y = img.height / 2 + r * (j - img.height / 2) / k;
            if x >= 0 and y >= 0 and x < ans.width and y < ans.height:
                max_x = max(max_x, x)
                max_y = max(max_y, y)
                ans.putpixel((int(x), int(y)), img.getpixel((i, j)))
    ans.show()
    print(ans.width, max_x)
    print(ans.height, max_y)
    ans.save("haha.jpg")


f2(img, theta)
