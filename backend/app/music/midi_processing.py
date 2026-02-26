import pretty_midi

def midi_to_tokens(midi_file):
    midi = pretty_midi.PrettyMIDI(midi_file)
    tokens = []

    for inst in midi.instruments:
        for note in inst.notes:
            token = f"{note.pitch}_{note.start:.2f}_{note.end:.2f}"
            tokens.append(token)

    return tokens
