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