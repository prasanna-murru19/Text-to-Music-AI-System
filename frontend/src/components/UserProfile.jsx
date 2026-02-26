import "./UserProfile.css";

export default function UserProfile({ user, onBack }) {
  // These can later come from backend
  const tracksCreated = user?.tracksCreated || 0;
  const preferredGenre = user?.preferredGenre || "Lofi";
  const preferredVoice = user?.preferredVoice || "Male Voice";
  const lastTrack = user?.lastTrack || "No track generated yet";

  return (
    <div className="profile-container">
      <button className="back-btn" onClick={onBack}>
        ← Back
      </button>

      <div className="profile-card">
        {/* ================= HEADER ================= */}
        <div className="profile-header">
          <div className="profile-avatar">🎧</div>

          <div className="profile-info">
            <h2>{user?.username || "User"}</h2>
            <p>{user?.email}</p>
            <p className="member-since">
              Active Since: {user?.createdAt || "2026"}
            </p>
          </div>
        </div>

        {/* ================= STATS ================= */}
        <div className="profile-stats">
          <div className="stat">
            <span className="stat-number">{tracksCreated}</span>
            <span className="stat-label">Tracks Created</span>
          </div>

          <div className="stat">
            <span className="stat-number">{preferredGenre}</span>
            <span className="stat-label">Preferred Genre</span>
          </div>

          <div className="stat">
            <span className="stat-number">{preferredVoice}</span>
            <span className="stat-label">Voice Type</span>
          </div>
        </div>

        {/* ================= LAST ACTIVITY ================= */}
        <div className="profile-section">
          <h3>🎵 Last Generated Track</h3>
          <p className="highlight-text">{lastTrack}</p>
        </div>

        {/* ================= RECENT TRACKS ================= */}
        <div className="profile-section">
          <h3>📂 Recent Tracks</h3>
          {tracksCreated === 0 ? (
            <p className="empty-message">
              No tracks created yet. Start generating music!
            </p>
          ) : (
            <ul className="track-list">
              <li>🎶 Calm lofi melody</li>
              <li>🎶 Pop beat with happy lyrics</li>
              <li>🎶 Classical piano theme</li>
            </ul>
          )}
        </div>

        {/* ================= PREFERENCES ================= */}
        <div className="profile-section">
          <h3>⚙️ Music Preferences</h3>
          <p>Default Genre: {preferredGenre}</p>
          <p>Default Voice: {preferredVoice}</p>
        </div>
      </div>
    </div>
  );
}
