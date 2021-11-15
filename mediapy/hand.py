import os

import numpy as np
from skimage import color, filters, measure
from skimage import io
from tqdm import tqdm


def get_hands():
    pen_point = {
        'hand10': (87, 124),
        'hand11': (206, 161),
        'hand6': (264, 148),
        'hand9': (191, 215),
        'hand8': (35, 249),
        'hand2': (10, 40),
        'hand1': (69, 35),
        'hand5': (174, 6),
        'hand4': (47, 61),
        'hand7': (98, 189),
    }

    hand_folder = "../imgs/hand"
    image_list = []
    for i in os.listdir(hand_folder):
        img = io.imread(f"../imgs/hand/{i}")
        im = np.zeros(shape=(*img.shape[:2], 4), dtype=img.dtype)
        im[:, :, 3] = 255
        im[:, :, :3] = img
        mean = np.mean(img, axis=2)
        sigma = np.std(img, axis=2)
        ind = np.logical_and(mean > 200, sigma < 3)
        im[ind] = 0
        pointer = pen_point[i[:i.index('.')]]
        image_list.append((im, (pointer[1], pointer[0])))
    return image_list


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
    depth = big.shape[2]
    big[bx - left_size:bx + right_size, by - top_size:by + bottom_size][should] = hand_sub[:, :, :depth][should]


def analyze_point_sequence(xs, ys):
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
    for i in tqdm(range(len(a) - 1), desc='构图'):
        not_visited = np.logical_not(visited)
        ind = np.argwhere(not_visited).reshape(-1)
        dis = np.linalg.norm(a[not_visited] - a[q[-1]], axis=1)
        which = np.argmin(dis)
        q.append(ind[which])
        visited[ind[which]] = True
    a = a[q]
    return a


def analyze_point_sequence_far(xs, ys):
    """
    尽量往远处走，会导致笔顺不够连续
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
    for i in tqdm(range(len(a) - 1), desc='构图'):
        not_visited = np.logical_not(visited)
        ind = np.argwhere(not_visited).reshape(-1)
        dis = np.linalg.norm(a[not_visited] - a[q[-1]], axis=1)
        # 寻找到第一个点距离近且到第二个点距离尽量远的点，这样做的目的是减少局部涂抹，尽量往远处走
        if len(q) >= 2:
            dis2last = np.linalg.norm(a[not_visited] - a[q[-2]], axis=1)
        else:
            dis2last = np.zeros_like(dis)
        which = np.lexsort((-dis2last, dis))[0]
        q.append(ind[which])
        visited[ind[which]] = True
    a = a[q]
    return a


def draw_point_list(img, point_list, hand_image, hand_pointer, silent_count=100, batch_size=10):
    if len(img.shape) != 3:
        raise Exception("图片深度应该为3")
    if img.dtype != np.uint8:
        raise Exception("图片类型应该为uint8")
    a = []
    paper = np.ones_like(img)
    paper[:] = 255
    for i in tqdm(range(0, len(point_list), batch_size), desc='绘图中'):
        for x, y in point_list[i:i + batch_size]:
            fx, tx = x - 1, x + 1
            fy, ty = y - 1, y + 1
            fx, tx = np.clip([fx, tx], 0, paper.shape[0])
            fy, ty = np.clip([fy, ty], 0, paper.shape[1])
            paper[fx:tx, fy:ty] = img[fx:tx, fy:ty]
        im = paper.copy()
        x, y = point_list[i]
        draw_image(im, (x, y), hand_image, hand_pointer)
        a.append(im)
    for i in range(silent_count):
        a.append(paper)
    a = np.array(a)
    return a


def generate_simple_image(img):
    grey_img = color.rgb2grey(img)
    img = filters.sobel(grey_img)
    edges = measure.find_contours(grey_img, 0.5)
    for edge in edges:
        x, y = edge[:, 0].astype(np.int), edge[:, 1].astype(np.int)
        for xx, yy in zip(x, y):
            if img[xx, yy] > 0.9:
                continue
            img[xx, yy] = 0.9
    img = color.grey2rgb(1 - img)
    img = np.round(img * 255).astype(np.uint8)
    # from skimage import exposure
    # img = exposure.equalize_hist(img)
    # img[img > 250] = 255
    # img[img <= 250] = 0
    return img


hands = get_hands()
