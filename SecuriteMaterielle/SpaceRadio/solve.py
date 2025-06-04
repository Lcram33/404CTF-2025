import numpy as np
from scipy.signal import decimate, butter, lfilter
from scipy.io.wavfile import write


# 1. Settings
fs = 48000  # sampling rate of the original signal
decim_factor = 3  # to reduce the sampling rate to a suitable audio rate
audio_fs = fs // decim_factor

# 2. Load .iq file (complex64 : I + jQ)
iq_data = np.fromfile("chall.iq", dtype=np.complex64)

# 3. FM de-modulation
phase = np.angle(iq_data)
d_phase = np.diff(phase)
d_phase = np.unwrap(d_phase)

# 4. Low-pass filter to improve audio quality
def butter_lowpass_filter(data, cutoff, fs, order=5):
    nyq = 0.5 * fs
    norm_cutoff = cutoff / nyq
    b, a = butter(order, norm_cutoff, btype='low', analog=False)
    return lfilter(b, a, data)

filtered = butter_lowpass_filter(d_phase, cutoff=15000, fs=fs)

# 5. Decimation to reduce the sampling rate
audio = decimate(filtered, decim_factor)

# 6. Normalization and conversion to int16
audio /= np.max(np.abs(audio))
audio_int16 = (audio * 32767).astype(np.int16)

# 7. Save the audio to a .wav file
write("flag.wav", audio_fs, audio_int16)
print("flag.wav saved.")
