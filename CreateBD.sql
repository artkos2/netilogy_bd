CREATE TABLE IF NOT EXISTS styles (
	id SERIAL PRIMARY KEY,
	name VARCHAR(40) NOT NULL
);

CREATE TABLE IF NOT EXISTS musicians (
	id SERIAL PRIMARY KEY,
	name VARCHAR(40) NOT NULL,
	year INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS albums (
	id SERIAL PRIMARY KEY,
	name VARCHAR(40) NOT NULL,
	year INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS songs (
	id SERIAL PRIMARY KEY,
	name VARCHAR(40) NOT NULL,
	duration INTEGER NOT null,
	album_id INTEGER REFERENCES albums(id) NOT NULL
);
CREATE TABLE IF NOT EXISTS collections (
	id SERIAL PRIMARY KEY,
	name VARCHAR(40) NOT NULL,
	year INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS musicians_styles (
	musician_id INTEGER REFERENCES musicians(id),
	style_id INTEGER REFERENCES styles(id),
	CONSTRAINT pk PRIMARY KEY (musician_id, style_id)

);
CREATE TABLE IF NOT EXISTS musicians_albums (
	song_id INTEGER REFERENCES songs(id),
	musician_id INTEGER REFERENCES musicians(id),
	CONSTRAINT sa PRIMARY KEY (song_id, musician_id)

);

CREATE TABLE IF NOT EXISTS songs_collections (
	collection_id INTEGER REFERENCES collections(id),
	song_id INTEGER REFERENCES songs(id),
	CONSTRAINT sc PRIMARY KEY (collection_id, song_id)
);