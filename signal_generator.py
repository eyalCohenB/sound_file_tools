import numpy as np
from scipy.io.wavfile import write
import os

def create_chirp_signal(sample_rate,start_freq,end_freq,signal_duration,silence_duration,repeat,amplitude):
    t = np.linspace(0, signal_duration, int(sample_rate * signal_duration), endpoint=False)
    freqs = np.linspace(start_freq, (start_freq+end_freq)/2, len(t))
    sin_waveform = amplitude *  (np.sin(2 * np.pi * freqs * t).astype(np.float32))
    silence = np.zeros(int(sample_rate * silence_duration), dtype=np.float32)
    data_with_silence = np.concatenate([sin_waveform, silence] * repeat)
    return data_with_silence

def create_cw_signal(sample_rate,start_freq,signal_duration,silence_duration,repeat,amplitude):
    t = np.linspace(0, signal_duration, int(sample_rate * signal_duration), endpoint=False)
    sin_waveform = amplitude *  (np.sin(2 * np.pi * start_freq * t).astype(np.float32))
    silence = np.zeros(int(sample_rate * silence_duration), dtype=np.float32)
    data_with_silence = np.concatenate([sin_waveform, silence] * repeat)
    return data_with_silence


def saveWav(path,fileName, sample_rate,data_with_silence):
    #Save to .wav file
    write(os.path.join(path,fileName), sample_rate, data_with_silence)


def chirp_cw_creator(sample_rate,start_freq,end_freq,signal_duration,silence_duration,repeat,amplitude,path):
    fileName = 'chirp_' + str(int(start_freq)//1000) + 'k_' + str(int(end_freq)//1000) + 'k.wav'
    if int(start_freq) == int(end_freq):
        fileName = 'cw_' + str(int(start_freq)//1000) + 'k.wav'
    
    data_to_save = create_chirp_signal(int(sample_rate),int(start_freq),int(end_freq),float(signal_duration),float(silence_duration),int(repeat),amplitude)

    saveWav(path,fileName, int(sample_rate),data_to_save)
    print('Saved file to: '+ os.path.join(path,fileName))

def cwinc_creator(sample_rate,start_freq,end_freq,signal_duration,silence_duration,repeat,amplitude,path):
    fileName = 'cw_' + str(int(start_freq/1000)) +'k' + '-' + str(int(end_freq/1000)) +'k.wav'
    
    data_to_save =  np.zeros(sample_rate , dtype=np.float32) # start every file with alittle silence to let hydrophones amp up
    loop_repeats = int((end_freq - start_freq) // 1000)
    # print("loop_repeats",loop_repeats)
    if loop_repeats == 0:
        data_to_save = np.concatenate([data_to_save,create_cw_signal(sample_rate,start_freq,signal_duration,silence_duration,repeat,amplitude)])
    for _ in range(loop_repeats):
        # data_to_save_tmp = create_cw_signal(sample_rate,start_freq,signal_duration,silence_duration,repeat,amplitude)
        # silence = np.zeros(float(sample_rate * 5), dtype=np.float32) # if u want extra pauses between signals
        # data_to_save = np.concatenate([data_to_save,data_to_save_tmp])
        data_to_save = np.concatenate([data_to_save,create_cw_signal(sample_rate,start_freq,signal_duration,silence_duration,repeat,amplitude)])
        start_freq += 1000
    
    saveWav(path,fileName, sample_rate,data_to_save)
    print('Saved file to: '+ os.path.join(path,fileName))

def main():
        
    signal_type = input("Which signal do you want to create? (chirp / cw / cwinc): ")
    while signal_type not in ["chirp" , "cw" , "cwinc"]:
        signal_type = input("Incorrect signal type, which signal do you want to create? (chirp / cw / cwinc): ")

    if signal_type == "chirp": #[ "chirp" , "cw"]:
        # print("Enter Values as instructed to create a Chirp or CW signal.\nNote: if you want to create a CW,\nsimply enter the same values for start & end frequency.")
        print("Enter Values as instructed to create a Chirp .")
    elif signal_type == "cw":
        print("Enter Values as instructed to create a CW signal.\nsimply entering the same values for start & end frequency will result in a CW.")
    else:
        print("Enter Values as instructed to create an increasing CW.\nNote: if you want to create a simple CW(not increasing),\nsimply enter the same values for start & end frequency.")

    #dynamic vars
    sample_rate = int(float(input("Sample Rate(KHz): ")) * 1000)
    start_freq = int(float(input("Start Frequency(Khz): ")) * 1000)
    end_freq = int(float(input("End Frequency(Khz): ")) * 1000)
    signal_duration = float(input("Signal Duration(sec): "))
    silence_duration = float(input("Silence Duration(sec): "))
    repeat = int(input("Repeat[int, times signal is repeated (if cwinc than at each frequency)]:"))
    #static vars
    amplitude = 0.5 # amp is risky, try to keep <= 0.5
    path = os.getcwd()
    path = path.replace("\\","/")
    # User Verification
    print("\nYou Chose:")
    print("signal type:",signal_type)
    print("sample rate:",sample_rate)
    print("start freq:",start_freq)
    print("end freq:",end_freq)
    print("signal duration:",signal_duration)
    print("silence duration:",silence_duration)
    print("repeated signals at each frequency:",repeat)
    valid_falg = input("Create '.wav' file? (y/n): ")
    if valid_falg == "y":
        if signal_type in ["chirp" , "cw"]:
            #***Chirp Or CW Activation***
            chirp_cw_creator(sample_rate,start_freq,end_freq,signal_duration,silence_duration,repeat,amplitude,path)
        else:
            #***CW invremented Activation***
            cwinc_creator(sample_rate,start_freq,end_freq,signal_duration,silence_duration,repeat,amplitude,path)
    else:
        main()

if __name__ == "__main__":
    main()