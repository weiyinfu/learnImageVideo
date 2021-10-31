"""
fps意思是frames perseconds，也就是帧率

无论是音频还是视频，都是离散的东西，把它们快速播放就变成了连续。

总帧数=时长 * 帧率
文件大小=帧数 * 每帧的字节数

对于音频，如果是单轨道，相当于深度为一
如果是双轨道，相当于深度为二

对于视频，如果是灰色，相当于深度为1
如果是三色相当于深度为3

skimage的vwrite默认的帧率是25。
"""
import mediapy as mp

meta, a = mp.read("../imgs/taylor.mp4")
print(a.shape)
print(meta.video_stream.duration)  # 持续时长，单位为秒
print('帧率', meta.video_stream.r_frame_rate, '总帧数', meta.video_stream.nb_frames)
print('视频时长', meta.video_stream.nb_frames / meta.frame_rate())
print('音频时长', meta.audio_stream.duration)
