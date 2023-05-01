"""
根据频率产生声音
"""
import numpy as np

import mediapy as mp

max_freq = 2000
ma = [261.626, 293.665, 329.628, 349.228, 391.995, 440.000, 493.883, ]


def get(freq, rate, duration):
    sz = int(duration * rate)
    a = np.arange(sz)
    t = a / len(a) * duration
    return np.sin(np.pi * 2 * freq * t)


# 两只老虎简谱
content = """
1 2 3 1  1 2 3 1
3 4 5  3 4 5
5 6 5 4 3 1  5 6 5 4 3 1
3 5_ 1  3 5_ 1
"""


def tokenize(content):
    book = []
    for i in content:
        if not book or i.isspace() != book[-1].isspace():
            book.append(i)
        else:
            book[-1] += i
    return book


def token2freq(token):
    ch = int(token[0])
    if ch == 0:
        return 0
    bas = ma[ch - 1]
    cnt = (len(token) - 1)
    if cnt == 0:
        return bas
    if token[1:] == '_' * cnt:
        bas /= 2 ** cnt
    elif token[1:] == '^' * cnt:
        bas *= 2 ** cnt
    else:
        raise Exception(f"unhandled token {token}")
    return bas


def get_duration(s):
    cnt = 0
    for i in s:
        if i == ' ':
            cnt += 1
        elif i == '\n':
            cnt += 2
    return cnt


def content2book(s):
    book = [[0, 0]]
    for i in tokenize(content):
        if i.isspace():
            book[-1][1] = get_duration(i)
        else:
            freq = token2freq(i)
            book.append([freq, 0])
    return book


book = content2book(content)
print(book)
rate = max_freq * 2
a = np.concatenate([get(freq, rate, duration * 0.3) for freq, duration in book])
a = (a * 2 ** 14).astype(np.int16)
print("文件长度", len(a), a.dtype, rate)
mp.write("a.wav", a, rate=rate)
mp.play("a.wav")
