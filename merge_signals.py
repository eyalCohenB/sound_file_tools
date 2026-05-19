from scipy.io.wavfile import write, read
import numpy as np
import os


def main():
    signal1_path = './chirp_30k_40k_0.01s_1-repeats.wav'
    signal2_path = './cw-inc_30k_40k_0.01s_1-repeats.wav'
    # signal1_path = './chirp_5k_15k_0.01s_1-repeats.wav'
    # signal2_path = './cw-inc_5k_16k_0.01s_1-repeats.wav'
    output_path = './'
    output_fileName = 'merged_signal.wav'

    s1_rate, s1_data = read(signal1_path)
    s2_rate, s2_data = read(signal2_path)

    if s1_rate != s2_rate:
        raise ValueError("Sample rates do not match!")

    if s1_data.dtype != np.int16:
        raise ValueError(f"{signal1_path} is not int16: {s1_data.dtype}")

    if s2_data.dtype != np.int16:
        raise ValueError(f"{signal2_path} is not int16: {s2_data.dtype}")

    sample_rate = s1_rate

    silence_between_wavs = 0.001
    silence = np.zeros(int(sample_rate * silence_between_wavs), dtype=np.int16)

    merged_data = np.concatenate([silence, s1_data, s2_data, silence]).astype(np.int16)

    out_file = os.path.join(output_path, output_fileName)
    write(out_file, sample_rate, merged_data)

    print("Saved:", out_file)
    print("dtype:", merged_data.dtype)
    print("min/max:", merged_data.min(), merged_data.max())


if __name__ == "__main__":
    main()