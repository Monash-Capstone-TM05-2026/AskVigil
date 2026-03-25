# TODO: @Adrian - Audio analysis in progress, make FastAPI endpoint, test that it works
import librosa
import numpy as np

def analyze_audio_forensics(file_path):
    # 1. Load audio
    y, sr = librosa.load(file_path, sr=None)
    report = {"score": 0, "flags": []}

    # --- TEST 1: Digital Silence (Perfect Pause Test) ---
    # AI often generates absolute 0 in pauses. Humans have "Room Tone."
    intervals = librosa.effects.split(y, top_db=60) # Find non-silent parts
    # If the energy in "silent" parts is mathematically zero
    full_indices = np.arange(len(y))
    silent_indices = np.setdiff1d(full_indices, np.concatenate([np.arange(start, end) for start, end in intervals]))
    
    if len(silent_indices) > 0:
        silent_amplitude = np.max(np.abs(y[silent_indices]))
        if silent_amplitude == 0:
            report["score"] += 40
            report["flags"].append("CRITICAL: Absolute digital silence detected in pauses.")

    # --- TEST 2: Nyquist Brick-wall (Low-Res AI Test) ---
    # Many scammers use cheap 22kHz AI models. This looks like a "cliff" in the spectrum.
    stft = np.abs(librosa.stft(y))
    freqs = librosa.fft_frequencies(sr=sr)
    avg_spectrum = np.mean(stft, axis=1)
    
    # Check if signal disappears abruptly at 11025Hz (half of 22k)
    high_freq_energy = np.sum(avg_spectrum[freqs > 11000])
    low_freq_energy = np.sum(avg_spectrum[freqs <= 11000])
    
    if high_freq_energy < (low_freq_energy * 0.001): # Arbitrary 0.1% threshold
        report["score"] += 30
        report["flags"].append("WARNING: Artificial frequency cutoff detected (Low-res AI signature).")

    # --- TEST 3: Spectral Flatness (Robot Voice Test) ---
    # AI voices are often "flatter" than human voices which have rich harmonics.
    flatness = librosa.feature.spectral_flatness(y=y)
    avg_flatness = np.mean(flatness)
    
    if avg_flatness > 0.1: # AI noise/vocoder artifacts increase flatness
        report["score"] += 20
        report["flags"].append("NOTICE: High spectral flatness (unnatural robotic hiss).")

    return report

# Usage
# result = analyze_audio_forensics("whatsapp_voice_note.wav")
# print(f"Scam Probability Score: {result['score']}%")
# print("\n".join(result['flags']))