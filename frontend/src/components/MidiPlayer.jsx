import { useRef, useState } from "react";
import * as Tone from "tone";
import { Midi } from "@tonejs/midi";

export default function MidiPlayer({ midiUrl, lyrics }) {
  const [playing, setPlaying] = useState(false);
  const [currentLine, setCurrentLine] = useState("");

  const synthRef = useRef(null);
  const partRef = useRef(null);
  const lyricTimerRef = useRef(null);

  const lyricLines = lyrics
    ? lyrics.split("\n").filter(Boolean)
    : [];

  const playMidi = async () => {
    try {
      stopMidi();
      await Tone.start();

      const res = await fetch(midiUrl);
      const buffer = await res.arrayBuffer();
      const midi = new Midi(buffer);

      const synth = new Tone.PolySynth(Tone.Synth).toDestination();
      synthRef.current = synth;

      const notes = midi.tracks.flatMap(track =>
        track.notes.map(n => ({
          time: n.time,
          name: n.name,
          duration: n.duration,
          velocity: n.velocity,
        }))
      );

      const part = new Tone.Part((time, note) => {
        synth.triggerAttackRelease(
          note.name,
          note.duration,
          time,
          note.velocity
        );
      }, notes);

      part.start(0);
      partRef.current = part;

      Tone.Transport.start();
      setPlaying(true);

      // Lyrics display (basic timing)
      let index = 0;
      setCurrentLine(lyricLines[index] || "");

      lyricTimerRef.current = setInterval(() => {
        index++;
        if (index < lyricLines.length) {
          setCurrentLine(lyricLines[index]);
        } else {
          clearInterval(lyricTimerRef.current);
        }
      }, 2000);

    } catch (e) {
      alert("Failed to play MIDI");
      console.error(e);
    }
  };

  const stopMidi = () => {
    Tone.Transport.stop();
    Tone.Transport.cancel();

    partRef.current?.dispose();
    synthRef.current?.dispose();

    clearInterval(lyricTimerRef.current);

    partRef.current = null;
    synthRef.current = null;

    setCurrentLine("");
    setPlaying(false);
  };

  return (
    <div>
      <button onClick={playing ? stopMidi : playMidi}>
        {playing ? "Stop" : "Play"}
      </button>

      {playing && currentLine && (
        <div style={{
          marginTop: 8,
          padding: 8,
          background: "#f2f2f2",
          borderRadius: 6
        }}>
          🎤 {currentLine}
        </div>
      )}
    </div>
  );
}
