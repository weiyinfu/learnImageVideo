"""
练习三维投影到二维。
"""

import numpy as np
import pylab as plt
from skimage import draw
from tqdm import tqdm

import mediapy as mp


def shier():
    # 正十二面体
    a = []
    for i in (-1, 1):
        for j in (-1, 1):
            for k in (-1, 1):
                a.append((i, j, k))
    phi = (1 + 5 ** 0.5) / 2
    for i in (phi, -phi):
        for j in (1 / phi, -1 / phi):
            a.append((i, j, 0))
            a.append((j, 0, i))
            a.append((0, i, j))
    return np.array(a)


def ershi():
    # 正二十面体
    a = []
    phi = (1 + 5 ** 0.5) / 2
    for j in (1, -1):
        for p in (phi, -phi):
            a.append((0, j, p))
            a.append((j, p, 0))
            a.append((p, 0, j))
    return np.array(a)


def eight():
    a = []
    for i in (1, 0, -1):
        for j in (1, 0, -1):
            for k in (1, 0, -1):
                if np.sum(np.abs([i, j, k])) == 1:
                    a.append((i, j, k))
    return np.array(a)


def six():
    a = []
    for i in (1, -1):
        for j in (1, -1):
            for k in (1, -1):
                a.append((i, j, k))
    return np.array(a)


def four():
    a = []
    for i in (1, -1):
        a.append((i, 0, -1 / (2 ** 0.5)))
        a.append((0, i, 1 / (2 ** 0.5)))
    return np.array(a)


cube_func = [four, six, eight, shier, ershi]


class Cube:
    def __init__(self, points: np.ndarray, edges: np.ndarray, faces: np.ndarray):
        self.points = points
        self.edges = edges
        self.faces = faces

    def show(self):
        print('面边点', len(self.faces), len(self.edges), len(self.points))
        for f, t in self.edges:
            # print('边长', np.linalg.norm(self.points[f] - self.points[t]))
            pass


def point2face(p, face):
    # 点p到面face的距离
    abc = np.linalg.solve(face[:3], [1, 1, 1])
    dis = (np.dot(abc, p) - 1) / np.linalg.norm(abc)
    return np.abs(dis)


def sort_points(a):
    # 对组成n边形的结点进行排序，这些结点共面，如果不排序，这个面的点就是无序的
    q = [0]
    vis = np.zeros(len(a), dtype=np.bool)
    vis[0] = True
    while len(q) < len(a):
        unvis = np.logical_not(vis)
        ind = np.argwhere(unvis).reshape(-1)
        dis = np.linalg.norm(a[unvis] - a[q[-1]], axis=1)
        x = ind[np.argmin(dis)]
        q.append(x)
        vis[x] = True
    return q


def make_cube(ind):
    # 要求以原点为中心，球的半径为1
    a = np.array(cube_func[ind]())
    a = a - np.mean(a, axis=0)
    a = a / np.linalg.norm(a[0])
    # 根据边的距离选择边，只选择那些很短的边，这些短边才是正n面体真正的边
    edges = []
    for i in range(len(a)):
        for j in range(i):
            edges.append((i, j))
    edges = np.array(edges)
    dis = np.linalg.norm(a[edges[:, 0]] - a[edges[:, 1]], axis=1)
    ind = np.argsort(dis)
    dis = dis[ind]
    edges = edges[ind]
    ind = np.searchsorted(dis, dis[0] + 1e-4)
    edges = edges[:ind]
    # 求面：首先确定基本面，然后根据基本面寻找面上的点，最后对面集合进行去重
    faces = []
    for i in range(len(edges)):
        for j in range(i):
            point_set = {*edges[i], *edges[j]}
            if len(point_set) == 3:  # 两条边有公共点才行
                point_list = list(point_set)
                if np.linalg.matrix_rank(a[point_list]) != 3:
                    # 正八面体的情况，可能导致选点错误
                    continue
                # 记录三角形的周长，优先选择那些三角形周长短的面
                cir = np.linalg.norm(a[point_list[0]] - a[point_list[1]]) + np.linalg.norm(a[point_list[2]] - a[point_list[1]]) + np.linalg.norm(a[point_list[0]] - a[point_list[2]])
                faces.append((point_list, cir))
    faces.sort(key=lambda x: x[1])  # 将面按照周长进行排序
    ind = len(faces)
    for i in range(1, len(faces)):
        if faces[i][1] > faces[0][1] + 1e-2:
            ind = i
            break
    faces = [i[0] for i in faces[:ind]]  # 去掉周长太长的面
    # 为每个面扩张点
    for face in faces:
        for ind, p in enumerate(a):
            if point2face(p, a[face]) < 1e-4:
                if ind not in face:
                    face.append(ind)
    # 对面进行去重
    uniq_faces = [sorted(face) for face in faces]
    uniq_faces.sort()
    faces = []
    for i in uniq_faces:
        if len(faces) and faces[-1] == i:
            continue
        faces.append(i)
    # face的边的顺序必须正确，否则涂颜色的时候会出现折线
    reorg_faces = []
    for face in faces:
        reorg_faces.append(np.array(face)[sort_points(a[face])])
    faces = reorg_faces
    a = np.array(a)
    edges = np.array(edges)
    faces = np.array(faces)
    return Cube(points=a, edges=edges, faces=faces)


CUBES = [make_cube(i) for i in range(len(cube_func))]
face_color = np.random.randint(0, 255, (25, 3))
for i in CUBES:
    i.show()


def turn(p, alpha, beta, theta):
    # 旋转一个点
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


def get_cube(c: Cube, alpha, beta, theta):
    aa = np.array([turn(i, alpha, beta, theta) for i in c.points])
    return Cube(points=aa, edges=c.edges, faces=c.faces)


def draw_cube(cube: Cube, sz: int):
    img = np.zeros((sz, sz, 3), dtype=np.uint8)
    radius = np.max(np.linalg.norm(cube.points, axis=1))  # 半径
    a = np.round(cube.points / radius * sz / 2 + sz / 2).astype(np.int)
    # 按照各个面到点(0,0,3)的距离进行排序画图
    dis = np.mean(np.linalg.norm(cube.points[cube.faces] - (0, 0, 3), axis=2), axis=1)
    ind = np.argsort(dis)
    ind = ind[::-1]  # 先画远处的，再画近处的
    opacity = 0.7
    for face, color in zip(cube.faces[ind], face_color[ind]):
        xy = draw.polygon(a[face, 0], a[face, 1])
        img[xy] = np.round(color * opacity + img[xy] * (1 - opacity)).astype(np.uint8)
    return img


def get_rotate_delta(image_count: int):
    # 让随机旋转的角度变得平滑一些
    dd = np.random.random((image_count + 20, 3)) * np.pi / 100
    ddd = []
    for i in range(4, image_count + 4):
        ddd.append(np.mean(dd[i - 4:i + 4], axis=0))
    ddd = np.array(ddd)
    return ddd


def main(show=False, show_which=-1):
    a = []
    image_count = 1000
    image_size = 900
    ang = np.zeros(3)
    # 五个图形的中心位置
    position = [
        (image_size / 4, image_size / 4),
        (image_size / 4, image_size / 4 * 3),
        (image_size / 4 * 3, image_size / 6 * 1),
        (image_size / 4 * 3, image_size / 6 * 3),
        (image_size / 4 * 3, image_size / 6 * 5),
    ]
    position = np.array(position, dtype=np.int)
    ddd = get_rotate_delta(image_count)
    for i in tqdm(range(image_count)):
        d = ddd[i]
        ang += d
        big_image = np.zeros((image_size, image_size, 3), dtype=np.uint8)
        if show_which == -1:
            for j in range(len(CUBES)):
                c = get_cube(CUBES[j], *ang)
                img = draw_cube(c, int(image_size / 7 * 2))
                x, y = position[j]
                target_shape = np.array(img.shape[:2]) // 2 * 2
                big_image[x - img.shape[0] // 2:x + img.shape[0] // 2, y - img.shape[1] // 2:y + img.shape[1] // 2] = img[:target_shape[0], :target_shape[1]]
        else:
            c = get_cube(CUBES[show_which], *ang)
            img = draw_cube(c, image_size)
            big_image = img
        a.append(big_image)
        if show:
            plt.imshow(big_image, cmap=plt.cm.gray)
            plt.show()
    a = np.array(a)
    mp.write('a.mp4', a, rate=30)
    mp.play('a.mp4')


# main(show=False, show_which=4)
# for i in CUBES:
#     print(i.edges.tolist(), len(i.faces))
