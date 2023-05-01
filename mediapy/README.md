看了moviepy、skvideo和sksound，发现这几个包实现非常简单，都是ffmpeg+数据处理，但是它们的写法也有一些瑕疵。于是整理了一个mediapy的包。本目录下存放使用mediapy读写多媒体数据的实例。  

* skvideo和sksound相对割裂，无法统一起来。
* ffmpeg的功能没有充分体现出来，例如录制视频和音频。 

