from scipy import signal
a=signal.fftconvolve([1,2,3],[4,5,6])#右面是低位，左面是高位
print(a)