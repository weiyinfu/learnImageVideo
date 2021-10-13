import mediapy as mp

s = "1 7 1 7 1 7 1 7 1 7 1 7"
rate = 8000
book = mp.nmn.content2book(s, 0.3)
a = []
for freq, duration in book:
    a.append(mp.nmn.freq2wave(freq, rate, duration))
print(sum(len(i)for i in a))
a = mp.nmn.concatenate_clips(a)
print(len(a))
print(a.dtype)
mp.write('a.wav', a, rate)
mp.play("a.wav")
