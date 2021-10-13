# 安装
```
pip install scikit-sound
```
需要下载ffplay、ffmpeg等命令。  
# 简介
sksound是一个非常小的包，它只包括两个子包：sounds和misc。

## sounds
sounds包下面有两个类：FFMPEG_info和Sound。
FFMPEG_info提供ffmpeg、ffmplay等命令的安装位置信息。  
Sound类提供IO功能。  
一般来说，只要把ffmpeg、ffmplay命令放在PATH中，可以忽略FFMPEG_info这个类。  

Sound类的作用：
* sounds.Sound.read_sound()：读取音频文件
* sounds.Sound.generate_sound() ：从numpy生成音频文件
* sounds.Sound.play() ：播放音频文件
* sounds.Sound.get_info() ：获取音频数据元信息，例如帧数、帧率
* sounds.Sound.write_wav() ：写入音频文件
* sounds.Sound.summary()：获取汇总信息

## misc
misc包其实是一个工具包，相当于util，包括一些GUI的实现。可以忽略之。   