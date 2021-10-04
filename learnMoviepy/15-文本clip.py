import io

import numpy as np
import pylab as plt
from PIL import Image
from moviepy.editor import *

a = """one two three four five eight nine ten eleven twelve""".split()
b = "Spring Summer Autumn Winter".split()
b = np.array(b).reshape(-1, 1)
b = np.hstack([b, b, b]).reshape(-1)
c = "January February March April May June July August September October November December".split()
clips = []


def get_plot_image():
    cout = io.BytesIO()
    plt.savefig(cout)
    img = Image.open(cout)
    return np.array(img)


def get_image(s: str):
    plt.close()
    plt.axis('off')
    plt.text(0.5, 0.5, s, fontsize=30, ha='center', va='center')
    return get_plot_image()


for aa, bb, cc in zip(a, b, c):
    img = get_image(f"{aa}\n{bb}\n{cc}")
    now = ImageClip(img)
    now = now.set_duration(3)
    clips.append(now)
movie = concatenate_videoclips(clips)
movie = movie.set_fps(20)
movie.write_videofile('12.mp4')
