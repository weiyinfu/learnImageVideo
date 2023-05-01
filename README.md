图像是非常重要的数据。眼睛是心灵的窗户，不仅仅是别人能从眼睛看向我们的心灵，也是心灵看向外界的必由之路。瞎子和聋子，谁更幸运一些？显然是聋子更幸运一些，他可以不听外界的胡言乱语，专心致志地通过书本或者视频去学习。  
人需要建立自己的知识体系，而建立知识体系就必须要存储，存储必须需要外脑，而外脑必须依靠纸张。不仅仅是存储，逻辑推演也需要用到外脑。而外脑的形式就是视觉。  
视觉是随机访存，而听觉则是顺序访存。  
看书是随机访存，看视频则是顺序访存。  
相比于音频和视频，自然语言是结构化更强的存储形式。  

计算机领域众多学科都和图像相关，例如图形学、计算几何、虚拟现实、图像处理、图像识别、图像分类、图像生成、模拟现实、三维建模、动画制作、游戏制作等，图像是一个巨大的领域，一生也钻研不到尽头。 

# ffmpeg
ffmpeg是世界上最著名的开源项目之一，它的功能非常丰富，skimage、moviepy等都只是ffmpeg功能的冰山一角，ffmpeg是值得深入学习的库。  

使用前需要下载ffmpeg、ffprob、ffplay等文件，把它们所在的目录添加到PATH中。[下载地址](https://evermeet.cx/ffmpeg/)

# 图像处理库
* opencv
* imagemagick
* PIL
* skimage

# 视频处理库
Python处理视频的库有很多，大都是基于ffmpeg进行的。这些代码代码量较小（一万行附近），并且作者维护不太积极。

* moviepy：基于ffmpeg、提供简单的视频编辑功能
* scikit-video：目标是为研究者提供便捷地视频数据处理功能，已经3年无更新。
* PyFFmpeg：ffmpeg的封装，已停止维护
* PyAV：ffmpeg的封装
* imageIO：提供各种图片数据的读写操作
* opencv：巨无霸长期维护的大库，值得深入学习。
* maptplotlib：python图表基础库。

# 视频和音频
视频帧率远远小于音频，人的视觉是50ms，也就是人眼接收的频率上限是20Hz。  
而音频人耳接收到的频率是20Hz到20000Hz，通常听得歌曲的频率是是440Hz附近。  
视频在空间上更占资源，音频在时间上更占资源。音频的帧率是视频的300倍，视频每一帧的大小是`300*300`的矩形，视频所占资源依旧是音频的好几百倍，同时音频的压缩算法比视频更简单一些。    

# 光线追踪渲染工具POV-RAY


# TODO
RGB YUV互转
https://www.google.com.hk/search?q=python%E5%9B%BE%E7%89%87%E8%BD%ACyuv&oq=python%E5%9B%BE%E7%89%87%E8%BD%ACyuv&aqs=chrome..69i57j0i30i546l2.7244j0j7&sourceid=chrome&ie=UTF-8

https://blog.csdn.net/yuejisuo1948/article/details/83512539

永不停止的音乐：https://flask.palletsprojects.com/en/1.1.x/patterns/streaming/

使用ffmpeg实现ndarray转图片。
声音证明波的位置不重要，重要的是波动。

视频生成：先生成三维物体，求三维物体的各种视图。


视频生成：
* 表达自己的思想
* 随机旋转的圆柱体，练习渲染
* 旋转的人形物体，用球、立方体、圆柱等搭建一个人体模型


给定文本，生成视频。一支笔正在写字的视频。  
两人对话的文本+语音。

做语音朗读器

# 源代码
* skimage：https://github.com/scikit-image/scikit-image  
* movie py：https://github.com/Zulko/moviepy  
* ffmpeg:https://www.ffmpeg.org/documentation.html  