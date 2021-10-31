import numpy as np

"""
十二平分律：1 1+ 2 2+ 3 3+ 4 5 5+ 6 6+ 7
do re mi fa so la xi
中音la为440hz

中音do为261.625
"""
la = 440
s = 'do dodo re rere mi fa fafa so soso la lala xi'.split()
a = np.zeros(len(s))
ind = s.index('la')


def solve(dis):
    return 2 ** (np.log2(la) + 1 / 12 * dis)


freq = [solve(d) for d in np.arange(len(s)) - ind]
for sound, fre in zip(s, freq):
    print(sound, f"{fre:.3f}")
"""
do 261.626
dodo 277.183
re 293.665
rere 311.127
mi 329.628
fa 349.228
fafa 369.994
so 391.995
soso 415.305
la 440.000
lala 466.164
xi 493.883
"""