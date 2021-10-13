# 图像编解码

图像编解码是一门学科，研究如何高效编码（节省内存）、解码（节省时间）。视频、图片、音频包含的数据量很大，根据这些多媒体的自身特点，可以提出更好的压缩算法。

# ffmpeg命令的基本格式

ffmpeg globalOptions inputList OutputList  
inputList中的每一项都是inputOption+inputFile  
outputList中的每一项都是outputOption+outputFile

inputList跟outputList格式很相似，每个inputOption只能对它接下来的那个文件选项起作用，一旦遇到一个文件，就会把过去的选项清空掉。

# ffmpeg的流程

一个多媒体文件包括格式信息+数据信息两部分。

输入文件经过demuxer解析文件格式得到encoded数据包，encoded数据包经过decoder得到解码之后的每一帧的数据。每一帧的数据经过编码器又得到编码之后的数据包，muxer把数据包和格式打包成文件。

```plain
 _______              ______________
|       |            |              |
| input |  demuxer   | encoded data |   decoder
| file  | ---------> | packets      | -----+
|_______|            |______________|      |
                                           v
                                       _________
                                      |         |
                                      | decoded |
                                      | frames  |
                                      |_________|
 ________             ______________       |
|        |           |              |      |
| output | <-------- | encoded data | <----+
| file   |   muxer   | packets      |   encoder
|________|           |______________|

```

此外，为了提高效率，数据包部分可以直接copy到输出中，这样就省掉了encoder和decoder编解码数据包的过程。

```plain
 _______              ______________            ________
|       |            |              |          |        |
| input |  demuxer   | encoded data |  muxer   | output |
| file  | ---------> | packets      | -------> | file   |
|_______|            |______________|          |________|

```

单词释义：  
muxing：把多个输入合并成一个进行输出 demuxing：把一个输入拆成多个进行输出

# 流的类型

一个多媒体文件可以视为若干个流的集合，流的类型有五种。

* 视频流
* 音频流
* 字幕流（subtitle）：字幕流是可以跟视频流混在一起的，那么为啥要吧字幕流独立出来呢？考虑一些场景：关闭字幕、字幕翻译、双语字幕等。
* 附件（attachment）：有些视频文件格式可以往视频文件里面塞进去一些附加文件，例如字体文件。
* data：数据流，用于自定义一些数据

不同的文件格式支持的流的类型是不一样的，例如mp3只支持音频流，pcm只支持音频流的数据部分（不包括格式部分）。

# 常用的枚举值

这些枚举值都可以通过ffplay、ffprobe、ffmpeg等命令直接获取，例如`ffplay -codecs > codecs.txt`

* codecs：包括视频和音频的编码方式，是数据部分的编码格式，也就是encoders和decoders需要依据codecs进行编码或解码。
* encoders，decoders：视频和音频文件的数据部分的编码格式
* muxers，demuxers：给定数据部分+文件格式，输出文件内容。
* formats：文件格式
* pix_fmts：像素点的颜色表示
* sample_fmts：音频数据中音频数据的表示
* protocols：支持的文件的协议
* layouts：音频的通道及其布局

# png和jpg

png支持4通道有透明度，jpg只支持3通道无透明度。  
jpg的压缩效果优于png，png的灵活性优于jpg，png可用于制作游戏精灵图片。

# 比特率

比特率又称“二进制位速率”，俗称“码率”。 表示单位时间内传送比特的数目。 用于衡量数字信息的传送速度，常写作bit/sec。 ...
在近代数字通信中，数字化的视频等信息传输量较大，因此往往以每秒千比特或每秒兆比特为单位于以计量，分别写作kbit/sec（或kbps）和Mbit/sec（或Mbps）。

# subprocess.Popen

[参考文档](https://docs.python.org/3/library/subprocess.html)
Python是一门胶水语言，它可以在命令行的基础上实现库。其中起到关键作用的就是subprocess.Popen()。  
可以通过它的stdin，stdout进行输入和输出。

```python
import subprocess

p = subprocess.Popen(['ffplay', '-help'])
p.stdin.write('asdf')
p.stdout.read(100)
```

为了节省内存，可以使用bufsize参数指明各个管道的缓冲区大小。

* 0表示不做缓存
* 1 基于行进行缓存
* 其它正数表示缓存区尽量接近那样的大小
* -1：系统默认值，mac上为8192

# 视频和音频录制
[doc](https://trac.ffmpeg.org/wiki/Capture/Capture/Desktop%E4%B8%AD%E6%96%87%E7%89%88%E6%9C%AC)
If you specify the input format and device then ffmpeg can grab video and audio directly.

`ffmpeg -f oss -i /dev/dsp -f video4linux2 -i /dev/video0 /tmp/out.mpg`
Or with an ALSA audio source (mono input, card id 1) instead of OSS:

`ffmpeg -f alsa -ac 1 -i hw:1 -f video4linux2 -i /dev/video0 /tmp/out.mpg` 
Note that you must activate the right video source and channel before launching ffmpeg with any TV viewer such as xawtv by Gerd Knorr. You also have to set the audio recording levels correctly with a standard mixer.

Grab the X11 display with ffmpeg via

`ffmpeg -f x11grab -video_size cif -framerate 25 -i :0.0 /tmp/out.mpg`
0.0 is display.screen number of your X11 server, same as the DISPLAY environment variable.

`ffmpeg -f x11grab -video_size cif -framerate 25 -i :0.0+10,20 /tmp/out.mpg`
0.0 is display.screen number of your X11 server, same as the DISPLAY environment variable. 10 is the x-offset and 20 the y-offset for the grabbing.
