import numpy as np
import soundfile as sf
import pyworld as pw
import pretty_midi
import librosa
from scipy.signal import medfilt


FFT_SIZE = 2048  # 🔥 MUST be same for cheaptrick & d4c


def midi_to_f0_curve(midi_path, frame_times):
    pm = pretty_midi.PrettyMIDI(midi_path)
    midi_f0 = np.zeros(len(frame_times))

    for instrument in pm.instruments:
        if instrument.is_drum:
            continue

        for note in instrument.notes:
            freq = pretty_midi.note_number_to_hz(note.pitch)
            idx = np.where(
                (frame_times >= note.start) &
                (frame_times <= note.end)
            )[0]
            midi_f0[idx] = freq

    return midi_f0


def tts_to_singing(tts_wav, midi_file, output_wav):
    # ---------------- LOAD AUDIO ----------------
    audio, sr = sf.read(tts_wav)
    if audio.ndim > 1:
        audio = audio.mean(axis=1)

    # 🔥 Slow down for smoother singing
    audio = librosa.effects.time_stretch(audio, rate=0.88)

    # ---------------- PITCH EXTRACTION ----------------
    f0, time_axis = pw.harvest(
        audio,
        sr,
        frame_period=10.0
    )
    f0 = pw.stonemask(audio, f0, time_axis, sr)

    # ---------------- MIDI PITCH ----------------
    midi_f0 = midi_to_f0_curve(midi_file, time_axis)

    # 🔥 Blend pitch (male voice friendly)
    alpha = 0.50
    final_f0 = np.where(
        midi_f0 > 0,
        alpha * midi_f0 + (1 - alpha) * f0,
        f0
    )

    # 🔥 Strong smoothing (no shaking)
    final_f0 = medfilt(final_f0, kernel_size=7)
    final_f0[final_f0 < 60] = 0

    # ---------------- WORLD RESYNTHESIS ----------------
    sp = pw.cheaptrick(
        audio,
        final_f0,
        time_axis,
        sr,
        fft_size=FFT_SIZE
    )

    ap = pw.d4c(
        audio,
        final_f0,
        time_axis,
        sr,
        fft_size=FFT_SIZE   # 🔥 SAME fft_size
    )

    singing = pw.synthesize(
        final_f0,
        sp,
        ap,
        sr
    )

    sf.write(output_wav, singing, sr)
