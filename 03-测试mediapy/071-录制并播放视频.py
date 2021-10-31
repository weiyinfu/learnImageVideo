import mediapy as mp

p = mp.get_record_pipe('0', '1', show_log=False)
pp = mp.play_pipe(p)
pp.join()
