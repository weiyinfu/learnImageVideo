import inspect

from mediapy import play, play_pipe
import mediapy as m


def test_check_play_args():
    # 用于测试，play和play_pipe这两个函数的参数应该是相同的
    play_info = inspect.getfullargspec(play)
    play_file_info = inspect.getfullargspec(play_pipe)
    assert play_file_info.args[1:] == play_info.args[1:]


def test_play_audio():
    m.play("../imgs/taylor.wav")


def test_play_video():
    # 也可以play一个URL
    m.play("../imgs/taylor.mp4", title="天下大势为我所控", border_less=True, duration_by_seconds=10, loop=3, show_mode=0)
