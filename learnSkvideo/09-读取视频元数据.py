import json

import skvideo.datasets
import skvideo.io

metadata = skvideo.io.ffprobe(skvideo.datasets.bigbuckbunny())
print(type(metadata))
print(json.dumps(metadata, indent=4))
