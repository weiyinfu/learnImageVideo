import json
from pprint import pprint

import mediapy as m


def video():
    resp = m.probe("../imgs/taylor.mp4")
    json.dump(resp, open('haha.json', 'w'), ensure_ascii=False, indent=2)


def audio():
    pprint(m.probe("../imgs/taylor.mp3"))
    pprint(m.get_meta("taylor.mp3"))


def three():
    info = m.get_meta('./a.matroska')
    print(info.video_stream)
    json.dump(info.video_stream.dict(), open('haha.json', 'w'), ensure_ascii=False, indent=2)


# audio()
# video()
three()
