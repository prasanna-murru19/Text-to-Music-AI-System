import os

import numpy as np
import soundfile as sf


def speech_to_singing(
    speech_wav: str,
    midi_path: str,
    out_path: str,
    voice: str = "male",
) -> str:
    if not os.path.exists(speech_wav):
        raise FileNotFoundError(speech_wav)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # Read WAV (no pitch shifting here — pitch shifting is what causes "robotic")
    y, sr = sf.read(speech_wav, always_2d=False)

    # Ensure mono
    if isinstance(y, np.ndarray) and y.ndim == 2:
        y = np.mean(y, axis=1)

    # Light "singing" polish: small echo / ambience (cheap + non-robotic)
    y_out = y.astype(np.float32, copy=True)

    def _add_echo(x: np.ndarray, delay_s: float, decay: float) -> None:
        n = int(delay_s * sr)
        if n <= 0 or n >= x.shape[0]:
            return
        x[n:] += decay * x[:-n]

    _add_echo(y_out, delay_s=0.065, decay=0.22)
    _add_echo(y_out, delay_s=0.130, decay=0.12)

    # Prevent clipping
    peak = float(np.max(np.abs(y_out))) if y_out.size else 0.0
    if peak > 1.0:
        y_out = y_out / peak * 0.98

    sf.write(out_path, y_out, sr)
    return out_path
