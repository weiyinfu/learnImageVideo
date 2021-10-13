import subprocess as sp
import time
import winsound

import pygame

filename = "../imgs/childhood.mp3"
# 方法一：winsound
winsound.PlaySound(filename, winsound.SND_FILENAME)
# 方法二：afplay
cmd = ['afplay', filename]
sp.run(cmd)
# 方法三：ffplay，略
# 方法四：pygame
pygame.init()
pygame.mixer.music.load(filename)
pygame.mixer.music.play()
time.sleep(10)
