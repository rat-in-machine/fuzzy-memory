import React, { useState, useRef, useEffect } from 'react';
import { chatAPI } from '../services/api';
import '../styles/ChatUI.css';

export const ChatUI = ({ sessionId, onSessionChange }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);
  const [currentSessionId, setCurrentSessionId] = useState(sessionId);

  // Auto-scroll a los últimos mensajes
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSendMessage = async () => {
    if (!input.trim()) return;

    // Agregar mensaje del usuario
    setMessages((prev) => [...prev, { role: 'user', content: input }]);
    setInput('');
    setLoading(true);

    try {
      const response = await chatAPI.chat(input, currentSessionId);
      
      // Actualizar session ID si es nuevo
      if (!currentSessionId) {
        setCurrentSessionId(response.data.session_id);
        onSessionChange?.(response.data.session_id);
      }

      // Agregar respuesta del chatbot
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: response.data.response,
          games: response.data.retrieved_games,
        },
      ]);
    } catch (error) {
      console.error('Error en chat:', error);
      setMessages((prev) => [
        ...prev,
        {
          role: 'error',
          content: 'Error al procesar tu solicitud. Intenta de nuevo.',
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleReset = async () => {
    if (!currentSessionId) return;
    
    try {
      await chatAPI.resetChat(currentSessionId);
      setMessages([]);
      setCurrentSessionId(null);
      onSessionChange?.(null);
    } catch (error) {
      console.error('Error al resetear chat:', error);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <h2>🎮 Chat Recomendador</h2>
        {currentSessionId && (
          <button className="reset-btn" onClick={handleReset}>
            🔄 Nueva sesión
          </button>
        )}
      </div>

      <div className="messages-list">
        {messages.length === 0 ? (
          <div className="empty-state">
            <p>Hola! 👋 Pregúntame sobre videojuegos y te daré recomendaciones</p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div className="message-avatar">
                {msg.role === 'user' ? '👤' : '🤖'}
              </div>
              <div className="message-content">
                <p>{msg.content}</p>
                {msg.games && msg.games.length > 0 && (
                  <div className="message-games">
                    {msg.games.map((game, gIdx) => (
                      <div key={gIdx} className="game-result">
                        <strong>{game.name}</strong>
                        <small>{game.genres.join(', ')} • {game.price.toFixed(2)}€</small>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))
        )}
        {loading && (
          <div className="message assistant">
            <div className="message-avatar">🤖</div>
            <div className="message-content typing">
              <span></span><span></span><span></span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="chat-input-area">
        <input
          type="text"
          placeholder="Ej: Recomiéndame un juego de rol..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          disabled={loading}
        />
        <button
          onClick={handleSendMessage}
          disabled={loading || !input.trim()}
          className="send-btn"
        >
          {loading ? '⏳' : '📤'}
        </button>
      </div>
    </div>
  );
};

export default ChatUI;
