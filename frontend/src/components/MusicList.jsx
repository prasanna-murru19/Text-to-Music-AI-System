import { useEffect, useState, useRef } from "react";
import { listMusic, downloadWav, deleteMusic } from "../services/api";
import "./MusicList.css";

export default function MusicList({ refreshFlag }) {
  const [musicList, setMusicList] = useState([]);
  const [playingId, setPlayingId] = useState(null);
  const [openLyricsId, setOpenLyricsId] = useState(null);
  const audioRefs = useRef({});

  const fetchMusic = async () => {
    try {
      const data = await listMusic();
      setMusicList(data || []);
    } catch (err) {
      console.error("Failed to fetch music", err);
    }
  };

  useEffect(() => {
    fetchMusic();
  }, [refreshFlag]);

  return (
    <div className="music-list">
      <h2 className="music-heading">🎵 Generated Music</h2>

      {musicList.map((music) => (
        <div key={music.id} className="music-item">
          
          {/* LEFT INFO */}
          <div className="music-info">
            <div className="music-title" title={music.prompt}>
              🎵 {music.prompt}
            </div>
            <div className="music-meta">⏱ {music.duration} sec</div>
          </div>

          {/* RIGHT ACTIONS */}
          <div className="actions">
            <a
              href={downloadWav(music.id)}
              className="btn download"
              download
              title="Download"
            >
              ⬇
            </a>

            <button
              className="btn play"
              onClick={async () => {
                const audio = audioRefs.current[music.id];
                const url = downloadWav(music.id);

                if (playingId === music.id) {
                  audio.pause();
                  audio.currentTime = 0;
                  setPlayingId(null);
                } else {
                  Object.values(audioRefs.current).forEach((a) => {
                    if (a) {
                      a.pause();
                      a.currentTime = 0;
                    }
                  });

                  if (!audio.src) audio.src = url;
                  setPlayingId(music.id);
                  await audio.play();
                }
              }}
            >
              {playingId === music.id ? "⏹" : "▶"}
            </button>

            <button
              className="btn lyrics"
              onClick={() =>
                setOpenLyricsId(openLyricsId === music.id ? null : music.id)
              }
            >
              Lyrics
            </button>

            <button
              className="btn delete"
              onClick={async () => {
                if (window.confirm("Delete this music?")) {
                  await deleteMusic(music.id);
                  fetchMusic();
                }
              }}
            >
              Delete
            </button>
          </div>

          {/* LYRICS */}
          {openLyricsId === music.id && (
            <div className="lyrics-box">
              <pre>{music.lyrics}</pre>
            </div>
          )}

          {/* AUDIO */}
          <audio
            ref={(el) => (audioRefs.current[music.id] = el)}
            onEnded={() => setPlayingId(null)}
          />
        </div>
      ))}
    </div>
  );
}
