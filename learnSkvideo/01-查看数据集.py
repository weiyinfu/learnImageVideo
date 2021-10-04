import os
from os.path import *

import cv2
import matplotlib.animation as animation
import pylab as plt
from skvideo import datasets as d
from skvideo import io

"""
skimage的数据集中提供了四个视频：
* bikes.mp4：一个街头车水马龙的景象
* carphone_pristine.mp4：一个小伙在车上
* bigbuckbunny：一个动画片
* carphone_distorted.mp4：一个小伙在车上第二个版本
"""
folder = dirname(d.bikes())
print(f"{folder}  数据集文件下的全部视频", os.listdir(folder))


def play_video(file_name: str):
    cap = cv2.VideoCapture(f'{file_name}')

    while cap.isOpened():
        ret, frame = cap.read()
        cv2.imshow(basename(file_name), frame)
        if cv2.waitKey(40) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def play_video2(filepath):
    v = io.vread(filepath)
    fig, axes = plt.subplots()

    def update(frame_index):
        if frame_index > len(v):
            plt.close()
            return
        plt.imshow(v[frame_index])

    ani = animation.FuncAnimation(fig, update, interval=0.5)
    plt.show()


def main():
    for i in os.listdir(folder):
        filepath = join(folder, i)
        print(i)
        try:
            play_video(filepath)
        except:
            print(f"{i}播放失败")
            pass


main()
