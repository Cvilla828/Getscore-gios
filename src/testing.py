from fantasy_gios import FantasyGios
from yahoo_parser import *

import json

cred_file = '../credentials.json'

ff = FantasyGios(cred_file)

# response_standings = ff.get_standings()
# print(json.dumps(response.json(), indent=4, sort_keys=True))

# response.json()['fantasy_content']['leagues']['0']['league'][1]['scoreboard']['0']['matchups']['0']['matchup']['0']['teams']['0']['team'][0][2]['name']
# response.json()['fantasy_content']['leagues']['0']['league'][1]['scoreboard']['0']['matchups']['0']['matchup']['0']['teams']['0']['team'][1]['team_points']['total']
# response.json()['fantasy_content']['leagues']['0']['league'][1]['scoreboard']['0']['matchups']['0']['matchup']['0']['teams']['0']['team'][1]['team_projected_points']['total']
# response.json()['fantasy_content']['leagues']['0']['league'][1]['scoreboard']['0']['matchups']['0']['matchup']['0']['teams']['0']['team'][1]['win_probability']

# response_scores = ff.get_score()
# test = parse_scores(response_scores.json())
# print(format_scores(test, 'pred'))
# print(format_scores(test, 'score'))

response_roster = ff.get_team_roster('Null Packets')

ff.renew_token()
temp =response_roster.json()
print(json.dumps(response_roster.json(), indent=4, sort_keys=True))
import pdb; pdb.set_trace()
