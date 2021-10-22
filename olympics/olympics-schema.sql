-- olympics-schema.sql: Create tables for the Olympics databese
-- Written by Xinyan Xiang, Oct 14 ,2021

CREATE TABLE athletes (
	id INTEGER,
	surname TEXT,
	given_name TEXT,
	sex TEXT
);
-- \copy athletes FROM 'athletes.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE games (
	id INTEGER,
	game_name TEXT,
	year INTEGER,
	season TEXT,
	city TEXT
);
-- \copy games FROM 'games.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE events (
	id INTEGER,
	event_name TEXT,
	sport TEXT
);
-- \copy events FROM 'events.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE nocs (
	id INTEGER,
	noc TEXT,
	region TEXT
);
-- \copy nocs FROM 'nocs.csv' DELIMITER ',' CSV NULL AS 'NULL'
-- Note: Since some athelets' ages, heights, and weights are NA,  I used TEXT to specify these values.

CREATE TABLE athletes_games_noc_biometrics(
	athletes_id INTEGER,
	game_id INTEGER,
	noc_id INTEGER,
	age TEXT,
	height TEXT,
	weight TEXT
);
-- \copy athletes_games_noc_biometrics FROM 'athletes_games_noc_biometrics.csv' DELIMITER ',' CSV NULL AS 'NULL'

CREATE TABLE athletes_games_medal(
	athletes_id INTEGER,
	game_id INTEGER,
	event_id INTEGER,
	medal TEXT
);
-- \copy athletes_games_medal FROM 'athletes_games_medal.csv' DELIMITER ',' CSV NULL AS 'NULL'
