import subprocess as sp

resp=sp.check_output(["echo","-"], stdin=open('haha.txt', 'w'))

