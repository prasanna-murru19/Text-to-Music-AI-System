import os
import pretty_midi
import soundfile as sf
import numpy as np

def midi_to_wav(midi_path: str, wav_path: str):
    os.makedirs(os.path.dirname(wav_path), exist_ok=True)

    # Verify MIDI file exists
    if not os.path.exists(midi_path):
        raise FileNotFoundError(f"MIDI file not found: {midi_path}")

    try:
        # Load MIDI file using pretty_midi
        midi_data = pretty_midi.PrettyMIDI(midi_path)
        
        # Try to synthesize audio using pretty_midi's fluidsynth method
        # This uses fluidsynth as a library (not command line)
        try:
            audio_data = midi_data.fluidsynth(fs=44100)
        except (OSError, RuntimeError, AttributeError) as e:
            # If fluidsynth library is not available, provide helpful error message
            error_msg = str(e)
            if "fluidsynth" in error_msg.lower() or "soundfont" in error_msg.lower():
                raise RuntimeError(
                    "FluidSynth library is required for MIDI to WAV conversion. "
                    "Please install it:\n"
                    "Windows: Download from https://www.fluidsynth.org/ or use: pip install pyfluidsynth\n"
                    "Or install fluidsynth system package and ensure it's in PATH."
                )
            else:
                raise RuntimeError(f"Failed to synthesize audio: {error_msg}")
        
        # Convert to mono if stereo (soundfile expects specific format)
        if len(audio_data.shape) > 1:
            audio_data = np.mean(audio_data, axis=1)
        
        # Normalize audio to prevent clipping
        max_val = np.abs(audio_data).max()
        if max_val > 0:
            audio_data = audio_data / max_val * 0.8  # Scale to 80% to avoid clipping
        
        # Save as WAV file using soundfile
        sf.write(wav_path, audio_data, 44100)
        
        # Verify WAV file was created
        if not os.path.exists(wav_path):
            raise RuntimeError(f"WAV file was not created: {wav_path}")
        
        return wav_path
    except ImportError:
        # If soundfile is not available, try using scipy
        try:
            from scipy.io import wavfile
            midi_data = pretty_midi.PrettyMIDI(midi_path)
            audio_data = midi_data.fluidsynth(fs=44100)
            
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
            
            max_val = np.abs(audio_data).max()
            if max_val > 0:
                audio_data = (audio_data / max_val * 0.8 * 32767).astype(np.int16)
            
            wavfile.write(wav_path, 44100, audio_data)
            
            if not os.path.exists(wav_path):
                raise RuntimeError(f"WAV file was not created: {wav_path}")
            
            return wav_path
        except ImportError:
            raise RuntimeError("Neither soundfile nor scipy is installed. Please install one: pip install soundfile or pip install scipy")
    except Exception as e:
        # Clean up partial file if it exists
        if os.path.exists(wav_path):
            try:
                os.remove(wav_path)
            except:
                pass
        raise RuntimeError(f"Failed to convert MIDI to WAV: {str(e)}") from e
