import mediapy as mp

meta, a = mp.read("../imgs/taylor.mp4", filetype='audio')
print(a.shape, a.dtype)
a = a[:, 1] / (2 ** 15)
print(meta.audio_stream.get_sample_rate(), meta.audio_stream.sample_rate)
b = mp.ap.sfft(a, meta.audio_stream.get_sample_rate(), window=500, freq_bei=1, duration_bei=1, top=1)
print(b.shape, a.shape)
print(b.dtype, a.dtype)
mp.write('a.wav', b, rate=int(meta.audio_stream.sample_rate))
mp.play('a.wav')
