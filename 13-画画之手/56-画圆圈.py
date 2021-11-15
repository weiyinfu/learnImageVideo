from mediapy import hand


def show():
    for img, point in hand.hands:
        print(img.shape, point)


# 画画之手生成视频
import numpy as np
import mediapy as mp

width = 1200
height = 1200
h, hand_pointer = hand.hands[0]

global_image = np.zeros((width, height, 4), dtype=np.uint8)

last = 0


def get_background(cx, cy, r, theta):
    global last
    ang = np.linspace(last, theta, 100)
    x = np.round(cx + r * np.cos(ang)).astype(np.int)
    y = np.round(cy + r * np.sin(ang)).astype(np.int)
    global_image[x, y, :] = 255
    last = theta
    return global_image.copy()


def get_image(theta):
    cx, cy = width // 2, height // 2
    r = min(width // 3, height // 3) - 10
    x, y = cx + r * np.cos(theta), cy + r * np.sin(theta)
    x, y = int(x), int(y)
    img = get_background(cx, cy, r, theta)
    draw_image(img, (x, y), h, hand_pointer)
    return img


def draw_image(big, big_pos, small, small_pos):
    # 将大图与小图按照big_pos和small_pos进行对齐然后画图
    bx, by = big_pos
    sx, sy = small_pos
    left_size = min(bx, sx)
    right_size = min(big.shape[0] - bx, small.shape[0] - sx)
    top_size = min(by, sy)
    bottom_size = min(big.shape[1] - by, small.shape[1] - sy)
    hand_sub = small[sx - left_size:sx + right_size, sy - top_size:sy + bottom_size, :]
    should = hand_sub[:, :, 3] > 0
    big[bx - left_size:bx + right_size, by - top_size:by + bottom_size][should] = hand_sub[should]


a = []

for i in range(1000):
    img = get_image(i * np.pi / 30)
    print(img.shape)
    a.append(img)
a = np.array(a)
a = a[:, :, :, :3]
print(a.shape, a.dtype)
mp.write('a.mp4', a, 5)
mp.play('a.mp4')
