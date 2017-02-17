from __future__ import print_function
import time
import pathofexile.pathofexile.api as poe
import pathofexile.pathofexile.ladder as poe_ladder

def write_league_to_table(league, cursor, table):
    ''' Writes a single league into an sqlite table
    
        :param league: Dictionary. Should contain 'startAt', 'description',
            'registerAt', 'url', 'endAt', 'id', 'rules', and 'event' keys.
        :param cursor: sqlite3.Cursor. A cursor connected to the database that
            contains the table to input leagues into.
        :param table: String. The table to insert leagues into.
        :return: Does not return.
    '''
    league_tuple = (str(league['id']),
                    str(league['description']),
                    str(league['startAt']),
                    str(league['endAt']),
                    str(league['registerAt']),
                    str(league['url']),
                    str(league['rules']),
                    int(league['event']))
    cursor.execute('INSERT INTO {} VALUES (?,?,?,?,?,?,?,?)'.format(table),
                   league_tuple)
    pass

def single_call_to_table(league_list, cursor, table):
    ''' Takes the returned list of leagues in a single API call and inputs them
        to a given SQLite table
    
        :param league_list: A list of league dicts. Each dict should have the
            keys: 'startAt', 'description', 'registerAt', 'url', 'endAt', 'id',
            'rules', and 'event'.
        :param cursor: sqlite3.Cursor. A cursor connected to the database that
            contains the table to input leagues into.
        :param table: String. The table to insert leagues into.
        :return: Does not return.
    '''
    for league in league_list:
        write_league_to_table(league, cursor, table)
    pass

def leagues_to_table(cursor, table, leagues_per_call, max_offset):
    ''' Leagues via the Path of Exile API and inputs them
        in an SQLite table

        :param cursor: sqlite3.Cursor. A cursor connected to the database that
            contains the table to input leagues into.
        :param table: String. The SQLite table name to store the leagues.
        :param leagues_per_call: Positive int. Number of leagues to get each
            API call.
        :param max_offset: Non-negative int or None. The highest offset to
            retrieve leagues from the API with. If None retrieves results
            until there are no leagues returned.
        :return: Does not return.
    '''
    offset = 0
    while True:
        print(offset)
        league_list = poe.get_leagues(league_type='all', 
                                      compact_info=0, 
                                      league_limit=leagues_per_call, 
                                      league_offset=offset)
        if len(league_list) == 0 :
            break
        single_call_to_table(league_list, cursor, table)
        offset += len(league_list)
        if max_offset != None and offset > max_offset:
            break
        time.sleep(5) # Wait so that the API does not throttle my requests
    pass

def all_leagues_to_table(cursor, table):
    ''' Collects all of the leagues via the Path of Exile API and inputs them
        in an SQLite table
    
        :param cursor: sqlite3.Cursor. A cursor connected to the database that
            contains the table to input leagues into.
        :param table: String. The SQLite table name to store the leagues.
        :return: Does not return.
    '''
    leagues_to_table(cursor, table, leagues_per_call=50, max_offset = None) 
    pass

def get_leagues_from_table(cursor, table):
    ''' Gets all the league ids and return in a list '

         :param cursor: sqlite3.Cursor. A cursor connected to the database that
            contains the table to input leagues into.
        :param table: String. The SQLite table that has the leagues.
        :return: List.
    '''
    cursor.execute('SELECT id FROM {}'.format(table))
    ids = [x[0] for x in cursor.fetchall()]
    return ids

def ladder_to_table(league_id, cursor, ladder_table):
    ''' Given a league id, adds all the players in the league to a table

        :param league_id: String.
        :param cursor: sqlite3.Cursor. A cursor connected to the database that
            contains the table to input leagues into.
        :param ladder_table: String. The SQLite table name to store the ladder.
        :return: Does not return.
    '''
    ladder = poe_ladder.retrieve(league_id)
    for entry in ladder:
        if 'twitch' in entry['account']:
            twitch = entry['account']['twitch']['name']
        else:
            twitch = 'NULL'
        ladder_tuple = (unicode(league_id),
                        unicode(entry['account']['name']),
                        unicode(twitch),
                        int(entry['account']['challenges']['total']),
                        unicode(entry['character']['name']),
                        int(entry['rank']),
                        unicode(entry['character']['class']),
                        int(entry['character']['experience']),
                        int(entry['dead']))
        cursor.execute(''' INSERT INTO {}
                           VALUES (?,?,?,?,?,?,?,?, ?)
                       '''.format(ladder_table), ladder_tuple)
    pass

def all_ladders_to_table(league_ids, cursor, ladder_table):
   """ Given a list of league_ids populates ladder_table with their ladders

       :param league_ids: List.
       :param cursor: sqlite3.Cursor. A cursor connected to the database that
            contains the table to input leagues into.
        :param ladder_table: String. The SQLite table name to store the ladder.
        :return: Does not return.
   """
   i = 0
   for league_id in league_ids:
       if i % 100:
           print('On league {}'.format(i))
       ladder_to_table(league_id, cursor, ladder_table)
