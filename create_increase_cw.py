import numpy as np
import os
from scipy.io.wavfile import write

def generateSignal(sample_rate,start_freq,signal_duration,silence_duration,repeat,amplitude):
    t = np.linspace(signal_duration, int(sample_rate * signal_duration), endpoint=False)
    freqs = np.linspace(start=start_freq,stop=start_freq, num=len(t))
    sin_waveform = amplitude *  (np.sin(2 * np.pi * freqs * t).astype(np.float32))
    silence = np.zeros(int(sample_rate * silence_duration), dtype=np.float32)
    data_with_silence_durations = np.concatenate([sin_waveform, silence] * repeat)
    return data_with_silence_durations

def saveWav( path , fileName , sample_rate , data_to_save ):
    #Save to .wav file
    write( os.path.join(path,fileName) , int(sample_rate) , data_to_save )


def main():
    #****Variables****
    #dynamic vars
    print("Enter Values as instructed to create an increasing cw.\nNote: if you want to create a simple CW(not increasing),\nsimply enter the same values for start & end frequency.")
    sample_rate = int(float(input("Sample Rate(kilo): ")) * 1000)
    start_freq = int(float(input("Start Frequency(kilo): ")) * 1000)
    end_freq = int(float(input("End Frequency(kilo): ")) * 1000)
    signal_duration = float(input("Signal Duration(sec): "))
    silence_duration = float(input("Silence Duration(sec): "))
    repeat = int(input("Repeat(int, times signal is repeated on each frequency): "))
    #static vars
    amplitude = 0.5 # amp is risky, try to keep <= 0.5
    path = os.getcwd()
    path = path.replace("\\","/")
    fileName = 'cw_' + str(int(start_freq/1000)) +'k' + '-' + str(int(end_freq/1000)) +'k.wav'
    print("\nYou Chose:")
    print("sample rate: ",sample_rate)
    print("start freq: ",start_freq)
    print("end freq: ",end_freq)
    print("signal duration: ",signal_duration)
    print("silence duration: ",silence_duration)
    print("repeat: ",repeat)
    valid_falg = input("Create '.wav' file? (y/n): ")
    if valid_falg == "y":
        #***Activation***
        #data_to_save = generateSignal(float(sample_rate),float(start_freq),float(signal_duration),float(silence_duration),int(repeat),amplitude)
        data_to_save =  np.zeros(sample_rate , dtype=np.float32) # start every file with alittle silence to let hydrophones amp up
        loop_repeats = int((end_freq - start_freq) // 1000)
        if loop_repeats == 0:
            data_to_save = np.concatenate([data_to_save,generateSignal(sample_rate,start_freq,signal_duration,silence_duration,repeat,amplitude)])
        for _ in range(loop_repeats):
            data_to_save_tmp = generateSignal(sample_rate,start_freq,signal_duration,silence_duration,repeat,amplitude)
            # silence = np.zeros(float(sample_rate * 5), dtype=np.float32) # if u want extra pauses between signals
            data_to_save = np.concatenate([data_to_save,data_to_save_tmp])
            start_freq += 1000
        
        #print(data_to_save)

        saveWav(path,fileName, sample_rate,data_to_save)
        print('Saved file to: '+ os.path.join(path,fileName))
        pass
    else:
        main()

if __name__ == "__main__":
    main()
    