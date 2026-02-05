-- Tabla de roles
CREATE TABLE IF NOT EXISTS Role (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    can_query INTEGER DEFAULT 0,
    can_update INTEGER DEFAULT 0,
    can_delete INTEGER DEFAULT 0,
    can_insert INTEGER DEFAULT 0
);

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS User (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role_id INTEGER NOT NULL,
    FOREIGN KEY (role_id) REFERENCES Role(id) ON DELETE CASCADE
);

-- Tabla de juegos
CREATE TABLE Games (
    id SERIAL PRIMARY KEY,
    appid INT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    short_description TEXT,
    currency CHAR(3),
    initial_price NUMERIC(10,2),
    final_price NUMERIC(10,2),
    discount_percent INT,
    is_free BOOLEAN DEFAULT FALSE,
    windows BOOLEAN DEFAULT TRUE,
    mac BOOLEAN DEFAULT FALSE,
    linux BOOLEAN DEFAULT FALSE
);


-- Tabla wishlist
CREATE TABLE IF NOT EXISTS Wishlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    appid INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
    FOREIGN KEY (appid) REFERENCES Games(appid) ON DELETE CASCADE,
    UNIQUE(user_id, appid)
);
