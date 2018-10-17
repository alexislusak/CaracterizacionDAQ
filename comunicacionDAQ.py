import numpy as np
import matplotlib.pyplot as plt
import visa
import time
import cool_functions as cf
import nicenquickplotlib as nq # https://github.com/SengerM/nicenquickplotlib

nq.default_file_format = 'pdf'

FS = 1537
amplitude = 1.2
offset = amplitude/2
frequencies=np.linspace(1,3000,20)
frequencies_out = [None]*len(frequencies)

little_board = cf.Little_Board('Dev10')
fungen= cf.fungen('USB0::0x0699::0x0346::C034167::INSTR')

fungen.on_off(channel='OUTP1',status='ON')
time.sleep(1)

for i in range(len(frequencies)):
    fungen.write(amplitude=amplitude,offset=offset,function='sin',frequencies=frequencies[i]) #sets function generator frequency
    data = np.array(little_board.acquire(n_samples=1000, sampling_frequency=FS,ch0=False,ch1=True))
    data -= data.mean()
    signal_fft = np.abs(np.fft.fft(data))
    signal_fft = signal_fft[:int(len(signal_fft)/2)]
    frequencies_out[i] = np.argmax(signal_fft)*FS/len(signal_fft)/2
    nq.plot(np.array(data))
    nq.plot(np.linspace(0,FS/2,len(signal_fft)), signal_fft, title=str(1+i)+'_fft', xlabel='Frecuencia (Hz)')

fungen.on_off(channel='OUTP1',status='OFF')

nq.plot(np.array(frequencies), np.array(frequencies_out), marker='.', xlabel='Frecuencia del generador (Hz)', ylabel='Frecuencia detectada (Hz)', title='Aliassing')

nq.save_all(timestamp=True)

