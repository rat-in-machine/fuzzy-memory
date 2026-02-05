import React, { useEffect } from 'react';
import '../styles/Wishlist.css';

export const Wishlist = ({ wishlist, onRemove }) => {
  useEffect(() => {
    // Guardar en localStorage
    localStorage.setItem('wishlist', JSON.stringify(wishlist));
  }, [wishlist]);

  const handleRemoveFromWishlist = (gameName) => {
    onRemove(gameName);
  };

  return (
    <div className="wishlist-container">
      <div className="wishlist-header">
        <h2>❤️ Mi Wishlist ({wishlist.length})</h2>
      </div>

      {wishlist.length === 0 ? (
        <div className="empty-wishlist">
          <p>Tu wishlist está vacía</p>
          <small>Añade juegos haciendo click en ♥</small>
        </div>
      ) : (
        <div className="wishlist-items">
          {wishlist.map((gameName, idx) => (
            <div key={idx} className="wishlist-item">
              <span className="game-name">{gameName}</span>
              <button
                className="remove-btn"
                onClick={() => handleRemoveFromWishlist(gameName)}
              >
                ✕
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default Wishlist;
