#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute('DELETE FROM matches')
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB = connect()
    c = DB.cursor()
    c.execute('DELETE FROM players')
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB = connect()
    c = DB.cursor()
    c.execute('SELECT count(*) FROM players')
    count = c.fetchone()[0]
    DB.close()
    return count


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    DB = connect()
    c = DB.cursor()
    c.execute('INSERT INTO players (name) VALUES (%s)', (name,))
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB = connect()
    c = DB.cursor()
    results = []
    # Test if have had any matches
    c.execute('SELECT count(*) from matches')
    count = c.fetchone()[0]
    if count == 0:
        c.execute('SELECT * from players')
        results = [(row[0], row[1], 0, 0) for row in c.fetchall()]
    else:
        c.execute('SELECT players.id, players.name, count(players.id) as wins FROM players, matches WHERE players.id=matches.winner GROUP BY players.id ORDER BY wins DESC')
        win_records = c.fetchall()
        for i in range(len(win_records)):
            win_record = win_records[i]
            c.execute('SELECT count(matches.id) FROM matches WHERE matches.loser=(%s)',
                      (win_record[0],))
            results.append(
                (win_record[0],
                 win_record[1],
                 win_record[2],
                 win_record[2] + c.fetchone()[0]))
    DB.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB = connect()
    c = DB.cursor()
    c.execute('INSERT INTO matches (winner, loser) VALUES (%s,%s)',
              (winner, loser,))
    DB.commit()
    DB.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.

    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    standings = playerStandings()
    pairs = []

    DB = connect()
    c = DB.cursor()
    c.execute('SELECT * FROM players')
    all_players = c.fetchall()
    ever_win_players = [(standing[0], standing[1]) for standing in standings]
    all_lose_players = [player for player in all_players if player not in ever_win_players]

    while len(ever_win_players) > 1:
        first_player = ever_win_players.pop()
        second_player = ever_win_players.pop()
        pairs.append(
            (first_player[0],
             first_player[1],
             second_player[0],
             second_player[1]))

    while len(all_lose_players) > 1:
        first_player = all_lose_players.pop()
        second_player = all_lose_players.pop()
        pairs.append(
            (first_player[0],
             first_player[1],
             second_player[0],
             second_player[1]))

    return pairs
