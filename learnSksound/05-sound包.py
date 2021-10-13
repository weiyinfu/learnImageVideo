import sksound

print(dir(sksound))
from sksound import sounds

# 第一种构造方式：从文件加载
filepath = "../imgs/childhood.mp3"
a = sounds.Sound(filepath)
a.play()  # 使用ffplay命令播放文件

# 第二种构造方式：从numpy构造
b = sounds.Sound(inData=a.data, inRate=a.rate)
b.play()

# 第三种方式：
c = sounds.Sound()
c.generate_sound(a.data, a.rate)

# 第四种方式
c = sounds.Sound()
c.read_sound(filepath)

# 打印信息
print(a.get_info())
print(a.summary())

# 保存文件
b.write_wav("a.mp3")

# 从视频中加载音频
sounds.Sound()
