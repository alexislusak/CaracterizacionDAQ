# -*- coding: utf-8 -*-
"""
Created on Tue Oct  9 17:49:05 2018

@author: admin
"""

import nidaqmx
import numpy as np
import matplotlib.pyplot as plt
import visa
import datetime

FS = 1000
amplitude = 1.2
offset = amplitude/2
frequencies=np.linspace(1,3000,20)

rm = visa.ResourceManager()
fungen = rm.open_resource('USB0::0x0699::0x0346::C036493::INSTR')

fungen.write('voltage {}'.format(amplitude))
fungen.write('voltage:offset {}'.format(offset))
fungen.write('source1:function:shape sin')

frequencies_out = [None]*len(frequencies)
for i in range(len(frequencies)):
    fungen.write(':frequency:fixed {}'.format(frequencies[i])) #sets function generator frequency
    
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan("Dev4/ai0")
        task.timing.cfg_samp_clk_timing(rate=FS)
        data = task.read(number_of_samples_per_channel=1000)
    frequencies_out[i] = np.argmax(np.abs(np.fft.fft(data)))*FS

plt.plot(frequencies, frequencies_out)
plt.show()

fungen.close()