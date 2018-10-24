# -*- coding: utf-8 -*-
"""
Created on Wed Oct 24 16:17:45 2018

@author: Publico
"""

import numpy as np
import visa
import time
import cool_functions as cf
import nicenquickplotlib as nq # https://github.com/SengerM/nicenquickplotlib


N_SAMPLES = 1000 # Max 1024
SAMPLING_FREQUENCY = 8000


rm = visa.ResourceManager()
rm.list_resources()

little_board = cf.Little_Board('Dev11')

time.sleep(1)
data = np.array(little_board.acquire(n_samples=N_SAMPLES, sampling_frequency=SAMPLING_FREQUENCY,ch0=True,ch1=False))

time_axis = np.linspace(0,N_SAMPLES/SAMPLING_FREQUENCY,N_SAMPLES)
nq.plot(x=time_axis, y=np.array(data), xlabel='Tiempo (s)')

nq.save_all(timestamp=True, image_format='pdf', csv=True)
nq.show()