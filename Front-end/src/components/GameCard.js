import React from 'react';
import '../styles/GameCard.css';

export const GameCard = ({ game, onWishlistToggle, isInWishlist }) => {
  const handleWishlistClick = (e) => {
    e.preventDefault();
    onWishlistToggle(game.name);
  };

  return (
    <div className="game-card">
      <div className="game-card-header">
        <h3 className="game-title">{game.name}</h3>
        <button
          className={`wishlist-btn ${isInWishlist ? 'active' : ''}`}
          onClick={handleWishlistClick}
          title={isInWishlist ? 'Eliminar de wishlist' : 'Añadir a wishlist'}
        >
          ♥
        </button>
      </div>

      <div className="game-genres">
        {Array.isArray(game.genres) ? (
          game.genres.map((genre, idx) => (
            <span key={idx} className="genre-badge">
              {genre}
            </span>
          ))
        ) : (
          <span className="genre-badge">{game.genres}</span>
        )}
      </div>

      {game.price && (
        <div className="game-price">
          💶 {game.price.toFixed(2)}€
        </div>
      )}

      {game.description && (
        <p className="game-description">{game.description.substring(0, 100)}...</p>
      )}

      <button className="game-details-btn">Ver detalles</button>
    </div>
  );
};

export default GameCard;
