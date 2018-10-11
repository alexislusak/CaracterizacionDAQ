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

little_board = cf.Little_Board('Dev10')

fungen.write('OUTP1:STAT ON')
time.sleep(1)
for i in range(len(frequencies)):
    fungen.write(':frequency:fixed {}'.format(frequencies[i])) #sets function generator frequency
    data = np.array(little_board.acquire(n_samples=1000, sampling_frequency=FS,ch0=True,ch1=True))
    signal_fft = [None]*len(data)
    for k in range(len(data)):
        data[k] -= data[k].mean()
        signal_fft[k] = np.abs(np.fft.fft(data[k]))
        signal_fft[k] = signal_fft[k][:int(len(signal_fft[k])/2)]
        nq.plot(np.array(data[k]), title=str(i) + ' CH ' + str(k) + ' at freq=' + str(frequencies[i]))
        nq.plot(np.linspace(0,FS/2,len(signal_fft[k])), signal_fft[k], title=str(1+i)+' FFT CH' + str(k) , xlabel='Frecuencia (Hz)')
    nq.plot(np.linspace(0,FS/2,len(signal_fft[k])), [signal_fft[0], signal_fft[1]], legend=['CH0', 'CH1'], title=str(1+i)+' los dos canales juntos' , xlabel='Frecuencia (Hz)')

fungen.write('OUTP1:STAT OFF')
fungen.close()
nq.save_all(timestamp=True)

