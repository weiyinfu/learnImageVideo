import mediapy as mp

video_file = "../imgs/taylor.mp4"
meta, video = mp.read(video_file)
# 生日快乐歌
birthday = """
5 5 6 5 1^ 7
5 5 6 5 2^ 1^
5 5 5^ 3^ 1^ 7 6
4^ 4^ 3^ 1^ 2^ 1^ 1^
"""
audio_file = "a.wav"
mp.nmn.build_music(audio_file, birthday, rate=2000, space_seconds=0.3)
mp.combine("a.mp4", video_file, audio_file)
mp.play('a.mp4')