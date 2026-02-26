import { useEffect, useState } from "react";
import MusicForm from "./components/MusicForm";
import MusicList from "./components/MusicList";
import RegisterForm from "./components/RegisterForm";
import LoginForm from "./components/LoginForm";
import UserProfile from "./components/UserProfile";
import "./App.css";

function App() {
  const [page, setPage] = useState("home");
  const [refreshFlag, setRefreshFlag] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [theme, setTheme] = useState("light");

  /* 🔥 RESTORE LOGIN ON PAGE REFRESH */
  useEffect(() => {
    const savedUser = localStorage.getItem("user");
    if (savedUser) {
      setCurrentUser(JSON.parse(savedUser));
    }
  }, []);

  const handleGenerated = () => {
    setRefreshFlag((prev) => !prev);
  };

  const goToGenerationIfLoggedIn = () => {
    if (!currentUser) {
      setPage("login");
    } else {
      setPage("generate");
    }
  };

  /* ✅ LOGOUT ONLY WHEN BUTTON CLICKED */
  const handleLogout = () => {
    localStorage.removeItem("user");
    setCurrentUser(null);
    setPage("home");
  };

  const toggleTheme = () => {
    setTheme(theme === "light" ? "dark" : "light");
  };

  const renderContent = () => {
    if (page === "register") {
      return (
        <RegisterForm
          onSuccess={() => {
            setPage("login");
          }}
        />
      );
    }

    if (page === "login") {
      return (
        <LoginForm
          onSuccess={(user) => {
            setCurrentUser(user);
            localStorage.setItem("user", JSON.stringify(user)); // 🔥 persist
            setPage("generate");
          }}
        />
      );
    }

    if (page === "profile") {
      return (
        <UserProfile
          user={currentUser}
          onBack={() => setPage("generate")}
        />
      );
    }

    if (page === "generate") {
      return (
        <div className="generate-container">
          <MusicForm onGenerated={handleGenerated} />
          <MusicList refreshFlag={refreshFlag} />
        </div>
      );
    }

    // HOME
    return (
      <div className="home-page">
        <h1>Text-to-Music Generation System</h1>
        <p>
          Turn your words into music — an AI-based system that transforms text prompts into complete musical compositions with lyrics, melody, and vocals.
        </p>
        <button
          className="cta-button"
          onClick={() =>
            currentUser ? setPage("generate") : setPage("login")
          }
        >
          Get Started →
        </button>
      </div>
    );
  };

  return (
    <div className={`app-container theme-${theme}`}>
      {/* NAVBAR */}
      <nav className="navbar">
        <button className="theme-toggle" onClick={toggleTheme}>
          {theme === "light" ? "🌙" : "☀️"}
        </button>

        <button onClick={() => setPage("home")}>Home</button>
        <button onClick={goToGenerationIfLoggedIn}>Generation</button>

        {!currentUser ? (
          <>
            <button onClick={() => setPage("register")}>Sign-up</button>
            <button onClick={() => setPage("login")}>Log-in</button>
          </>
        ) : (
          <>
            <button
              className="profile-btn"
              onClick={() => setPage("profile")}
            >
              👤 {currentUser.username || "User"}
            </button>

            <button
              className="logout-btn"
              onClick={handleLogout}
            >
              Logout
            </button>
          </>
        )}
      </nav>

      {/* MAIN CONTENT */}
      <div className="main-content">{renderContent()}</div>
    </div>
  );
}

export default App;
