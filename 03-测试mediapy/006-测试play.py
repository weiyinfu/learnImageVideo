import mediapy as m


def audio():
    m.play("../imgs/taylor.wav")


def video():
    # 也可以play一个URL
    m.play("../imgs/taylor.mp4", title="天下大势为我所控", border_less=True, duration_by_seconds=10, loop=3, show_mode=0)


video()
