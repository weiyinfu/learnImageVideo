import io

import numpy as np
import pylab as plt
from PIL import Image
from tqdm import tqdm

import mediapy as mp

fig = plt.figure(figsize=(3, 3))
x, y = 0, 2  # 小球的位置
v = 0  # 小球的速度
plt.plot([-1, 1], (-0.25, -0.25))  # 画一条地平线
dt = 0.1  # 每个间隔的时间
g = 1  # 重力系数


def get_frame(frame_index):
    global y, v
    if y < 1e-3 and v < 1e-3:
        return
    plt.cla()
    plt.axis('off')
    plt.xlim(-1, 1)
    plt.ylim(-0.5, 2.5)
    plt.plot([-1, 1], (-0.25, -0.25))  # 画一条地平线
    need_time = ((v * v + 2 * g) ** 0.5 - v) / g  # 到落地需要的时间
    need_time = min(abs(need_time), dt)
    left_time = dt - need_time  # 转向需要的时间
    vv = v - g * need_time
    y += (vv + v) / 2 * need_time
    v = vv
    if y <= 1e-7:
        v *= -0.91
        y += v * left_time
    plt.scatter(x, y, s=500)  # 把小球画出来
    cout = io.BytesIO()
    fig.canvas.print_png(cout)
    a = np.array(Image.open(cout))
    return a


def main():
    a = []
    for i in tqdm(range(1000)):
        img = get_frame(i)
        if img is None:
            break
        a.append(img)
    a = np.array(a, dtype=np.uint8)
    a = a[:, :, :, :3]
    print(a.dtype, a.shape)
    mp.write("a.mp4", a, 20)


main()
