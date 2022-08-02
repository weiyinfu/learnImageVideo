import mediapy as mp
import numpy as np
from tqdm import tqdm

meta, a = mp.read('xigua.mp4')
a = np.array(a)


def smart():
    one = a[:, :, :, 0] > 125
    two = np.argmax(a, axis=3) == 0
    three = a[:, :, :, 0] / np.sum(a, axis=3) > 0.4
    print(one.shape, two.shape, three.shape)
    candidates = np.logical_and(one, two)
    print(candidates.shape, len(candidates))
    t = a[candidates, 0]
    a[candidates, 0] = a[candidates, 2]
    a[candidates, 2] = t


def brute():
    for i in tqdm(range(a.shape[0])):
        for x in range(a.shape[1]):
            for y in range(a.shape[2]):
                it = tuple(a[i, x, y])
                if it[0] > 200 and np.argmax(it) == 0:
                    a[i, x, y, :] = (it[1], it[0], it[2])


def fast():
    tmp = a[:, :, :, 0]
    a[:, :, :, 0] = a[:, :, :, 2]
    a[:, :, :, 2] = tmp


# fast()
smart()
mp.write('xigua2.mp4', a, meta.frame_rate())
