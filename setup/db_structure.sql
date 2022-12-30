CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    email TEXT NOT NULL UNIQUE, 
    password TEXT NOT NULL, 
    extra, 
    privileges TEXT NOT NULL DEFAULT ''
);

CREATE TABLE aliases (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    source TEXT NOT NULL UNIQUE, 
    destination TEXT NOT NULL, 
    permitted_senders TEXT
);

CREATE TABLE mfa (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    user_id INTEGER NOT NULL, 
    type TEXT NOT NULL, 
    secret TEXT NOT NULL, 
    mru_token TEXT, 
    label TEXT, 
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE auto_aliases (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    source TEXT NOT NULL UNIQUE, 
    destination TEXT NOT NULL, 
    permitted_senders TEXT
);
