import numpy as np
from scipy.io.wavfile import write

def generateSignal(sample_rate,start_freq,end_freq,signal_duration,interval,repeat,amplitude):
    t = np.linspace(0, signal_duration, int(sample_rate * signal_duration), endpoint=False)
    freqs = np.linspace(start_freq, (start_freq+end_freq)/2, len(t))
    sin_waveform = amplitude *  (np.sin(2 * np.pi * freqs * t).astype(np.float32))
    silence = np.zeros(int(sample_rate * interval), dtype=np.float32)
    data_with_intervals = np.concatenate([sin_waveform, silence] * repeat)
    return data_with_intervals

def saveWav(path,fileName, sample_rate,data_with_intervals):
    #Save to .wav file
    write(path + fileName, sample_rate, data_with_intervals)


if __name__ == "__main__":

    #****Variables****
    #dynamic vars
    sample_rate , start_freq , end_freq , signal_duration , interval , repeat = input('Enter in this order: sample rate, start-freq, end-freq, signal duration(in sec), interval duration(in sec), repeat .\n').split(' ')
    
    #static vars
    amplitude = 0.5
    path = ''
    fileName = 'chirp_' + str(int(start_freq)//1000) + 'k-' + str(int(end_freq)//1000) + 'k.wav'
    if int(start_freq) == int(end_freq):
        fileName = 'cw_' + str(int(start_freq)//1000) + 'k.wav'

    #***Activation***
    data_to_save = generateSignal(int(sample_rate),int(start_freq),int(end_freq),float(signal_duration),float(interval),int(repeat),amplitude)
    saveWav(path,fileName, int(sample_rate),data_to_save)
    print('Saved file to: '+ path + fileName)
