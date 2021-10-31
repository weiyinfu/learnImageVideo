import numpy as np

import mediapy as mp

mp.nmn.build_music('a.mp3', mp.nmn.momo, freq_wav_type=mp.nmn.FreqWaveType.three, smooth_method=mp.nmn.SmoothMethod.phi_smooth)
meta, a = mp.read('a.mp3')
print(np.min(a), np.max(a), np.mean(a))
mp.play('a.mp3')
