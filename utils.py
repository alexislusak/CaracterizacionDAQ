import numpy as np

def calculate_SNR(samples):
	if not isinstance(samples, np.ndarray):
		raise ValueError('"samples" must be a numpy.ndarray object')
	if len(samples.shape) is not 1:
		raise ValueError('"samples" must be a one dimensional array')
	fft = np.absolute(np.fft.rfft(samples))
	return fft[fft.argmax()]/fft.mean()

def mapp(number, from_min, from_max, to_min, to_max):
	number = (number-from_min)/(from_max-from_min)*(to_max-to_min) + to_min
	if number < to_min:
		number = to_min
	if number > to_max:
		number = to_max
	return number
