from math import log2

import numpy as np
import pandas as pd

"""
人类顶多能够听到10个音阶

人类只有120个音符，7*17=119
"""
print(log2(20000 / 20))
la = 440

print(2 ** (log2(20000) + log2(20) / 2), '音频中位数')


def solve(dis):
    return 2 ** (np.log2(la) + 1 / 12 * dis)


i = 0
a = {}
while 1:
    yin = solve(i)
    if yin > 20000:
        break
    a[i] = yin
    i += 1
i = 0
while 1:
    yin = solve(i)
    if yin < 20:
        break
    a[i] = yin
    i -= 1
rc_yin = []
for ind, yin in a.items():
    if (ind % 12 + 12) % 12 in (1, 4, 6, 8, 11):
        continue
    c = [3, 5, 7, 9, 10, 0, 2].index((ind % 12 + 12) % 12)
    r = (ind + 9) // 12
    rc_yin.append((r, c, yin))
rc_yin.sort()
a = np.array(rc_yin)
print('音的个数', len(a))
b = np.zeros((int(a[-1, 0] - a[0, 0] + 1), 7))
for r, c, yin in a:
    b[int(r - a[0, 0]), int(c)] = yin
yin_jie = list(set(a[:, 0]))
yin_jie.sort()
ans = pd.DataFrame(b, index=yin_jie, columns='do re mi fa so la xi'.split())
print(ans)
ans.to_csv("yinjie.csv")
