import numpy as np

import mediapy as mp

"""
高低音三个音部一起唱生日快乐
"""
# 生日快乐歌
birthday = """
5 5 6 5 1^ 7
5 5 6 5 2^ 1^
5 5 5^ 3^ 1^ 7 6
4^ 4^ 3^ 1^ 2^ 1^ 1^
"""
birthday_low = """
5_ 5_ 6_ 5_ 1 7_
5_ 5_ 6_ 5_ 2 1
5_ 5_ 5 3 1 7_ 6_
4 4 3 1 2 1 1
"""
birthday_high = """
5^ 5^ 6^ 5^ 1^^ 7^
5^ 5^ 6^ 5^ 2^^ 1^^
5^ 5^ 5^^ 3^^ 1^^ 7^ 6^
4^^ 4^^ 3^^ 1^^ 2^^ 1^^ 1^^
"""
mid_rate, mid = mp.nmn.get_float_array(birthday, rate=4000, space_seconds=0.3)
high_rate, high = mp.nmn.get_float_array(birthday_high, rate=4000, space_seconds=0.3)
low_rate, low = mp.nmn.get_float_array(birthday_low, rate=4000, space_seconds=0.3)
print(mid_rate, high_rate, low_rate)
print(mid.shape, high.shape, low.shape)
a = np.zeros(len(mid) + 1000)
a[:len(low)] += high
a[-len(high):] += low
shift = (len(a) - len(mid)) // 2
a[shift:shift + len(mid)] += mid
a /= 3
mp.write("a.wav", a, rate=4000)
mp.play("a.wav")
