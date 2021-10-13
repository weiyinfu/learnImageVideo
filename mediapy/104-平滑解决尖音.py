from typing import List

import numpy as np

import mediapy as mp

s = "1 7 1 7 1 7 1 7"
rate = 8000
book = mp.nmn.content2book(s, 0.3)
a = []
for freq, duration in book:
    a.append(mp.nmn.freq2wave(freq, rate, duration))


def concatenate_clips_by_merge_common(a: List[np.ndarray], rate: int):
    # 将若干个音频片段拼接起来，拼接过程中需要保证波形平滑连续
    ans = a[0]
    cover = round(80 / 8000 * rate)  # 根据不同的rate决定渐变部分的长度
    for i in range(1, len(a)):
        nex = a[i]
        if len(ans) == 0:
            ans = nex
            continue
        if len(nex) == 0:
            continue
        sz = min(cover, len(ans), len(nex))
        weight = np.linspace(0, 1, sz)
        merged = weight * nex[:sz] + (1 - weight) * ans[-sz:]
        ans = np.concatenate([ans[:-sz], merged, nex[sz:]])
    return ans


cover = 100
b = [a[0]]
for i in range(1, len(a)):
    pre = b[-1]
    nex = a[i]
    if len(pre) == 0:
        b.append(nex)
        continue
    if len(nex) == 0:
        continue
    weight = np.linspace(0, 1, cover)
    print(weight.shape, pre.shape, nex.shape)
    merged = weight * nex[:cover] + (1 - weight) * pre[-cover:]
    b[-1] = pre[:-cover]
    b.append(merged)
    b.append(nex[cover:])
print(len(b), len(a))
a = np.concatenate(b)
print(a.dtype)
mp.write('a.wav', a, rate)
mp.play("a.wav")
