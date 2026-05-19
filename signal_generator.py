import numpy as np
from scipy.io.wavfile import write
from scipy.signal import chirp
import os
import wave


def create_chirp_signal(sample_rate, start_freq, end_freq, signal_duration,
                        silence_duration, repeat, amplitude):

    n_signal = int(round(sample_rate * signal_duration))
    n_silence = int(round(sample_rate * silence_duration))

    t = np.arange(n_signal, dtype=np.float64) / sample_rate

    signal = chirp(
        t,
        f0=start_freq,
        f1=end_freq,
        t1=signal_duration,
        method="linear",
        phi=-90
    )

    signal = amplitude * signal
    silence = np.zeros(n_silence, dtype=np.float64)

    data = np.concatenate([np.concatenate([signal, silence]) for _ in range(repeat)])
    return data


def create_cw_signal(sample_rate, freq, signal_duration,
                     silence_duration, repeat, amplitude):

    n_signal = int(round(sample_rate * signal_duration))
    n_silence = int(round(sample_rate * silence_duration))

    t = np.arange(n_signal, dtype=np.float64) / sample_rate

    # phi=-90 equivalent: starts at 0 instead of max amplitude
    signal = amplitude * np.sin(2 * np.pi * freq * t)
    silence = np.zeros(n_silence, dtype=np.float64)

    data = np.concatenate([np.concatenate([signal, silence]) for _ in range(repeat)])
    return data


def save_wav_pcm16(path, file_name, sample_rate, data):
    os.makedirs(path, exist_ok=True)

    data = np.asarray(data, dtype=np.float64)

    max_abs = np.max(np.abs(data))
    if max_abs > 1.0:
        print(f"WARNING: signal exceeded +/-1.0, normalizing from {max_abs}")
        data = data / max_abs

    data = np.clip(data, -0.999, 0.999)

    # Add tiny fade-in/fade-out to avoid clicks
    fade_len = min(128, len(data) // 20)
    if fade_len > 0:
        fade = np.linspace(0.0, 1.0, fade_len)
        data[:fade_len] *= fade
        data[-fade_len:] *= fade[::-1]

    data_int16 = np.round(data * 32767).astype("<i2")

    full_path = os.path.join(path, file_name)
    write(full_path, int(sample_rate), data_int16)

    # Verify with Python wave module
    with wave.open(full_path, "rb") as wf:
        print("Saved:", full_path)
        print("channels:", wf.getnchannels())
        print("sample rate:", wf.getframerate())
        print("sample width:", wf.getsampwidth())
        print("frames:", wf.getnframes())

    print("PCM16 min/max:", data_int16.min(), data_int16.max())


def chirp_cw_creator(sample_rate, start_freq, end_freq, signal_duration,
                     silence_duration, repeat, amplitude, path):

    sample_rate = int(sample_rate)
    start_freq = int(start_freq)
    end_freq = int(end_freq)

    if start_freq == end_freq:
        file_name = f"cw_{start_freq // 1000}k_{signal_duration}s_{repeat}-repeats.wav"
        data = create_cw_signal(
            sample_rate, start_freq, signal_duration,
            silence_duration, repeat, amplitude
        )
    else:
        file_name = f"chirp_{start_freq // 1000}k_{end_freq // 1000}k_{signal_duration}s_{repeat}-repeats.wav"
        data = create_chirp_signal(
            sample_rate, start_freq, end_freq, signal_duration,
            silence_duration, repeat, amplitude
        )

    save_wav_pcm16(path, file_name, sample_rate, data)


def cwinc_creator(sample_rate, start_freq, end_freq, signal_duration,
                  silence_duration, repeat, amplitude, path):

    sample_rate = int(sample_rate)
    start_freq = int(start_freq)
    end_freq = int(end_freq)

    file_name = f"cw-inc_{start_freq // 1000}k_{end_freq // 1000}k_{signal_duration}s_{repeat}-repeats.wav"

    parts = []

    # Initial silence
    parts.append(np.zeros(sample_rate, dtype=np.float64))

    freq = start_freq
    while freq <= end_freq:
        parts.append(
            create_cw_signal(
                sample_rate, freq, signal_duration,
                silence_duration, repeat, amplitude
            )
        )
        freq += 1000

    data = np.concatenate(parts)
    save_wav_pcm16(path, file_name, sample_rate, data)


def create_signal_main(signal_type=None, sample_rate=None, start_freq=None,
                       end_freq=None, signal_duration=None,
                       silence_duration=None, repeat=None):

    if signal_type is None:
        signal_type = input("Which signal do you want to create? (chirp / cw / cwinc): ")

        while signal_type not in ["chirp", "cw", "cwinc"]:
            signal_type = input("Incorrect signal type. Choose chirp / cw / cwinc: ")

        sample_rate = int(float(input("Sample Rate (kHz): ")) * 1000)
        start_freq = int(float(input("Start Frequency (kHz): ")) * 1000)
        end_freq = int(float(input("End Frequency (kHz): ")) * 1000)
        signal_duration = float(input("Signal Duration (sec): "))
        silence_duration = float(input("Silence Duration (sec): "))
        repeat = int(input("Repeat: "))

    amplitude = 0.5
    path = "./"

    print("\nYou chose:")
    print("signal type:", signal_type)
    print("sample rate:", sample_rate)
    print("start freq:", start_freq)
    print("end freq:", end_freq)
    print("signal duration:", signal_duration)
    print("silence duration:", silence_duration)
    print("repeat:", repeat)

    if signal_type in ["chirp", "cw"]:
        chirp_cw_creator(
            sample_rate, start_freq, end_freq,
            signal_duration, silence_duration,
            repeat, amplitude, path
        )
    else:
        cwinc_creator(
            sample_rate, start_freq, end_freq,
            signal_duration, silence_duration,
            repeat, amplitude, path
        )


if __name__ == "__main__":
    create_signal_main()