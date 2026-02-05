import React, { useState } from 'react';
import { chatAPI } from '../services/api';
import GameCard from './GameCard';
import '../styles/GamesList.css';

export const GamesList = ({ onWishlistToggle, wishlist }) => {
  const [games, setGames] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState('name'); // 'name' o 'genre'

  const handleSearch = async () => {
    if (!searchTerm.trim()) return;

    setLoading(true);
    try {
      const response =
        filterType === 'name'
          ? await chatAPI.searchByName(searchTerm, 10)
          : await chatAPI.searchByGenre(searchTerm, 10);

      setGames(response.data || []);
    } catch (error) {
      console.error('Error en búsqueda:', error);
      setGames([]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="games-list-container">
      <div className="search-section">
        <h2>🎮 Listado de Juegos</h2>
        
        <div className="search-bar">
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="filter-select"
          >
            <option value="name">Buscar por nombre</option>
            <option value="genre">Buscar por género</option>
          </select>

          <input
            type="text"
            placeholder={
              filterType === 'name'
                ? 'Ej: Cyberpunk 2077...'
                : 'Ej: Rol, Acción...'
            }
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            onKeyPress={handleKeyPress}
            disabled={loading}
            className="search-input"
          />

          <button
            onClick={handleSearch}
            disabled={loading || !searchTerm.trim()}
            className="search-btn"
          >
            {loading ? '🔍 Buscando...' : '🔍 Buscar'}
          </button>
        </div>
      </div>

      <div className="games-grid">
        {games.length === 0 && !loading && (
          <div className="empty-state">
            <p>📭 Realiza una búsqueda para ver juegos</p>
          </div>
        )}

        {loading && (
          <div className="loading">
            <p>⏳ Buscando juegos...</p>
          </div>
        )}

        {games.map((game, idx) => (
          <GameCard
            key={idx}
            game={game}
            onWishlistToggle={onWishlistToggle}
            isInWishlist={wishlist.includes(game.name)}
          />
        ))}
      </div>
    </div>
  );
};

export default GamesList;
