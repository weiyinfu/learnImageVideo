"""
根据简谱生成音乐
"""
from typing import List

import numpy as np
from scipy import interpolate as it

import mediapy.io as mp

logger = mp.logger

# C调的频率
ma = [261.626, 293.665, 329.628, 349.228, 391.995, 440.000, 493.883, ]

# 两只老虎简谱
twotiger = """
1 2 3 1  1 2 3 1
3 4 5  3 4 5
5 6 5 4 3 1  5 6 5 4 3 1
3 5_ 1  3 5_ 1
"""
# 生日快乐歌
birthday = """
5 5 6 5 1^ 7
5 5 6 5 2^ 1^
5 5 5^ 3^ 1^ 7 6
4^ 4^ 3^ 1^ 2^ 1^ 1^
"""
# 千与千寻
qianyuqianxun = """
1 2 3 1 5  3 2 5 2 1 6_ 3 1
7_ 6_ 7_ 1 2 5_ 1 2 3 4  4 3 2 1 2
1 2 3 1 5 3 2 5 2 1 6_ 6_ 7_ 1 5_
5_ 6_ 7_ 1 2 5_ 1 2 3 4 4 3 2 1 1
3 4 5 5 5 5   5 6 5 4 3 3 3 3 3 4 3 2 1 1 1 7_ 6_ 7_ 7_  1  2 2 3 2 3 2
3 4 5 5 5 5   5 6 5 4 3 3 3 3 4 3 4 3 2 1 7_ 6_ 6_ 7_ 1 2 5_ 1 2 3 2 2 2 1   
1
"""
# 世上只有妈妈好
momo = """
6  5 3 5 1^ 6 5 6 
3 5 6 5 3  2 1 6_ 5 3 2
2 3 5 5  6 3 2 1
5 3 2 1 6_ 1 5_
"""
# 蜜雪冰城
mixuebingcheng = """
3 5 5 6 5 3 1  1 2 3 3 2 1 2
3 5 5 6 5 3 1  1 2 3 3 2 2 1
4 4 4 6  5 5 3 2
3 5 5 6 5 3 1  1 2 3 3 2 2 1 
"""


class FreqWaveType:
    strong2weak = '1=>0'
    weak2strong = '0=>1'
    three = "0=>1=>0"
    constant = "1"


def freq2wave(freq: float, rate: float, duration: float, phi: float = 0, A: float = 1.0, freq_wav_type: str = FreqWaveType.strong2weak):
    # 给定频率，采样率，时长，生成一个波形数组
    sz = int(duration * rate)
    t = np.arange(sz) / sz * duration
    if freq_wav_type == FreqWaveType.strong2weak:
        a = np.linspace(1, 0, sz)
    elif freq_wav_type == FreqWaveType.weak2strong:
        a = np.linspace(0, 1, sz)
    elif freq_wav_type == FreqWaveType.constant:
        a = np.ones(sz, dtype=np.float32)
    elif freq_wav_type == FreqWaveType.three:
        a = np.concatenate([np.linspace(0, 1, sz // 2), np.linspace(1, 0, sz - sz // 2)])
    else:
        raise Exception(f"unkown audio type {freq_wav_type}")
    ans = a * A * np.sin(np.pi * 2 * freq * t + phi)
    return ans


def tokenize(content: str) -> List[str]:
    # 将简谱字符串转为token列表
    book = []
    for i in content:
        if not book or i.isspace() != book[-1].isspace():
            book.append(i)
        else:
            book[-1] += i
    return book


def token2freq(token: str) -> float:
    # 将token转为频率
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


def token2duration(s: str) -> float:
    # 把一个空白字符串转为停顿的时间长度
    cnt = 0
    for i in s:
        if i == ' ':
            cnt += 1
        elif i == '\n':
            cnt += 2
    return cnt


def content2book(s: str, space_seconds: float):
    book = [[0, 0.]]
    for i in tokenize(s):
        if i.isspace():
            book[-1][1] = token2duration(i)
        else:
            freq = token2freq(i)
            book.append([freq, 0])
    for i in book:
        i[1] *= space_seconds
    return book


def concatenate_clips(a: List[np.ndarray], new_point_count=4):
    ans = a[0]
    for i in range(1, len(a)):
        nex = a[i]
        if len(ans) == 0:
            ans = nex
            continue
        if len(nex) == 0:
            continue
        sz = new_point_count
        use = 5
        line = np.concatenate([ans[-use:], nex[:use]])
        beg = (len(line) - sz) // 2
        end = len(line) - beg
        ind = np.arange(len(line))
        need = np.concatenate([ind[:beg], ind[end:]])
        t, c, k = it.splrep(ind[need], line[need])
        f = it.BSpline(t, c, k)
        line = f(ind)
        ans = np.concatenate([ans[:-use], line, nex[use:]])
    return ans


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


class SmoothMethod:
    phi_smooth = 'phi_smooth'
    linear_smooth = 'linear_smooth'
    bspline_smooth = 'bspline_smooth'


def get_float_array(content: str, rate: int = 0, space_seconds=0.3, smooth_method=SmoothMethod.phi_smooth, freq_wav_type=FreqWaveType.three):
    book = content2book(content, space_seconds)
    big_freq = np.max([i[0] for i in book])
    if rate != 0 and big_freq * 2 > rate:
        raise Exception(f"采样率偏低:最大频率{big_freq}")
    if rate == 0:
        rate = big_freq * 2 + 10  # 应该略微高出最大频率
    rate = int(rate)
    if smooth_method == SmoothMethod.phi_smooth:
        logger.info(f"using phi to smooth")
        phi = 0
        a = []
        for freq, duration in book:
            now = freq2wave(freq, rate, duration, phi, freq_wav_type=freq_wav_type)
            a.append(now)
            phi += freq * np.pi * 2 * duration
        a = np.concatenate(a)
    else:
        a = []
        for freq, duration in book:
            now = freq2wave(freq, rate, duration, freq_wav_type=freq_wav_type)
            a.append(now)
        if smooth_method == SmoothMethod.bspline_smooth:
            logger.info("bspline")
            a = concatenate_clips(a)
        elif smooth_method == SmoothMethod.linear_smooth:
            logger.info(f"merge common")
            a = concatenate_clips_by_merge_common(a, rate=rate)
    return rate, a


def build_music(filepath: str, content: str, rate: int = 0, space_seconds=0.3, freq_wav_type=FreqWaveType.three, smooth_method: str = SmoothMethod.phi_smooth):
    rate, a = get_float_array(content, rate, space_seconds, freq_wav_type=freq_wav_type, smooth_method=smooth_method)
    logger.info(f"writing file {a.shape} {a.dtype}")
    a = a * (2 ** 15)
    a = a.astype(np.int16)
    assert a.dtype == np.int16
    mp.write(filepath, a, rate=rate, )
