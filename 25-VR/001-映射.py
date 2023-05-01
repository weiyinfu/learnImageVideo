import numpy as np
import pylab as plt

"""
球面坐标、真实坐标的相互转换
"""


def ball2rec(x, y, z, rows, cols):
    p = np.array([x, y, z], dtype=np.float32)
    p /= np.linalg.norm(p)
    alpha = np.arccos(p[2])
    beta = np.arctan2(x, y)
    tx = np.round(alpha / np.pi * rows) % rows
    ty = np.round(beta / np.pi * cols) % cols
    print(f"ball2rec alpha={np.rad2deg(alpha)} beta={np.rad2deg(beta)}")
    return tx, ty


def rec2ball(x, y, rows, cols):
    alpha = x / rows * np.pi
    beta = y / cols * np.pi
    print("rec2ball:纬度", np.rad2deg(alpha), "经度", np.rad2deg(beta))
    ball_z = np.cos(alpha)
    ball_x = np.sin(alpha) * np.sin(beta)
    ball_y = np.sin(alpha) * np.cos(beta)
    return ball_x, ball_y, ball_z


def main():
    points = np.ones((20, 20, 3), dtype=np.uint8)
    points[:, :, 0] = 250
    z = -5
    scale = 0.02
    target = np.zeros((100, 100, 3))

    for i in range(points.shape[0]):
        for j in range(points.shape[1]):
            k = z
            p = np.array([i * scale, j * scale, k])
            p /= np.linalg.norm(p)
            x = np.arccos(p[2]) / np.pi * target.shape[0]
            y = np.arccos(-p[0]) / np.pi * target.shape[1]
            target[x][y] = points[i][j]
    plt.imshow(target)
    plt.show()


def test_convert():
    # 因为0,5这种点对应球面的极点（0,0），所以不可避免在两极处是错的
    rows, cols = 10, 10
    right = 0
    for i in range(rows):
        for j in range(cols):
            x, y, z = rec2ball(i, j, rows, cols)
            ii, jj = ball2rec(x, y, z, rows, cols)
            if (i, j) == (ii, jj):
                right += 1
            else:
                print(f'bad ({i},{j}) ({ii},{jj})')
    print(right / (rows * cols))


def test_one():
    rows, cols = 10, 10
    x, y, z = rec2ball(5, 5, rows, cols)  # should be 0,0,1
    print(x, y, z)
    xx, yy = ball2rec(x, y, z, rows, cols)
    print(xx, yy)


if __name__ == '__main__':
    test_convert()
    # test_one()
