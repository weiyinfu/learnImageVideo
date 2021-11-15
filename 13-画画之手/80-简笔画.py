import numpy as np
import pylab as plt
import skimage.io as io
from tqdm import tqdm

import mediapy as mp
from mediapy import hand

boy = io.imread("../imgs/简笔画/boy.jpg")
girl = io.imread("../imgs/简笔画/girl.jpg")
pen_width = 3
pos = np.argwhere(np.mean(boy, axis=2)[:, :, ] < 125)
xs, ys = pos[:, 0], pos[:, 1]
print(boy.shape, boy.dtype)
img = np.ones(boy.shape, boy.dtype) * 255


def analyze(xs, ys):
    """
    ge
    :param xs:
    :param ys:
    :return:
    """
    # 分析得到一个point_list
    a = list(zip(xs, ys))
    a.sort()
    a = np.array(a)
    q = [0]
    visited = np.zeros(len(a), dtype=np.bool)
    visited[0] = True
    for i in tqdm(range(len(a)-1), desc='构图'):
        not_visited = np.logical_not(visited)
        ind = np.argwhere(not_visited).reshape(-1)
        dis = np.linalg.norm(a[not_visited] - a[q[-1]], axis=1)
        which = np.argmin(dis)
        q.append(ind[which])
        visited[ind[which]] = True
    a = a[q]
    return a


hand_image, hand_pointer = hand.hands[0]


def draw(point_list):
    a = []
    batch_size = 10
    for i in tqdm(range(0, len(point_list), batch_size), desc='绘图中'):
        for x, y in point_list[i:i + batch_size]:
            fx, tx = x - 1, x + 1
            fy, ty = y - 1, y + 1
            fx, tx = np.clip([fx, tx], 0, img.shape[0])
            fy, ty = np.clip([fy, ty], 0, img.shape[1])
            img[fx:tx, fy:ty] = boy[fx:tx, fy:ty]
        im = img.copy()
        # print(im.shape, hand_image.shape)
        x, y = point_list[i]
        hand.draw_image(im, (x, y), hand_image, hand_pointer)
        a.append(im)
    for i in range(100):
        a.append(img)
    a = np.array(a)
    return a


point_list = hand.analyze_point_sequence(xs, ys)
a = draw(point_list)


def show():
    plt.imshow(boy)
    plt.show()


mp.write('a.mp4', a, 25)
mp.play('a.mp4')
