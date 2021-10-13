import numpy as np

import mediapy as mp

"""
波形不光滑，就会导致有奇怪的频率出现。

即便频率非常连续，如果波形不连续，就会发生高音

直接使用np.concatenate拼接音频会导致声音出现高音，必须使用渐变来拼接两段音频
"""

s = """
1  7  1  7  1  7  1  7
"""
book = mp.nmn.content2book(s, 0.3)
rate = 8000
bad = np.concatenate([mp.nmn.freq2wave(freq, rate, duration) for freq, duration in book])
good = mp.nmn.concatenate_clips([mp.nmn.freq2wave(freq, rate, duration) for freq, duration in book], rate)
mp.write("a.wav", bad, rate)
mp.play("a.wav")
mp.write("a.wav", good, rate)
mp.play("a.wav")
