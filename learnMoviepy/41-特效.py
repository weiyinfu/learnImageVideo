from moviepy.editor import *
"""
理解特效语法


effect_1(clip, args1) -> new clip
effect_2(clip, args2) -> new clip
effect_3(clip, args3) -> new clip
其中args表示参数和/或关键字参数。要按该顺序将这些函数应用于一个剪辑，您可以编写类似

newclip =  effect_3( effect_2( effect_1(clip, args3), args2), args1)
但这并不容易阅读。要获得更清晰的语法，您可以使用clip.fx：

newclip = (clip.fx( effect_1, args1)
               .fx( effect_2, args2)
               .fx( effect_3, args3))
"""
clip = (VideoFileClip("myvideo.avi")
        .fx( vfx.resize, width=460) # resize (keep aspect ratio)
        .fx( vfx.speedx, 2) # double the speed
        .fx( vfx.colorx, 0.5)) # darken the picture

# 自定义效果
def invert_green_blue(image):
        return image[:,:,[0,2,1]]

modifiedClip = my_clip.fl_image( invert_green_blue )