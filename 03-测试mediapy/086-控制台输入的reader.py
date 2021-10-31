from mediapy.io import *
from mediapy.io import _ffmpeg_common
import pylab as plt

"""
本程序意在证明：ffmpeg从控制台作为输入的时候，许多格式都无法使用。例如mp4等各种格式都会遇到乱码问题。matroska则不存在这个问题。  

在向外写出的时候，同样如此，写出mp4会有问题，而写出matroska则一切正常。  
"""


def get_reader(input_fmt: str, media_type: str, frame_shape: Union[Tuple[int], List[int]], out_audio_fmt='s16e', out_pix_fmt='rgb24', show_log=False) -> ArrayPipe:
    global_options = []
    _ffmpeg_common(global_options, show_log)
    output_options = []
    output_options.extend([
        '-f', 'image2pipe',
        '-pix_fmt', out_pix_fmt,
        '-vcodec', 'rawvideo',
    ])
    dtype = np.uint8
    # in_options = ['-f', input_fmt, '-pix_fmt', 'yuv420p']
    input_options = [
        # '-f', 'matroska',
        # '-r', 30,
        # '-pix_fmt', 'yuv422p',
        # '-video_size', '1280x720',
        # '-vcodec', 'h264',
    ]
    a = ['ffmpeg'] + global_options + input_options + ['-i', '-', ] + output_options + ['-']
    a = [str(i) for i in a]
    logger.info(f"{' '.join(a)} dtype={dtype} shape={frame_shape}")
    p = sp.Popen(a, stdin=sp.PIPE, stdout=sp.PIPE)
    reader = ArrayPipe(cin=p.stdin, cout=p.stdout, output_meta=ArrayMeta(dtype=np.uint8, frame_shape=frame_shape))

    # f = open('../imgs/taylor.mp4', 'rb')
    f = open('./a.matroska', 'rb')
    content = f.read()
    f.close()

    def write():
        block_size = 4096
        for i in range(0, len(content), block_size):
            reader.cin.write(content[i:i + block_size])
        print('write over')
        reader.cin.close()

    def read():
        block_size = 40960
        a = []
        while 1:
            res = reader.cout.read(block_size)
            if res is None or len(res) == 0:
                break
            a.extend(res)
        print('read over')
        print(len(a), len(content))

    print("reader output", reader.output_meta)

    ans = []

    def read2():
        nonlocal ans
        while 1:
            img = reader.read(1)
            if img is None:
                break
            img = img[0]
            ans.append(img)
        print('read over')
        print(len(ans))

    # 使用mp4格式虽然可以读取字节，但是读取array作为reader却是行不通的
    # threads = thread_run([write, read], block=True)
    threads = thread_run([write, read2], block=True)
    for i in threads:
        i.join()
    plt.imshow(ans[0])
    plt.show()
    return reader


reader = get_reader('matroska', MediaType.video, [720, 1280, 3], )
