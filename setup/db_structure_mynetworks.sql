CREATE TABLE mynetworks (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    cidr TEXT NOT NULL, 
    addr_in_range TEXT NOT NULL UNIQUE, 
    description TEXT NOT NULL
);
