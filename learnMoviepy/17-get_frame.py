import pylab as plt
from moviepy.editor import *
from skvideo import datasets as d
from tqdm import tqdm

a = d.bikes()
a = VideoFileClip(a)
print(a.duration, a.fps)
sz = round(a.duration * a.fps)
print(sz)
for i in tqdm(range(sz)):
    img = a.get_frame(i)
    plt.imshow(img)
    plt.show()
