import mediapy as mp

mp.record_file_by_time('0', '0', 'a.matroska', rate=30, duration=10, show_log=False)
print('record over')
mp.play('a.matroska')
