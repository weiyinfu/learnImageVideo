1. `ffmpeg -hide_banner _log_level error`
关闭banner和log
2. `ffmpeg -i /tmp/test.yuv /tmp/out.avi`
快速格式转换
3. `ffmpeg -i /tmp/test.yuv -y /tmp/out.avi`
强制写入out.avi，指定-y，即便输出文件已经存在也会覆盖掉。也可以指定-n，表示一定不要覆盖已存在的文件。-y和-n是全局选项。全局选项不会因为遇到新文件而遗忘。     
4. `ffmpeg -stream_loop -1 -i a.mp3 -i b.mov c.mp4`
使用stream_loop可以控制流的播放次数，-1表示循环无数次，0表示不循环，正数表示循环次数。  
5. `ffmpeg -f mp3 -i /tmp/test.yuv /tmp/out.avi`
-f强制指明输入文件的格式，不要让ffmpeg自作主张。通常不需要指定-f，因为ffmpeg能够自动分析，强制指定的格式还存在格式错误的风险。  
6. `ffmpeg -i input.avi -r 24 output.avi`
重写input.avi的帧率为24，不改变播放时长。  
7. `ffmpeg -r 1 -i input.m2v -r 24 output.avi`
以input.m2v的每帧数据和帧率为1读入视频，以帧率24写入视频。 
8. `ffmpeg -i A.avi -i B.mp4 out1.mkv out2.wav -map 1:a -c:a copy out3.mov`
输入为A.avi和B.mp4两个文件，输出包括三个文件。out1和out2没有指明流映射，而out3指明了流映射。如果没有指明流映射，则从输入中选择最佳的流。  
最佳的流指的是：如果是视频流，分辨率最高（长度乘宽度）的最好；如果是音频流，通道最多（音轨个数）的最好；如果是字幕流，默认选择第一个。
out3的map 1:a表示接受第一个输入的所有音频流。1:v则表示视频流。一旦指定了map，则自动选择流不在生效。  
out3.mov还制定了`c:a copy`参数，`c:a`表示音频的编码方式，copy表示直接复制数据包不经过编解码过程。 
9. `ffmpeg -i /tmp/a.wav -s 640x480 -i /tmp/a.yuv /tmp/a.mpg`
把音频和图像拼接起来，同时设置视频尺寸
10. `ffmpeg -i /tmp/a.wav -ar 22050 /tmp/a.mp2`
音频采样率改为22050Hz。
11. `ffmpeg -i bikes.mp4 -f image2pipe -pix_fmt rgb24 -vcodec rawvideo -`
读取bikes.mp4的文件内容，并将文件内容打印到控制台。 
12. `ffmpeg -y -f rawvideo -pix_fmt rgb24 -s 680x480 -i - outputvideo.mp4`
写入视频文件内容，其中文件内容来自于控制台。这个命令的关键在于rawvideo，它能够将视频的格式部分都去掉，只保留未压缩的数据部分。-y参数表示强制写入，即便output文件已经存在也会覆盖掉。-s指明了输出视频的大小，-pix_fmt表示颜色的表示方法。`-i -`这个参数非常重要，表示输入文件参考接下来的输入。   
13. `ffmpeg -i ../imgs/taylor.mp4 -f s16le -`
读取原始音频数据。此命令从mp4中提取音频文件，关键命令在于`-f s16e`，使用带符号16位小头序表示每个采样。如果-f wav，则输出的数据依旧是带格式的。  
14. `ffmpeg -i INPUT -map 0 -c:v libx264 -c:a copy OUTPUT`
取第一个输入文件，-map 0；-c:v libx264，视频编码器使用libx264，-c:a copy,音频直接复制不经过编解码。  
15. `ffmpeg -i INPUT -map 0 -c copy -c:v:1 libx264 -c:a:137 libvorbis OUTPUT`
`-c copy`没有指明具体的流，所以对于全部流的默认行为是copy，但是-c:v:1 libx264制定了第2个视频流的编码方式，所以这个视频流就不会直接copy而是使用正常的编解码过程。后面的第138个音频流也是同样道理。  
16. `ffmpeg -i in.avi -metadata title="my title" out.flv`
给输出文件设置metadata，metadata是随意写的kv对，一个metadata只能设置一个kv对。  

17. `ffmpeg -i INPUT -metadata:s:a:0 language=eng OUTPUT`
为第一个音频流设置语言。 
18. `ffmpeg -i in.mp4 -i IMAGE -map 0 -map 1 -c copy -c:v:1 png -disposition:v:1 attached_pic out.mp4`
为视频设置封面。
19. `ffmpeg -i myfile.avi -target vcd /tmp/vcd.mpg`
使用target可以简化选项，target可以指定一些参数模板。target类型包括五种：vcd, svcd, dvd, dv, dv50. 每种大类又可以使用前缀指定小类，pal-, ntsc- or film-，小类包括三种. 
    例如vcd等价于以下参数。 
    ```plain
    pal:
        -f vcd -muxrate 1411200 -muxpreload 0.44 -packetsize 2324
        -s 352x288 -r 25
        -codec:v mpeg1video -g 15 -b:v 1150k -maxrate:v 1150v -minrate:v 1150k -bufsize:v 327680
        -ar 44100 -ac 2
        -codec:a mp2 -b:a 224k
    
    ntsc:
    -f vcd -muxrate 1411200 -muxpreload 0.44 -packetsize 2324
    -s 352x240 -r 30000/1001
    -codec:v mpeg1video -g 18 -b:v 1150k -maxrate:v 1150v -minrate:v 1150k -bufsize:v 327680
    -ar 44100 -ac 2
    -codec:a mp2 -b:a 224k
    
    film:
    -f vcd -muxrate 1411200 -muxpreload 0.44 -packetsize 2324
    -s 352x240 -r 24000/1001
    -codec:v mpeg1video -g 18 -b:v 1150k -maxrate:v 1150v -minrate:v 1150k -bufsize:v 327680
    -ar 44100 -ac 2
    -codec:a mp2 -b:a 224k
    ```
20. `ffmpeg -i INPUT -attach DejaVuSans.ttf -metadata:s:2 mimetype=application/x-truetype-font out.mkv`
为字幕添加字体文件。 
21. `ffmpeg -dump_attachment:t:0 out.ttf -i INPUT`
把第一个附件导出来。 
22. `ffmpeg -dump_attachment:t "" -i INPUT`
把所有的附件都导出来。 
23. -vcodec等价于-codec:v,-acodec等价于-codec:a，字幕流、data流同理。 
24. `ffmpeg -itsscale 1.5 -i taylor.mp4  scale.mp4`
使用itsscale（input timestamp scale）选项缩放视频的播放时长。  
25. `ffmpeg -itsoffset 30 -t 120 -i taylor.mp4  -t 80 scale.mp4`
设置开始播放的位置为30s，播放时长为120s。输出位置的-t 80，表示输出的这个视频只保留80s的数据，超过部分丢弃。  
26. `ffmpeg -i taylor.mp4  -fs 120 scale.mp4`
执行文件转换，但是输出的文件的大小限制在120b。 
27. `ffmpeg -ss 30 -i taylor.mp4  -ss 45 scale.mp4`
从输入文件的30b处开始解码，输出是从45b处开始编码。  
28. 流选择
使用map：1:2表示选择第2个输入文件的第3个流。使用vn,an,dn,sn。分别表示忽略视频流、忽略音频流、忽略数据流、忽略字幕流。
29. `ffprobe -print_format json -show_streams -show_format -show_pixel_formats -hide_banner -loglevel error ../imgs/taylor.mp4`
以JSON形式打印文件meta信息。
30. ` ffprobe -show_pixel_formats -print_format json > pixel_formats.json`
打印pixel_formats详细信息。  
31. `ffmpeg -i input.flv pipe:1 | ffplay -i -`
ffmpeg+ffplay，一边写一边播放。pipe:0表示输入，pipe:1表示输出，pipe:2表示错误流。也可以直接使用-作为占位符替代，在需要输入流的地方-表示输入流，在需要输出流的地方-表示输出流。   
32. `ffmpeg -hide_banner -loglevel error   -i a.matroska -f matroska pipe:1  |ffplay -i -`
matroska类型的格式能够流式访问。  
33. `ffmpeg -f avfoundation -r 30  -i 1:0 -f image2pipe  - | ffplay -`
一边录制一边播放。  
34. `ffmpeg -i input.avi <options> -f matroska - | ffplay -`
一边往外写，一边播放。 
35. `ffmpeg -i segment.ts -c copy -movflags frag_keyframe+empty_moov -f mp4 -`
导出的时候，导出mp4格式。如果没有movflags参数会报错。  [Stack Overflow](https://stackoverflow.com/questions/34123272/ffmpeg-transmux-mpegts-to-mp4-gives-error-muxer-does-not-support-non-seekable) [doc](https://ffmpeg.org/ffmpeg-formats.html#mov_002c-mp4_002c-ismv)
36. mp4在PICO设备上无法播放，使用ffmpeg转换格式
    ```
    ffmpeg -i a.mp4 -vcodec h264 -crf 26  -pix_fmt yuv420p a-avc.mp4
    ```
37. linux使用x11grab设备采集视频图像

    ffmpeg -video_size 1024x768 -framerate 25 -f x11grab -i :0.0+100,200 output.mp4
这条命令将会从桌面图像的左上角偏移坐标位置为 (x=100, y=200)处获取宽高为1024x768的图像.  
如果需要加入音频，有两种：采集ALSA或者采集pulse。  
采集ALSA：`ffmpeg -video_size 1024x768 -framerate 25 -f x11grab -i :0.0+100,200 -f alsa -ac 2 -i hw:0 output.mkv`
采集pulse：`ffmpeg -video_size 1024x768 -framerate 25 -f x11grab -i :0.0+100,200 -f pulse -ac 2 -i default output.mkv`
38. 苹果MacOS采集音视频，使用avfoundation采集。  
首先需要查看设备列表： `ffmpeg -f avfoundation -list_devices true -i ""`
然后执行命令`ffmpeg -f avfoundation -i "<screen device index>:<audio device index>" out.mov`。 这个命令`-f avfoundation`指定了输入流的格式。`-i`指定了视频设备编号和音频设备编号。这条命令执行后将会从 `<screen device index>` 编号处获得视频图像，从 `<audio device index>` 编号处获得音频数据写入至输出文件 out.mov 中.
39. 
