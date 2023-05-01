import json
from pprint import pprint

import mediapy as m
import mediapy as mp


def test_video():
    resp = m.probe("../imgs/taylor.mp4")
    json.dump(resp, open('haha.json', 'w'), ensure_ascii=False, indent=2)


def test_audio():
    pprint(m.probe("../imgs/taylor.mp3"))
    pprint(m.get_meta("taylor.mp3"))


def test_three():
    info = m.get_meta('./a.matroska')
    print(info.video_stream)
    json.dump(info.video_stream.dict(), open('haha.json', 'w'), ensure_ascii=False, indent=2)


def test_record_metainfo():
    meta, a = mp.read('a.matroska')
    print(meta.video_stream)
    print(len(a) / meta.frame_rate(), meta.frame_rate(), '时长')
    print(a.shape)
