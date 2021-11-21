"""
练习三维投影到二维。

彩色透明八面体
"""

import numpy as np
import pylab as plt
from skimage import draw
from tqdm import tqdm

import mediapy as mp


def make_cube():
    a = [[-1, 0, 0], [0, -1, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [0, 0, -1]]
    edges = []
    for i in range(4):
        for j in (4, 5):
            edges.append((i, j))
    faces = []
    for i in (4, 5):
        for j in range(4):
            faces.append((i, j, (j + 1) % 4))
    a = np.array(a)
    edges = np.array(edges)
    faces = np.array(faces)
    return a, edges, faces


points, edges, faces = make_cube()
print(len(faces), len(edges), len(points))
face_color = np.random.randint(0, 255, (len(faces), 3))
for f, t in edges:
    print('边长', np.linalg.norm(points[f] - points[t]))


def turn(p, alpha, beta, theta):
    rx = [[1, 0, 0],
          [0, np.cos(alpha), np.sin(alpha)],
          [0, -np.sin(alpha), np.cos(alpha)],
          ]
    ry = [[np.cos(beta), 0, -np.sin(beta)],
          [0, 1, 0],
          [np.sin(beta), 0, np.cos(beta)],
          ]
    rz = [[np.cos(theta), np.sin(theta), 0],
          [-np.sin(theta), np.cos(theta), 0],
          [0, 0, 1]
          ]
    r = np.matmul(np.matmul(rx, ry), rz)
    return np.dot(p, r)


def get_cube(alpha, beta, theta):
    aa = np.array([turn(i, alpha, beta, theta) for i in points])
    return aa


def draw_cube(cube):
    sz = 700
    img = np.zeros((sz, sz, 3), dtype=np.uint8)
    center = np.mean(points, axis=0)  # 体心
    radius = np.max(np.linalg.norm(points - center, axis=1))  # 半径
    a = np.round(cube / radius * sz / 2 + sz / 2).astype(np.int)
    # 按照各个面到点(0,0,3)的距离进行排序画图
    dis = np.mean(np.linalg.norm(cube[faces] - (0, 0, 3), axis=2), axis=1)
    ind = np.argsort(dis)
    ind = ind[::-1]  # 先画远处的，再画近处的
    for face, color in zip(faces[ind], face_color[ind]):
        xy = draw.polygon(a[face, 0], a[face, 1])
        img[xy] = np.round(color * 0.9 + img[xy] * 0.1).astype(np.uint8)
    return img


def main(show=False):
    ang = np.zeros(3)
    a = []
    img_count = 1000
    # 让随机旋转的角度变得平滑一些
    dd = np.random.random((img_count + 20, 3)) * np.pi / 100
    ddd = []
    for i in range(4, img_count + 4):
        ddd.append(np.mean(dd[i - 4:i + 4], axis=0))
    ddd = np.array(ddd)
    for i in tqdm(range(img_count)):
        d = ddd[i]
        ang += d
        c = get_cube(*ang)
        img = draw_cube(c)
        a.append(img)
        if show:
            plt.imshow(img, cmap=plt.cm.gray)
            plt.show()
    a = np.array(a)
    mp.write('a.mp4', a, rate=30)
    mp.play('a.mp4')


main()
# make_cube()
