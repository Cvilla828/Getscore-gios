from fantasy_gios import FantasyGios
from yahoo_parser import *
import json

cred_file = '../credentials.json'

test = FantasyGios(cred_file)

response = test.get_standings(test.session)
print(json.dumps(response.json(), indent=4, sort_keys=True))

# response.json()['fantasy_content']['leagues']['0']['league'][1]['scoreboard']['0']['matchups']['0']['matchup']['0']['teams']['0']['team'][0][2]['name']
# response.json()['fantasy_content']['leagues']['0']['league'][1]['scoreboard']['0']['matchups']['0']['matchup']['0']['teams']['0']['team'][1]['team_points']['total']
# response.json()['fantasy_content']['leagues']['0']['league'][1]['scoreboard']['0']['matchups']['0']['matchup']['0']['teams']['0']['team'][1]['team_projected_points']['total']
# response.json()['fantasy_content']['leagues']['0']['league'][1]['scoreboard']['0']['matchups']['0']['matchup']['0']['teams']['0']['team'][1]['win_probability']

response = test.get_score(test.session)
test = parse_scores(response.json())
import pdb; pdb.set_trace()
print(json.dumps(response.json(), indent=4, sort_keys=True))