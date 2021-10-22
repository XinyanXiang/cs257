-- queries.sql
-- Written by Xinyan Xiang

-- List all the NOCs (National Olympic Committees), in alphabetical order by abbreviation.
SELECT nocs.noc FROM nocs
ORDER BY nocs.noc;

-- List the names of all the athletes from Kenya, sorted by surname.
SELECT DISTINCT athletes.given_name, athletes.surname, nocs.region
FROM athletes, nocs, athletes_games_noc_biometrics,games
WHERE athletes.id = athletes_games_noc_biometrics.athletes_id
AND nocs.id = athletes_games_noc_biometrics.noc_id
AND games.id = athletes_games_noc_biometrics.game_id
AND nocs.region = 'Kenya'
ORDER BY athletes.surname;

-- List all the medals won by Greg Louganis, sorted by year.
SELECT athletes.given_name, athletes.surname, games.game_name,games.year,events.event_name,athletes_games_medal.medal
FROM athletes,athletes_games_medal,games,events
WHERE athletes.id = athletes_games_medal.athletes_id
AND games.id = athletes_games_medal.game_id
AND events.id = athletes_games_medal.event_id
AND athletes.given_name = 'Gregory'
AND athletes.surname = 'Louganis'
AND athletes_games_medal.medal != 'NA'
ORDER BY games.year;

-- List all the NOCs and the number of gold medals they have won, in decreasing order of the number of gold medals.
-- Note: if several people share the same gold medal together, this code consider everyone in this activity won the gold medal
-- rather than considering only one gold medal.

SELECT DISTINCT nocs.noc, COUNT(athletes_games_medal.medal)
FROM nocs,athletes_games_medal,games,athletes_games_noc_biometrics
WHERE athletes_games_noc_biometrics.athletes_id = athletes_games_medal.athletes_id
AND athletes_games_noc_biometrics.game_id = athletes_games_medal.game_id
AND athletes_games_noc_biometrics.game_id = games.id
AND athletes_games_noc_biometrics.noc_id = nocs.id
AND athletes_games_medal.medal = 'Gold'
GROUP by nocs.noc
ORDER BY COUNT(athletes_games_medal.medal) DESC;
