import numpy as np
import math

def sign(x):
    s = 1 if x>=0 else  -1
    return s

def abs(x):
    return x * sign(x)

def EigenGeneration(signal):
    length, width = signal.shape
    print(width, length)
    power = np.zeros(length)
    amp = np.zeros(length)
    zero_pass = np.zeros(length)


    for i in range(length):
        for j in range(width):
            x = signal[i][j]
            power[i] += x*x
            amp[i] += abs(x)
            if (j<width-1):
                zero_pass[i] += abs(sign(signal[i][j+1])-sign(x))
                # print(zero_pass)
        power[i] /= width
        amp[i] /= width
        zero_pass[i] /= 2
    
    return (power, amp, zero_pass)

wave = np.random.randn(3,5)
print(wave)
p, a, z =EigenGeneration(wave)
print(p, a, z)

