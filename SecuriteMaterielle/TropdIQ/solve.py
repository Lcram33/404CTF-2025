import numpy as np
from scipy.io.wavfile import write


# Settings
sample_rate = 44100
filename = 'chall.iq'

# 1. Read IQ Complex128 data
iq_data = np.fromfile(filename, dtype=np.complex128)

# 2. Reverse the Fourier Transform
time_domain_signal = np.fft.ifft(iq_data)

# 3. Normalize the signal and amplify
normalized_signal = np.real(time_domain_signal)
normalized_signal /= np.max(np.abs(normalized_signal))  # Scaling to [-1, 1]

# 4. Save in WAV format
write('flag.wav', sample_rate, (normalized_signal * 32767).astype(np.int16))
print("flag.wav saved.")