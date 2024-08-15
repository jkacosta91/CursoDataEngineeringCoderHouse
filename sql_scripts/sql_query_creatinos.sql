DROP TABLE IF EXISTS jkacosta91_coderhouse.anime;

CREATE TABLE jkacosta91_coderhouse.anime (
    mal_id INTEGER NOT NULL PRIMARY KEY,
    url VARCHAR(500),
    approved BOOLEAN,
    title VARCHAR(255),
    title_english VARCHAR(255),
    title_japanese VARCHAR(255),
    type VARCHAR(50),
    source VARCHAR(255),
    episodes INTEGER,
    status VARCHAR(50),
    airing BOOLEAN,
    duration VARCHAR(50),
    rating VARCHAR(50),
    score INTEGER,
    scored_by INTEGER,
    rank INTEGER,
    popularity INTEGER,
    members INTEGER,
    favorites INTEGER,
    synopsis VARCHAR(MAX),
    background VARCHAR(MAX), 
    season VARCHAR(20),
    year INTEGER
);