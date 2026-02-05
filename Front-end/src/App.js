import React, { useState, useEffect } from 'react';
import GamesList from './components/GamesList';
import ChatUI from './components/ChatUI';
import Wishlist from './components/Wishlist';
import './App.css';

function App() {
  const [wishlist, setWishlist] = useState([]);
  const [activeTab, setActiveTab] = useState('games');
  const [sessionId, setSessionId] = useState(null);

  // Cargar wishlist del localStorage
  useEffect(() => {
    const saved = localStorage.getItem('wishlist');
    if (saved) {
      setWishlist(JSON.parse(saved));
    }
  }, []);

  const handleWishlistToggle = (gameName) => {
    setWishlist((prev) => {
      if (prev.includes(gameName)) {
        return prev.filter((name) => name !== gameName);
      } else {
        return [...prev, gameName];
      }
    });
  };

  const handleRemoveFromWishlist = (gameName) => {
    setWishlist((prev) => prev.filter((name) => name !== gameName));
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>🎮 Videogames Recommender</h1>
          <p>Encuentra tu próximo juego favorito</p>
        </div>
      </header>

      <div className="app-container">
        <nav className="tabs-nav">
          <button
            className={`tab-btn ${activeTab === 'games' ? 'active' : ''}`}
            onClick={() => setActiveTab('games')}
          >
            🎮 Juegos ({wishlist.length})
          </button>
          <button
            className={`tab-btn ${activeTab === 'chat' ? 'active' : ''}`}
            onClick={() => setActiveTab('chat')}
          >
            💬 Chat
          </button>
          <button
            className={`tab-btn ${activeTab === 'wishlist' ? 'active' : ''}`}
            onClick={() => setActiveTab('wishlist')}
          >
            ❤️ Wishlist
          </button>
        </nav>

        <main className="app-content">
          {activeTab === 'games' && (
            <GamesList
              onWishlistToggle={handleWishlistToggle}
              wishlist={wishlist}
            />
          )}

          {activeTab === 'chat' && (
            <ChatUI
              sessionId={sessionId}
              onSessionChange={setSessionId}
            />
          )}

          {activeTab === 'wishlist' && (
            <Wishlist
              wishlist={wishlist}
              onRemove={handleRemoveFromWishlist}
            />
          )}
        </main>
      </div>

      <footer className="app-footer">
        <p>
          Powered by FastAPI • MongoDB • React |{' '}
          <button 
            onClick={() => window.open('https://github.com', '_blank')}
            className="footer-link"
            aria-label="GitHub"
          >
            GitHub
          </button>
        </p>
      </footer>
    </div>
  );
}

export default App;
