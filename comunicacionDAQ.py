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

rm = visa.ResourceManager()
# rm.list_resources()
fungen = rm.open_resource('USB0::0x0699::0x0346::C034167::INSTR')

fungen.write('voltage {}'.format(amplitude))
fungen.write('voltage:offset {}'.format(offset))
fungen.write('source1:function:shape sin')

little_board = cf.Little_Board('Dev7')

frequencies_out = [None]*len(frequencies)
fungen.write('OUTP1:STAT ON')
time.sleep(1)
for i in range(len(frequencies)):
    fungen.write(':frequency:fixed {}'.format(frequencies[i])) #sets function generator frequency
    data = np.array(little_board.acquire(n_samples=1000, sampling_frequency=FS,ch0=False,ch1=True))
    data -= data.mean()
    signal_fft = np.abs(np.fft.fft(data))
    signal_fft = signal_fft[:int(len(signal_fft)/2)]
    frequencies_out[i] = np.argmax(signal_fft)*FS/len(signal_fft)/2
    nq.plot(np.array(data))
    nq.plot(np.linspace(0,FS/2,len(signal_fft)), signal_fft, title=str(1+i)+'_fft', xlabel='Frecuencia (Hz)')
fungen.write('OUTP1:STAT OFF')
fungen.close()

nq.plot(np.array(frequencies), np.array(frequencies_out), marker='.', xlabel='Frecuencia del generador (Hz)', ylabel='Frecuencia detectada (Hz)', title='Aliassing')

#nq.save_all(timestamp=True)

