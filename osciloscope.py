import nicenquickplotlib as nq # https://github.com/SengerM/nicenquickplotlib
import sounddevice as sd
import numpy as np
from utils import *

import os
os.system('clear')
# Parameters -----------------------------------------------------------
AMPLITUDE = 1 # Amplitude of the signal between 0 and 1.
SIGNAL_FREQUENCY = 1000 # In Hertz.
N_CYCLES = 1000 # This must be "a great number" to overcome a strange transitory of the sound card...
SAMPLING_FREQUENCY = 48000 # Must be integer.
FREQUENCY_DELTA = SIGNAL_FREQUENCY
# ----------------------------------------------------------------------
samples = np.sin(2*np.pi*np.arange(SAMPLING_FREQUENCY/SIGNAL_FREQUENCY)*SIGNAL_FREQUENCY/SAMPLING_FREQUENCY)
# Create the output samples ---------------------
output_samples = samples
for k in range(N_CYCLES-1):
	output_samples = np.append(output_samples, samples)
# Play and record samples -----------------------
recorded_samples = sd.playrec(output_samples, SAMPLING_FREQUENCY, channels=2)
sd.wait()
recorded_samples = np.transpose(recorded_samples)
time = np.linspace(0,N_CYCLES/SIGNAL_FREQUENCY,len(output_samples))
# Calculate FFT --------------------------------------------------------
samples_FFT = np.fft.rfft(output_samples)
recorded_FFT = np.fft.rfft(recorded_samples[0])
samples_FFT = np.absolute(samples_FFT)
recorded_FFT = np.absolute(recorded_FFT)
# Plot recorded signals ------------------------------------------------
# ~ nq.plot(time, [output_samples, recorded_samples[0]], together=False)
nq.plot(
	[np.log(samples_FFT)*20, np.log(recorded_FFT)*20], 
	together=False,
	marker='.',
	xlabel='Frecuency (Hz)',
	title='FFT')
# Calculate SNR --------------------------------------------------------
print('20*log(SNR) = ' + str(np.log(calculate_SNR(recorded_samples[0]))*20))
print('SNR = ' + str(calculate_SNR(recorded_samples[0])))

nq.show()
