import mediapy as mp

rate = 20
p = mp.get_record_pipe('0', '1', rate, show_log=False)
frame_shape = (720, 1280, 3)
reader = mp.get_reader('-', mp.MediaType.video, p.output_meta.frame_shape)
reader = mp.connect_pipe(p, reader)
writer = mp.get_writer('-', p.output_meta.dtype, p.output_meta.frame_shape, mp.matroska, rate=rate, media_type=mp.MediaType.video)
pp = mp.play_pipe(writer)
while 1:
    img = reader.read(1)
    if img is None:
        break
    img = 255 - img
    writer.write(img)
