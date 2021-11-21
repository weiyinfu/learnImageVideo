"""
练习三维投影到二维。
"""

import numpy as np
import pylab as plt
from skimage import draw

import mediapy as mp

"""
生成正方体的点、线、面
"""
a = []
for i in (-1, 1):
    for j in (-1, 1):
        for k in (-1, 1):
            a.append((i, j, k))
a = np.array(a)
edges = set()
for i in range(len(a)):
    for j in range(i):
        if np.linalg.norm(a[i] - a[j]) == 2:
            edges.add((j, i))
edges = np.array(list(edges))
print('边数，结点数', len(edges), len(a))


def to_polar(p):
    # 平面直角坐标系转极坐标系
    x, y, z = p
    r = np.linalg.norm(p)
    al = np.arctan2(y, x)
    th = np.arctan2(np.linalg.norm([x, y]), z)
    return r, al, th


def to_zhi(r, alpha, theta):
    # 极坐标系转平面直角坐标系
    return np.array([r * np.sin(theta) * np.cos(alpha), r * np.sin(theta) * np.sin(alpha), r * np.cos(theta)])


def turn(p, alpha, beta, theta):
    # 将点p绕x轴、y轴、z轴分别旋转alpha、beta、theta度
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
    # 旋转alpha，beta，theta度之后的正方体的每个点的坐标
    aa = np.array([turn(i, alpha, beta, theta) for i in a])
    return aa


def draw_cube(cube):
    # cube是一个点列表，把正方体画出来
    sz = 700
    img = np.zeros((sz, sz, 3), dtype=np.uint8)
    r = sz / 2 / np.sqrt(3) - 3
    aa = np.round(cube * r + sz // 2).astype(np.int)
    for f, t in edges:
        xy = draw.line(*aa[f][:2], *aa[t][:2])
        img[xy] = 255
    return img


def main(show=False):
    ang = np.zeros(3)
    a = []
    for i in range(1000):
        d = np.random.random(3) * np.pi / 100
        ang += d
        c = get_cube(*ang)
        img = draw_cube(c)
        a.append(img)
        if show:
            plt.imshow(img, cmap=plt.cm.gray)
            plt.show()
    a = np.array(a)
    mp.write('a.mp4', a, rate=20)


def test_polar_zhi():
    p = np.random.random(3)
    pp = to_polar(p)
    print(p)
    print(to_zhi(*pp))


def test_cube():
    c = get_cube(1, 1, 1)
    for f, t in edges:
        print(np.linalg.norm(c[f] - c[t]))


main()
# test_cube()
