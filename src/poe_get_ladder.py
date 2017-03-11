import pathofexile.pathofexile.api as poe

leagues = poe.get_leagues() # Gets the 50 last leagues
standard_league_id = leagues[0]['id']
top_100 = poe.get_ladder_segment(standard_league_id, ladder_limit=100)

# Print out the top 100
for i,entry in enumerate(top_100['entries']):
    print('{0}: {1}'.format(i + 1, entry['character']['name']))
