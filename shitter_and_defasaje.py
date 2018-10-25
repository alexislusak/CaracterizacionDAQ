import numpy as np
import visa
import time
import cool_functions as cf
import nicenquickplotlib as nq # https://github.com/SengerM/nicenquickplotlib

GENERATOR_FREQUENCY = 20 # Hz
SAMPLING_FREQUENCIES = [100, 1000, 10e3, 48e3/2] # Maximum sampling rate = 48 kSPS
GENERATOR_AMPLITUDE = 2.5 # volt
N_SAMPLES = 1000 # Max 1024

rm = visa.ResourceManager()
rm.list_resources()
fungen = rm.open_resource('USB0::0x0699::0x0346::C036492::INSTR')

fungen.write('OUTP1:IMP INF') # Set the output impedance to zero (infinite load impedance).
fungen.write('voltage {}'.format(GENERATOR_AMPLITUDE))
fungen.write('voltage:offset {}'.format(GENERATOR_AMPLITUDE/2))
fungen.write(':frequency:fixed {}'.format(GENERATOR_FREQUENCY)) #sets function generator frequency
fungen.write('source1:function:shape squ')

little_board = cf.Little_Board('Dev11')

fungen.write('OUTP1:STAT ON')
time.sleep(1)
for k in range(len(SAMPLING_FREQUENCIES)):
	data = np.array(little_board.acquire(n_samples=N_SAMPLES, sampling_frequency=SAMPLING_FREQUENCIES[k],ch0=True,ch1=True))
	time_axis = np.linspace(0,N_SAMPLES/SAMPLING_FREQUENCIES[k],N_SAMPLES)
	nq.plot(x=time_axis, y=[np.array(data[0]), np.array(data[1]), np.array(data[0])-np.array(data[1])], marker='.', together=False, xlabel='Tiempo (s)', title='fs = ' + str(SAMPLING_FREQUENCIES[k]))
fungen.write('OUTP1:STAT OFF')
fungen.close()

nq.save_all(timestamp='now', image_format='pdf', csv=True)
nq.show()

