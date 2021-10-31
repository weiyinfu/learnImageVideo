"""
根据频率产生声音
"""

import mediapy as mp

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
mp.nmn.build_music("a.mp3", mixuebingcheng * 3, rate=8000, space_seconds=0.3, freq_wav_type=mp.nmn.FreqWaveType.three)
mp.play("a.mp3")
# mp.nmn.build_music("a.wav", birthday, space_seconds=0.3)
# mp.play("a.wav")
# mp.nmn.build_music("a.wav", twotiger + "  " + birthday, space_seconds=0.3)
# mp.play("a.wav")
# mp.nmn.get_float_array(twotiger)
