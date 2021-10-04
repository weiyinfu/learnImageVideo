from moviepy.editor import VideoFileClip, concatenate_videoclips

clip1 = VideoFileClip("myvideo.mp4")
clip2 = VideoFileClip("myvideo2.mp4").subclip(50, 60)
clip3 = VideoFileClip("myvideo3.mp4")
final_clip = concatenate_videoclips([clip1, clip2, clip3])
final_clip.write_videofile("my_concatenation.mp4")
