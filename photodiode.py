import numpy as np
import matplotlib.pyplot as plt
import visa
import time
import cool_functions as cf
import nicenquickplotlib as nq # https://github.com/SengerM/nicenquickplotlib

GENERATOR_FREQUENCY = 20 # Hz
GENERATOR_AMPLITUDE = 2.5 # volt
N_SAMPLES = 1000 # Max 1024
N_CYCLES = 4


rm = visa.ResourceManager()
# rm.list_resources()
fungen = rm.open_resource('USB0::0x0699::0x0346::C034167::INSTR')

fungen.write('OUTP1:IMP INF') # Set the output impedance to zero (infinite load impedance).
fungen.write('voltage {}'.format(GENERATOR_AMPLITUDE))
fungen.write('voltage:offset {}'.format(GENERATOR_AMPLITUDE/2))
fungen.write(':frequency:fixed {}'.format(GENERATOR_FREQUENCY)) #sets function generator frequency
fungen.write('source1:function:shape squ')

little_board = cf.Little_Board('Dev10')

fungen.write('OUTP1:STAT ON')
time.sleep(1)
data = np.array(little_board.acquire(n_samples=N_SAMPLES, sampling_frequency=GENERATOR_FREQUENCY*N_SAMPLES/N_CYCLES,ch0=True,ch1=True))

time_axis = np.linspace(0,N_CYCLES/GENERATOR_FREQUENCY,N_SAMPLES)
nq.plot(x=time_axis, y=[np.array(data[0]), np.array(data[1])], together=False, xlabel='Tiempo (s)')

fungen.write('OUTP1:STAT OFF')
fungen.close()

nq.save_all(timestamp=True, image_format='pdf', csv=True)
nq.show()


fungen.write('OUTP1:STAT ON')
time.sleep(1)
data = np.array(little_board.acquire(n_samples=N_SAMPLES, sampling_frequency=GENERATOR_FREQUENCY*N_SAMPLES/N_CYCLES,ch0=True,ch1=True))

time_axis = np.linspace(0,N_CYCLES/GENERATOR_FREQUENCY,N_SAMPLES)
nq.plot(x=time_axis, y=[np.array(data[0]), np.array(data[1])], together=False, xlabel='Tiempo (s)')

fungen.write('OUTP1:STAT OFF')
fungen.close()

nq.save_all(timestamp=True)

