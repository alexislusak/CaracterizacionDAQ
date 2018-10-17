import nidaqmx

class Little_Board:
    def __init__(self, usb_port):
        self.usb_port = usb_port
    
    def acquire(self, n_samples=1000, sampling_frequency=1000, ch0=True, ch1=False):
        with nidaqmx.Task() as task:
            if ch0 is True:
                task.ai_channels.add_ai_voltage_chan("%s/%s" % (self.usb_port, "ai0"))
            if ch1 is True:
                task.ai_channels.add_ai_voltage_chan("%s/%s" % (self.usb_port, "ai1"))
            task.timing.cfg_samp_clk_timing(rate=sampling_frequency)
            return task.read(number_of_samples_per_channel=n_samples)
   
import visa
     
class fungen:
    def __init__(self,usb_port):
        self.usb_port = usb_port
        
    def write(self, amplitude, offset, function, frequencies): #functions as: sin, sqrt
        rm = visa.ResourceManager()
        # rm.list_resources()
        fungen = rm.open_resource('%s' %self.usb_port)
        fungen.write('voltage {}'.format(amplitude))
        fungen.write('voltage:offset {}'.format(offset))
        fungen.write('source1:function:shape %s' %function)
        fungen.write(':frequency:fixed {}'.format(frequencies))
        fungen.close()
        
    def on_off(self,channel,status): #channel OUTP1 __ status: on / off
        rm = visa.ResourceManager()
        fungen = rm.open_resource('%s' %self.usb_port)
        fungen.write('%s :STAT %s' %(channel,status))
        fungen.close()