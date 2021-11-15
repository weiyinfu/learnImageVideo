import numpy as np
import skimage.io as io

import mediapy as mp
from mediapy import hand

boy = io.imread("../imgs/简笔画/girl.jpg")
pos = np.argwhere(np.mean(boy, axis=2)[:, :, ] < 125)
xs, ys = pos[:, 0], pos[:, 1]
hand_image, hand_pointer = hand.hands[0]
point_list = hand.analyze_point_sequence(xs, ys)
a = hand.draw_point_list(boy, point_list, hand_image, hand_pointer)
mp.write('a.mp4', a, 25)
mp.play('a.mp4')
