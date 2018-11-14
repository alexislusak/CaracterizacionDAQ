import numpy as np
import visa
import time
import cool_functions as cf
import nicenquickplotlib as nq # https://github.com/SengerM/nicenquickplotlib
 
#REFERENCE_SIGNAL = 0.5
SAMPLING_FREQUENCY = 1000
GENERATOR_AMPLITUDE = 2.5 # volt
N_CYCLES = 4
N_SAMPLES_PER_BURST = 1000
DUTY_CYCLE = 0.5
KP = 0.5
KI = 0.01
KD = 0

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

fungen.write('OUTP1:IMP INF') # Set the output impedance to zero (infinite load impedance).
fungen.write('voltage {}'.format(GENERATOR_AMPLITUDE))
fungen.write('voltage:offset {}'.format(GENERATOR_AMPLITUDE/2))
fungen.write(':frequency:fixed {}'.format(freq)) #sets function generator frequency
fungen.write('source1:function:shape PULS')
fungen.write('source1:PULS:WIDT ' + str(DUTY_CYCLE/freq) + 's')
fungen.write('OUTP1:STAT ON')
time.sleep(1)

REFERENCE_SIGNAL = 1/(2*freq)
error_integral = 0
error_signal_n_menos_uno = 0
error_signal = 0
generator_phase = 1/(2*freq)
fungen.write('source1:PULSE:DELAY ' + str(generator_phase) + ' S')
while True:
    data = np.array(little_board.acquire(n_samples=N_SAMPLES_PER_BURST,sampling_frequency=freq*N_SAMPLES_PER_BURST))
    data -= data.min()
    data /= data.max()
    data = data.round()
    data *= -1
    data += 1
    duty = data.sum()/(freq*len(data))
    error_signal_n_menos_uno = error_signal
    error_signal = REFERENCE_SIGNAL - duty
    error_integral += error_signal
    error_derivative = error_signal - error_signal_n_menos_uno
    
    generator_phase = 1/(2*freq) - (KP*error_signal + KI*error_integral + KD*error_derivative)
    if generator_phase > 1/freq:
        generator_phase=generator_phase%(1/freq)
    if generator_phase < 0:
        generator_phase=1/freq - np.abs(generator_phase)%(1/freq)
        
    fungen.write('source1:PULSE:DELAY ' + str(generator_phase) + ' S')
    

    print('-----------')
    print('generator_phase = ' + str(generator_phase))
    print('Error signal = ' + str(error_signal))
    print('Error integral = ' + str(error_integral))
    print('Error derivative = ' + str(error_derivative))
        
    
    

fungen.close()
