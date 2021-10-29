#!/usr/bin/env python3
'''
    Xinyan Xiang, 28 Oct 2021
    Olympics Data API.
'''
import sys
import argparse
import flask
import json
import psycopg2

from config import password
from config import database
from config import user

app = flask.Flask(__name__)

try:
    connection = psycopg2.connect(database=database, user=user, password=password)
except Exception as e:
    print(e)
    exit()

@app.route('/games')
def get_games():
    ''' Return a JSON list of dictionaries, each of which represents one
        Olympic games, sorted by year. Each dictionary in this list will have
        the following fields.
    id -- (INTEGER) a unique identifier for the games in question
    year -- (INTEGER) the 4-digit year in which the games were held (e.g. 1992)
    season -- (TEXT) the season of the games (either "Summer" or "Winter")
    city -- (TEXT) the host city (e.g. "Barcelona") '''

    games_list = []
    try:
        cursor = connection.cursor()
        query = 'SELECT games.id, games.year, games.season, games.city FROM games ORDER BY games.year'
        cursor.execute(query)
    except Exception as e:
            print(e)
            exit()   
    for row in cursor:
        games_list.append({"id":row[0],"year":row[1],"season":row[2],"city":row[3]})
    return json.dumps(games_list)

@app.route('/nocs')
def get_nocs():
    '''Return a JSON list of dictionaries, each of which represents one
       National Olympic Committee, alphabetized by NOC abbreviation. Each dictionary
       in this list will have the following fields.
   abbreviation -- (TEXT) the NOC's abbreviation (e.g. "USA", "MEX", "CAN", etc.)
   name -- (TEXT) the NOC's full name (see the noc_regions.csv file) '''

    nocs_list = []
    try:
        cursor = connection.cursor()
        query = 'SELECT nocs.noc, nocs.region FROM nocs ORDER BY nocs.noc'
        cursor.execute(query)
    except Exception as e:
            print(e)
            exit()   
    for row in cursor:
        nocs_list.append({"abbreviation":row[0],"name":row[1]})
    return json.dumps(nocs_list)
            
@app.route('/medalists/games/<games_id>')
def get_medals_game(games_id):
    '''Return a JSON list of dictionaries, each representing one athlete
       who earned a medal in the specified games. Each dictionary will have the
       following fields.
   athlete_id -- (INTEGER) a unique identifier for the athlete
   athlete_name -- (TEXT) the athlete's full name
   athlete_sex -- (TEXT) the athlete's sex as specified in the database ("F" or "M")
   sport -- (TEXT) the name of the sport in which the medal was earned
   event -- (TEXT) the name of the event in which the medal was earned
   medal -- (TEXT) the type of medal ("gold", "silver", or "bronze") '''

    medals_list = []
    noc = flask.request.args.get('noc')
    query = '''SElECT athletes_games_medal.athletes_id,CONCAT(athletes.given_name,' ', athletes.surname) AS given_name,
        athletes.sex,events.sport,events.event_name,athletes_games_medal.medal
        FROM athletes_games_medal,athletes,events,nocs,athletes_games_noc_biometrics
        WHERE athletes_games_medal.athletes_id = athletes.id
        AND athletes_games_medal.event_id = events.id
        AND athletes_games_medal.game_id = {0}
        AND athletes_games_noc_biometrics.athletes_id = athletes_games_medal.athletes_id
        AND athletes_games_noc_biometrics.noc_id = nocs.id
        AND athletes_games_noc_biometrics.game_id = athletes_games_medal.game_id
        AND athletes_games_medal.medal != 'NA' '''.format(games_id)
    if noc != None:
        noc_quote = "'" + noc + "'"
        query = query + "AND nocs.noc = {0} ORDER by athletes.id".format(noc_quote)
    try:
        cursor = connection.cursor()
        cursor.execute(query)
    except Exception as e:
            print(e)
            exit()   
    for row in cursor:
        medals_list.append({"athlete_id":row[0],"athlete_name":row[1],"athlete_sex":row[2],"sport":row[3],"event":row[4],"medal":row[5]})
        # medals_list.append({"athlete_id":row[0]})

    return json.dumps(medals_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser('A sample Flask application/API')
    parser.add_argument('host', help='the host on which this application is running')
    parser.add_argument('port', type=int, help='the port on which this application is listening')
    arguments = parser.parse_args()
    app.run(host=arguments.host, port=arguments.port, debug=True)
