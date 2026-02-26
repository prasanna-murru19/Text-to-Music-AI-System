from pydub import AudioSegment

def merge_audio(inst_path, vocal_path, out_path):
    inst = AudioSegment.from_file(inst_path)
    voc = AudioSegment.from_file(vocal_path)

    voc = voc + 4
    final = inst.overlay(voc)

    final.export(out_path, format="wav")
    return out_path
