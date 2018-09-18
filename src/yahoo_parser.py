
# Number of matches per week
MATCHES = 5


def parse_scores(scores_json):
    base_json = scores_json['fantasy_content']['leagues']['0']['league'][1]['scoreboard']['0']['matchups']
    matches = [
        {
            'name_team_1': base_json[str(i)]['matchup']['0']['teams']['0']['team'][0][2]['name'],
            'name_team_2': base_json[str(i)]['matchup']['0']['teams']['1']['team'][0][2]['name'],
            'score_team_1': base_json[str(i)]['matchup']['0']['teams']['0']['team'][1]['team_points']['total'],
            'score_team_2': base_json[str(i)]['matchup']['0']['teams']['1']['team'][1]['team_points']['total'],
            'pred_team_1': base_json[str(i)]['matchup']['0']['teams']['0']['team'][1]['team_projected_points']['total'],
            'pred_team_2': base_json[str(i)]['matchup']['0']['teams']['1']['team'][1]['team_projected_points']['total'],
            'chance_team_1': base_json[str(i)]['matchup']['0']['teams']['0']['team'][1]['win_probability'],
            'chance_team_2': base_json[str(i)]['matchup']['0']['teams']['1']['team'][1]['win_probability']
        } for i in range(0, MATCHES)
    ]
    return matches
