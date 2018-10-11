import numpy as np
import matplotlib.pyplot as plt
import visa
import time
import cool_functions as cf

FS = 10000
amplitude = 1.2
offset = amplitude/2
SIGNAL_FREQUENCY = 1e3 # Hz

rm = visa.ResourceManager()
# rm.list_resources()
fungen = rm.open_resource('USB0::0x0699::0x0346::C034167::INSTR')

fungen.write('voltage {}'.format(amplitude))
fungen.write('voltage:offset {}'.format(offset))
fungen.write('source1:function:shape sin')

fungen.write(':frequency:fixed {}'.format(SIGNAL_FREQUENCY)) #sets function generator frequency

fungen.write('OUTP1:STAT ON')
time.sleep(1)
little_board = cf.Little_Board('Dev10')
data = little_board.acquire(3, FS, ch1=True)
print(data)
fungen.write('OUTP1:STAT OFF')
fungen.close()

plt.plot(data)
plt.show()

