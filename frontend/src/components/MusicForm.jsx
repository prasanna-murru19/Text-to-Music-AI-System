import { useState } from "react";
import { generateMusic } from "../services/api";
import "./MusicForm.css";

export default function MusicForm({ onGenerated }) {
  const [prompt, setPrompt] = useState("");
  const [genre, setGenre] = useState("lofi");
  const [voice, setVoice] = useState("male");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!prompt.trim()) {
      alert("Please enter a text prompt");
      return;
    }

    setLoading(true);

    try {
      const result = await generateMusic({
        prompt,
        genre,
        voice,
      });

      if (result) {
        onGenerated(); // refresh music list
      }
    } catch (err) {
      console.error("Music generation failed:", err);
      alert("Failed to generate music. Please try again.");
    } finally {
      setLoading(false);
      setPrompt("");
    }
  };

  return (
    <form className="music-form" onSubmit={handleSubmit}>
      {/* Prompt */}
      <input
        type="text"
        placeholder="Describe your song (lyrics idea)"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        required
      />

      {/* Genre */}
      <select value={genre} onChange={(e) => setGenre(e.target.value)}>
        <option value="lofi">Lofi</option>
        <option value="pop">Pop</option>
        <option value="classical">Classical</option>
      </select>

      {/* Voice */}
      <select value={voice} onChange={(e) => setVoice(e.target.value)}>
        <option value="male">Male Voice</option>
        <option value="female">Female Voice</option>
      </select>

      <button type="submit" disabled={loading}>
        {loading ? "Generating..." : "Generate Music"}
      </button>
    </form>
  );
}
