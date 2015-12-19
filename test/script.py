import scipy.signal as sig
import scipy.fftpack as fft
import numpy
import pylab
import matplotlib.pyplot as plt


data = open("../data/0930/60.txt", "r+").read()

array_x = []
array_y = []
x = 0

for d in data.split('\n'):
    if d:
        delta_x, y = d.split("\t")
        delta_x = float(delta_x)
        y = float(y)
        x = x + delta_x
        array_x.append(x)
        array_y.append(y)




print (array_x)
print (len(array_y))

print(len(sig.medfilt(sig.wiener(array_y))))


plt.figure(1)
plt.subplot(311)
plt.title("Before")
plt.plot(array_x, array_y)

plt.subplot(312)
plt.title("After")
plt.plot(array_x, sig.medfilt(array_y))

M = len(array_y)

Spectrum = fft.fft(array_y)

[Low_cutoff, High_cutoff, F_sample] = map(float, [0,50,500])

[Low_point, High_point] = map(lambda F:F/F_sample * M /2, [Low_cutoff, High_cutoff])

Filtered_spectrum = [Spectrum[i] if i>= Low_point and i<= High_point else 0.0 for i in xrange(M)]

Filtered_signal = fft.ifft(Filtered_spectrum, n=M)

plt.subplot(313)

print (len(Filtered_signal))

plt.plot(array_x, Filtered_signal)



#minimum_y = Filtered_signal.min()
#minumum_x = array_x[Filtered_signal.argmin()]
#plt.plot(minumum_x, minimum_y, "or")

print(Filtered_signal.argmin())

#plt.show()



working_wave = Filtered_signal
step = 30
threshold = 0.4
derive = []
division = []

for i in range(1, len(working_wave)-step-1, step):
    print i+step, i
    print abs(working_wave[i+step]-working_wave[i])
    if abs(working_wave[i] - working_wave[i+step]) >= threshold:
        division.append((i, i+step))
        plt.axvline(array_x[i])
        plt.axvline(array_x[i+step])

print division

for divide in division:
    start = divide[0]
    end = divide[1]
    minimum_y = Filtered_signal[start:end].min()
    minumum_x = array_x[start + Filtered_signal[start:end].argmin()]
    plt.plot(minumum_x, minimum_y, "or")



plt.show()



