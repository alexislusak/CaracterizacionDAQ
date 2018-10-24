import numpy as np
import visa
import time
import cool_functions as cf
import nicenquickplotlib as nq # https://github.com/SengerM/nicenquickplotlib

REFERENCE_SIGNAL = 0.5
SAMPLING_FREQUENCY = 10000
GENERATOR_AMPLITUDE = 2.5 # volt
N_CYCLES = 4

def measure_freq(fungen, little_board, sampling_frequency=SAMPLING_FREQUENCY):
    fungen.write('OUTP1:IMP INF') # Set the output impedance to zero (infinite load impedance).
    fungen.write('voltage 20e-3')
    fungen.write('voltage:offset {}'.format(GENERATOR_AMPLITUDE))
    fungen.write('source1:function:shape squ')
    fungen.write('OUTP1:STAT ON')
    time.sleep(1)
    data = np.array(little_board.acquire(sampling_frequency=sampling_frequency))
    fungen.write('OUTP1:STAT OFF')
    data -= data.mean()
    signal_fft = np.abs(np.fft.fft(data))
    signal_fft = signal_fft[:int(len(signal_fft)/2)]
    return np.argmax(signal_fft)*sampling_frequency/len(signal_fft)/2

rm = visa.ResourceManager()
rm.list_resources()
fungen = rm.open_resource('USB0::0x0699::0x0346::C036492::INSTR')

little_board = cf.Little_Board('Dev11')

freq = measure_freq(fungen, little_board)
print(freq)

fungen.close()
