import io
import logging
from os.path import *

import numpy as np
import pylab as plt
from PIL import Image
from moviepy.editor import *
from skimage import transform
from skvideo import io as vio

"""
一个不错的gif生成网站
http://gif.weixinbiaoqing.com/wangjingze/
"""
log = logging.getLogger("haha")
log.level = logging.INFO
log.addHandler(logging.StreamHandler(sys.stdout))
folder = dirname(__file__)
filepath = join(folder, "../imgs/delicious.gif")
plt.rcParams['font.sans-serif'] = 'HanziPen SC,STFangsong,Baoli SC'.split(",")  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

original = [
    "老子就是饿死，死外边",
    "从这跳下去",
    "我也不会吃一点东西",
    "诶呀妈，真香"
]
woman = [
    "老子就是闲着",
    "哪怕啥都不干",
    "我也不会跟女人说一句话",
    "女人真他妈的带劲",
]
xingdaolong = "我乃零陵上将军邢道荣  汝是何人  速速下马来降  卧槽！真猛".split()
dapeng = "海淀区远大路世纪金源 十二点 明天谁迟到 谁请客".split()
learn = "不想睡觉 只想编程 音视频编程 太好玩了！".split()
bytedance = "住房有房补 吃饭管三餐 还发衣裳 诶妈！真香".split()
words = bytedance
region_list = [
    # 开始帧，结束帧，最小宽度（需要覆盖掉原来的文字）
    (0, 8, 236 - 65),
    (13, 23, 336 - 65),
    (26, 35, 248 - 58),
    (37, 50, 220 - 90),
]


def get_plot_image():
    cout = io.BytesIO()
    plt.savefig(cout)
    img = Image.open(cout)
    return np.array(img)


def get_image(s: str, rows: int, cols: int):
    plt.close()
    plt.figure(figsize=(10, 4))
    plt.axis('off')
    plt.text(0.5, 0.5, s, fontsize=20, ha='center', va='center')
    img = get_plot_image()
    plt.close()
    return img


def compact_word_image(img: np.ndarray):
    # 把文本图片空白区域去掉
    pos = np.argwhere(img < 2)
    fx, tx = np.min(pos[:, 0]), np.max(pos[:, 0])
    fy, ty = np.min(pos[:, 1]), np.max(pos[:, 1])
    sz = 4
    fx, tx = np.clip([fx - sz, tx + sz], 0, img.shape[0])
    fy, ty = np.clip([fy - sz, ty + sz], 0, img.shape[1])
    res = img[fx:tx + 1, fy:ty + 1, :]
    log.info(f"compcting {img.shape}=>{res.shape}")
    return res


def get_word_image(s: str, rows: int, cols: int, show=False):
    # 去width和height的最小值
    img = get_image(s, rows, cols)
    img = compact_word_image(img)
    r = rows
    c = round(rows / img.shape[0] * img.shape[1])
    if c > cols:
        r = round(cols / img.shape[1] * img.shape[0])
        c = cols
    res = transform.resize(img, (r, c, 4))
    log.info(f"resize image {img.shape}=>{res.shape} r={r},c={c}")
    # 去掉alpha层
    res = res[:, :, :3]
    res = (1 - res.astype(np.uint8)) * 255  # 颜色反转一下
    if show:
        fig, axes = plt.subplots(2, 1)
        m, n = axes.reshape(-1)
        m.imshow(img)
        n.imshow(res)
        plt.show()
    return res


f = VideoFileClip(filepath)
log.info(f"fps={f.fps}, duration={f.duration}, {f.fps * f.duration}")  # 一共有86张图片
a = vio.vread(filepath)
log.info(f"a.shape={a.shape}")


def main(show_image=False, verbose=0):
    for word, (f, t, word_width) in zip(words, region_list):
        # 目标大小为35，300，居中
        word_img = get_word_image(word, 35, 300)
        x, y = a[0].shape[0] - 40 / 2, a[0].shape[1] / 2
        fx, tx = int(x - word_img.shape[0] / 2), int(x + word_img.shape[0] / 2)
        # 先涂黑一块区域，覆盖掉原来的文字
        fy, ty = int(y - word_img.shape[1] / 2), int(y + word_img.shape[1] / 2)
        fyy, tyy = int(y - word_width / 2), int(y + word_width / 2)
        word_img = word_img[:tx - fx, :ty - fy, :]  # 对字幕文件进行裁剪一下
        a[f:t + 1, fx:tx, fyy:tyy, :] = 0
        a[f:t + 1, fx:tx, fy:ty, :] = word_img
        if show_image:
            fig, axes = plt.subplots(2, 1)
            one, two = axes.reshape(-1)
            one.imshow(a[f])
            two.imshow(word_img)
            plt.show()
    log.info(f"最终结果的大小{a.shape}")
    vio.vwrite("a.gif", a, inputdict={"-r": "8"}, outputdict={"-r": "8"}, verbosity=verbose)


def test_word_image():
    img = get_word_image(words[0], 35, 300, True)

    print(img.shape)
    plt.imshow(img)
    plt.show()


main(False)
# test_word_image()
