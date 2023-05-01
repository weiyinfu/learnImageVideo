"""
练习三维投影到二维。

先画远处的再画近处的，近处的会在一定程度上覆盖掉远处的。
"""

import numpy as np
import pylab as plt
from tqdm import tqdm

import mediapy as mp


def make_cube():
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
    faces = []
    for i in range(len(a)):
        for j in range(i):
            for k in range(j):
                for l in range(k):
                    good = False
                    for t in range(3):
                        if a[i][t] == a[j][t] == a[k][t] == a[l][t]:
                            good = True
                            break
                    if not good:
                        continue
                    face = [i, j, k, l]
                    face.sort(key=lambda x: np.linalg.norm(a[x] - a[i]))
                    face[-1], face[-2] = face[-2], face[-1]
                    faces.append(face)
    faces = np.array(faces)
    return a, edges, faces


points, edges, faces = make_cube()
print(len(faces), len(edges), len(points))
face_color = np.random.randint(0, 255, (6, 3))


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


def ball2rec(ps, rows, cols):
    p = ps / np.linalg.norm(ps, axis=1, keepdims=True)
    alpha = np.arccos(p[:, 2])
    beta = np.arctan2(p[:, 0], p[:, 1])
    tx = np.round(alpha / np.pi * rows) % rows
    ty = np.round(beta / np.pi * cols) % cols
    return tx, ty


def ball2rec_one(p, rows, cols):
    x, y = ball2rec(np.array([p]), rows, cols)
    return x[0], y[0]


def get_point_count(f, t, rows, cols):
    fp = ball2rec_one(f, rows, cols)
    tp = ball2rec_one(t, rows, cols)
    point_count = np.linalg.norm(np.array(fp) - np.array(tp))
    return int(point_count)


def line(f, t, rows, cols):
    # 三维空间中的直线(f,t)对应的真实图片上的坐标列表
    point_count = get_point_count(f, t, rows, cols)
    p = np.linspace(f, t, int(point_count))
    return ball2rec(p, rows, cols)


def get_face_points(A, B, C, D, rows, cols):
    point_count = get_point_count(A, B, rows, cols)
    fs = np.linspace(A, B, point_count)
    ts = np.linspace(D, C, point_count)
    ans = set()
    for f, t in zip(fs, ts):
        ps = line(f, t, rows, cols)
        for p in ps:
            ans.add((p[0], p[1]))
    ans = list(ans)
    xs = np.array([int(i[0]) for i in ans])
    ys = np.array([int(i[1]) for i in ans])
    return xs, ys


def draw_cube(cube):
    sz = 700
    img = np.zeros((sz, sz, 3), dtype=np.uint8)
    r = sz / 2 / np.sqrt(3) - 3
    a = np.round((cube + np.array([-3, 0, 0])) * r + sz // 2).astype(np.int32)
    # 按照各个面到点(0,0,3)的距离进行排序画图
    dis = np.mean(np.linalg.norm(cube[faces] - (0, 0, 3), axis=2), axis=1)
    ind = np.argsort(dis)
    ind = ind[::-1]  # 先画远处的，再画近处的
    for face, color in zip(faces[ind], face_color[ind]):
        # xy = draw.polygon(a[face, 0], a[face, 1])
        xy = get_face_points(a[face[0]], a[face[1]], a[face[2]], a[face[3]], sz, sz)
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


#
# def test_get_facepoinst():
#     get_face_points(())
#
main(True)
# test_get_facepoinst()
