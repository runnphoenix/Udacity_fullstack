-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

CREATE TABLE players (
	id serial primary key,
	name text
);

CREATE TABLE matches (
	id serial primary key,
	winner int references players (id),
	loser int references players (id)
);

CREATE VIEW win_records AS
	SELECT players.id, players.name, count(matches.winner) AS wins
	FROM players LEFT JOIN matches
	ON players.id=matches.winner
	GROUP BY players.id
	ORDER BY wins DESC
