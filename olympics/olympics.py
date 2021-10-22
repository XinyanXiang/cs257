# olympics.py
# Written by Xinyan Xiang, Oct 21, 2021
import argparse
import psycopg2

from config import password
from config import database
from config import user


# some colors we need for our outputs
class bcolors:
    OKGREEN = "\033[0;32m"
    WARNING = "\033[31m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"

def get_parsed_arguments():
    ''' Create an ArgumentParser object and fill it with information about command lines 
        utilized by this program arguments.
    '''
    parser = argparse.ArgumentParser(add_help=False, description="Olympics Database Searching Tool")
    parser.add_argument("-anoc", "--athlete_noc", nargs="?", const="Noinput") 
    parser.add_argument("-am", "--athlete_medal", nargs="?", const="Noinput") 
    parser.add_argument("-ln", "--last_name", nargs="?", const="Noinput",default = "Nomention") 
    parser.add_argument("-fn", "--first_name", nargs="?", const="Noinput",default = "Nomention") 
    parser.add_argument("-n", "--noc", const = "Noinput", nargs="?")
    parser.add_argument("-cm", "--count_medal", const = "Noinput", nargs="?")
    parser.add_argument("-h", "--help", action = "store_true", dest="help_me")
    parsed_arguments = parser.parse_args()
    return parsed_arguments

def main():
    arguments = get_parsed_arguments()
    try:
        connection = psycopg2.connect(database=database, user=user, password=password)
    except Exception as e:
            print(e)
            exit()
   
    # When the user types the help flag (-h): print the command-line documentation 
    if arguments.help_me:
        f = open("usage.txt", "r")
        file_contents = f.read()
        print(file_contents)
        f.close
    
    # When the user types the athlete_noc flag (-anoc)
    if arguments.athlete_noc:
        if arguments.athlete_noc == "Noinput":
            try:
                cursor = connection.cursor()
                query = 'SELECT athletes.given_name, athletes.surname FROM athletes ORDER BY surname'
                cursor.execute(query)
            except Exception as e:
                    print(e)
                    exit()
            print('===== All athletes from all nocs =====')
            for row in cursor:
                print(row[0], row[1])
            print()
            connection.close()
        else:
            search_string = arguments.athlete_noc.upper()
            query = '''SELECT DISTINCT athletes.given_name, athletes.surname, nocs.region
                       FROM athletes, nocs, athletes_games_noc_biometrics,games
                       WHERE athletes.id = athletes_games_noc_biometrics.athletes_id
                       AND nocs.id = athletes_games_noc_biometrics.noc_id
                       AND games.id = athletes_games_noc_biometrics.game_id
                       AND nocs.noc = %s
                       ORDER BY athletes.surname'''
            try:
                cursor = connection.cursor()
                cursor.execute(query, (search_string,))
            except Exception as e:
                print(e)
                exit()
            print('===== Athletes with NOC {0} ====='.format(search_string))
            for row in cursor:
                print(row[0], row[1])
            print() 
            connection.close()         

    # When the user types noc flag (-n) and count_medal flag (-cm)
    if arguments.noc:
        select_clause = '''SELECT nocs.noc, COUNT(athletes_games_medal.medal)
                FROM nocs,athletes_games_medal,games,athletes_games_noc_biometrics
                WHERE athletes_games_noc_biometrics.athletes_id = athletes_games_medal.athletes_id
                AND athletes_games_noc_biometrics.game_id = athletes_games_medal.game_id
                AND athletes_games_noc_biometrics.game_id = games.id
                AND athletes_games_noc_biometrics.noc_id = nocs.id'''
        noc_string = arguments.noc
        if noc_string != "Noinput":
            noc_string_quote = "'" + noc_string + "'"
            select_clause = select_clause + ''' AND nocs.noc = {0}'''.format(noc_string_quote)
        medal_string = arguments.count_medal
        if medal_string == "Noinput":      
            query = select_clause + ''' GROUP by nocs.noc
            ORDER BY COUNT(athletes_games_medal.medal) DESC'''
        else:
            medal_string_quote = "'" + medal_string + "'"
            query = select_clause + ''' AND athletes_games_medal.medal = {0}
            GROUP by nocs.noc
            ORDER BY COUNT(athletes_games_medal.medal) DESC'''.format(medal_string_quote)
        try:
            cursor = connection.cursor()
            cursor.execute(query)
        except Exception as e:
            print(e)
            exit()
        if noc_string == "Noinput" and medal_string == "Noinput":
            print('===== Number of gold, silver, and bronze medals gained by each NOC =====')
        elif noc_string == "Noinput" and medal_string != "Noinput": 
            print('===== Number of {0} medals gained by each NOC ====='.format(medal_string))
        elif noc_string != "Noinput" and medal_string == "Noinput": 
            print('===== Number of gold, silver, and bronze medals gained by {0} ====='.format(noc_string))
        else:
            print('===== Number of {0} medals gained by {1} ====='.format(medal_string,noc_string))
        for row in cursor:
            print(row[0], f"{bcolors.OKGREEN}{row[1]}{bcolors.ENDC}")
        print() 
        connection.close() 
               
    # When the user types the athlete_medal flag (-am) and the flags fn and ln
    if arguments.athlete_medal:
        if arguments.first_name == "Nomention" and arguments.last_name == "Nomention":
            print("Pleae use -fn and -ln to specify the first name and the last name")
        else:
            if arguments.first_name == "Noinput" or arguments.last_name == "Noinput":
                print("Please provide both first name and last name")
            else:
                first_name = "'" + arguments.first_name + "'"
                last_name = "'" + arguments.last_name + "'"
                query = '''
                SELECT athletes.given_name, athletes.surname, games.game_name,games.year,events.event_name,athletes_games_medal.medal
                FROM athletes,athletes_games_medal,games,events
                WHERE athletes.id = athletes_games_medal.athletes_id
                AND games.id = athletes_games_medal.game_id
                AND events.id = athletes_games_medal.event_id
                AND athletes.given_name = {0}
                AND athletes.surname = {1}
                AND athletes_games_medal.medal != 'NA'
                ORDER BY games.year '''.format(first_name,last_name)
                try:
                    cursor = connection.cursor()
                    cursor.execute(query)
                except Exception as e:
                    print(e)
                    exit() 
                print('===== Medals awared by %s %s ====='% (first_name, last_name))
                for row in cursor:
                    print(row[0], row[1],row[2],row[4],f"{bcolors.OKGREEN}{row[5]}{bcolors.ENDC}")
                print() 
                connection.close() 

if __name__ == "__main__":
    main()










