DROP TABLE IF EXISTS jkacosta91_coderhouse.Marvel_Characters;

CREATE TABLE jkacosta91_coderhouse.Marvel_Characters (
    id INTEGER NOT NULL,
    name VARCHAR(250),
    description TEXT,
    modified TIMESTAMP,
    resourceURI VARCHAR(500),
    comics_available INTEGER,
    series_available INTEGER,
    stories_available INTEGER,
    events_available INTEGER,
    urls_type VARCHAR(100),
    urls_url VARCHAR(500)
);