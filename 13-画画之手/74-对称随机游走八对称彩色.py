from mediapy import hand


def show():
    for img, point in hand.hands:
        print(img.shape, point)


# 画画之手生成视频
import numpy as np
import mediapy as mp

width = 700
height = 700
h, hand_pointer = hand.hands[0]

global_image = np.zeros((width, height, 4), dtype=np.uint8)

last = (width // 2, height // 2, np.random.randint(0, 255, 3))


def get_background(x, y, color):
    if len(color) == 3:
        color = (*color, 255)
    global last
    xx = np.round(np.linspace(last[0], x, 100)).astype(np.int)
    yy = np.round(np.linspace(last[1], y, 100)).astype(np.int)
    cx, cy = width // 2 - 1, height // 2 - 1
    xx[xx >= cx] = (cx * 2 - xx)[xx >= cx]
    yy[yy >= cy] = (cy * 2 - yy)[yy >= cy]
    global_image[xx, yy, :] = color
    global_image[cx * 2 - xx, cy * 2 - yy] = color
    global_image[xx, cy * 2 - yy] = color
    global_image[cx * 2 - xx, yy] = color
    global_image[yy, xx, :] = color
    global_image[cy * 2 - yy, cx * 2 - xx, :] = color
    global_image[cy * 2 - yy, xx, :] = color
    global_image[yy, cx * 2 - xx, :] = color
    last = (x, y, color)
    return global_image.copy()


def get_next_color(color):
    r = 10
    alpha, beta = np.random.random(2) * np.pi * 2
    x, y, z = color[:3]
    dx, dy, dz = r * np.cos(alpha), r * np.sin(alpha) * np.sin(beta), r * np.sin(alpha) * np.cos(beta)
    a = x + dx, y + dy, z + dz
    a = [np.clip(i, 0, 255) for i in a]
    return a


def get_image():
    r = 20
    cx, cy, last_color = last
    theta = np.random.random() * np.pi * 2
    x, y = cx + r * np.cos(theta), cy + r * np.sin(theta)
    x, y = np.clip(x, 0, width - 1), np.clip(y, 0, height - 1)
    x, y = int(x), int(y)
    img = get_background(x, y, get_next_color(last_color))
    draw_image(img, (x, y), h,hand_pointer)
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
    img = get_image()
    a.append(img)
a = np.array(a)
a = a[:, :, :, :3]
print(a.shape, a.dtype)
mp.write('a.mp4', a, 20)
mp.play('a.mp4')
