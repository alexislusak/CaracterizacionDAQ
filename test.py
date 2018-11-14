import nicenquickplotlib as nq # https://github.com/SengerM/nicenquickplotlib
import sounddevice as sd
import numpy as np
import os
import time
from utils import *
from pid import *

# Parameters -----------------------------------------------------------
DESIRED_SNR = 200 # Not dB!
MAX_SNR = 2400
MIN_SNR = 0
SIGNAL_FREQUENCY = 800 # In Hertz.
SAMPLING_FREQUENCY = 48000 # Must be integer.
MIN_CHUNK_SIZE = 2**9 # Minimum chunk size.
# ----------------------------------------------------------------------

PURE_SAMPLES = np.sin(2*np.pi*np.arange(SAMPLING_FREQUENCY/SIGNAL_FREQUENCY)*SIGNAL_FREQUENCY/SAMPLING_FREQUENCY)
while len(PURE_SAMPLES) < MIN_CHUNK_SIZE:
	PURE_SAMPLES = np.append(PURE_SAMPLES, PURE_SAMPLES)
PURE_SAMPLES = PURE_SAMPLES.transpose()

def create_callback(): # Esto es una función que devuelve una funcion... Es la "función constructora".
	pid = PID(kP=0.5, kI=0.5, kD=0.1) # El objeto "pid" es instanciado y luego queda viviendo en un lugar mágico del más allá.
	pid.set_point = mapp(DESIRED_SNR, MIN_SNR, MAX_SNR, -1, 1)
	pid.print_config()
	def callback(indata, outdata, frames, time, status): # Prototipo del callback de sounddevice.
		# ~ print('---')
		SNR = calculate_SNR(indata.transpose()[0])
		amplitude = mapp(pid.get_control(mapp(SNR, MIN_SNR, MAX_SNR, -1, 1)), -1, 1, 0, 1)
		outdata[:] = amplitude*PURE_SAMPLES.reshape(len(PURE_SAMPLES),1)
		print('SP={:.2f}   '.format(DESIRED_SNR) + 'SNR={:.2f}   '.format(SNR) + 'eSNR={:.2f}   '.format(DESIRED_SNR - SNR) + 'a={:.3f}   '.format(amplitude))
	return callback

stream = sd.Stream(
	samplerate=SAMPLING_FREQUENCY, 
	callback=create_callback(), 
	blocksize=len(PURE_SAMPLES), 
	channels=1)

stream.start()
while True:
	time.sleep(1)
stream.stop()
