# 画画之手生成视频
import numpy as np

import mediapy as mp
from mediapy import hand

sz = 40
width = sz * (8 + 2)
height = sz * (9 + 2)
h, hand_pointer = hand.hands[0]

global_image = np.zeros((height, width, 4), dtype=np.uint8)
global_image[:, :] = 255


def get_background(fx, fy, tx, ty):
    img = global_image
    fx, fy, tx, ty = [int(i) for i in (fx, fy, tx, ty)]
    x, y = np.linspace(fx, tx, 100), np.linspace(fy, ty, 100)
    x = np.round(np.clip(x, 0, width)).astype(np.int32)
    y = np.round(np.clip(y, 0, height)).astype(np.int32)
    img[x, y, :] = 0
    img[x + 1, y + 1, :] = 0
    img = img.copy()
    draw_image(img, (tx, ty), h, hand_pointer)
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


def draw_line(fx, fy, tx, ty):
    print(fx, fy, tx, ty)
    point_count = int(np.round(np.hypot(tx - fx, ty - fy) / sz * 4))
    x = np.linspace(fx, tx, point_count)
    y = np.linspace(fy, ty, point_count)
    for i in range(1, len(x)):
        img = get_background(x[i - 1], y[i - 1], x[i], y[i])
        a.append(img)


def main():
    for i in range(10):
        draw_line(i * sz + sz, sz, i * sz + sz, width - sz)
    for i in range(9):
        if i in (0, 8):
            draw_line(sz, i * sz + sz, height - sz, i * sz + sz)
        else:
            draw_line(sz, i * sz + sz, 5 * sz, i * sz + sz)
            draw_line(sz * 6, i * sz + sz, 10 * sz, i * sz + sz)
    draw_line(sz, 4 * sz, sz * 3, 6 * sz)
    draw_line(sz, 6 * sz, sz * 3, 4 * sz)
    draw_line(height - sz, 4 * sz, height - sz * 3, 6 * sz)
    draw_line(height - sz, 6 * sz, height - sz * 3, 4 * sz)
    for i in range(100):
        a.append(global_image.copy())


main()
a = np.array(a)
a = a[:, :, :, :3]
print(a.shape, a.dtype)
mp.write('a.mp4', a, 20)
mp.play('a.mp4')
