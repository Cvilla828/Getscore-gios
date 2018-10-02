from operator import itemgetter

# Number of matches per week
MATCHES = 5
ROSTER = 15
POSITIONS = ['QB', 'WR', 'RB', 'TE', 'W/R/T', 'BN']


def parse_scores(scores_json):
    base_json = scores_json['fantasy_content']['leagues']['0']['league'][1]['scoreboard']['0']['matchups']
    matches = [
        {
            'name_team_1': base_json[str(i)]['matchup']['0']['teams']['0']['team'][0][2]['name'],
            'manager_team_1': base_json[str(i)]['matchup']['0']['teams']['0']['team'][0][19]['managers'][0]['manager']['nickname'],
            'name_team_2': base_json[str(i)]['matchup']['0']['teams']['1']['team'][0][2]['name'],
            'manager_team_2': base_json[str(i)]['matchup']['0']['teams']['1']['team'][0][19]['managers'][0]['manager']['nickname'],
            'score_team_1': base_json[str(i)]['matchup']['0']['teams']['0']['team'][1]['team_points']['total'],
            'score_team_2': base_json[str(i)]['matchup']['0']['teams']['1']['team'][1]['team_points']['total'],
            'pred_team_1': base_json[str(i)]['matchup']['0']['teams']['0']['team'][1]['team_projected_points']['total'],
            'pred_team_2': base_json[str(i)]['matchup']['0']['teams']['1']['team'][1]['team_projected_points']['total'],
            'chance_team_1': base_json[str(i)]['matchup']['0']['teams']['0']['team'][1]['win_probability'],
            'chance_team_2': base_json[str(i)]['matchup']['0']['teams']['1']['team'][1]['win_probability']
        } for i in range(0, MATCHES)
    ]
    return matches


def parse_roster(roster_json):
    base_json = roster_json['fantasy_content']['team'][1]['roster']['0']['players']

    roster = []
    for i in range(0, ROSTER):
        temp = base_json.get(str(i), '')
        if temp != '':
            roster.append(
                {
                    'name_full': base_json[str(i)]['player'][0][2]['name']['full'],
                    'position': base_json[str(i)]['player'][1]['selected_position'][1]['position'],
                    'team': base_json[str(i)]['player'][0][5].get(
                        'editorial_team_full_name', base_json[str(i)]['player'][0][7].get(
                            'editorial_team_full_name',
                            base_json[str(i)]['player'][0][6].get('editorial_team_full_name', ''))),
                    'status': base_json[str(i)]['player'][0][3].get('status', '')
                }
            )
    rtn_roster = []
    for position in POSITIONS:
        for player in roster:
            if player['position'] == position:
                rtn_roster.append(player)

    return rtn_roster


def parse_standings(standings_json):
    base_json = standings_json['fantasy_content']['leagues']['0']['league'][1]['standings'][0]['teams']
    count = int(base_json['count'])
    stands = [
        {
            'name': base_json[str(i)]['team'][0][2]['name'],
            'wins': int(base_json[str(i)]['team'][2]['team_standings']['outcome_totals']['wins']),
            'losses': int(base_json[str(i)]['team'][2]['team_standings']['outcome_totals']['losses']),
            'ties': int(base_json[str(i)]['team'][2]['team_standings']['outcome_totals']['ties']),
            'points_for': float(base_json[str(i)]['team'][2]['team_standings']['points_for']),
            'points_against': float(base_json[str(i)]['team'][2]['team_standings']['points_against']),
            'rank': int(base_json[str(i)]['team'][2]['team_standings']['rank']),
            'streak': base_json[str(i)]['team'][2]['team_standings']['streak']
        } for i in range(0, count)
    ]
    return stands
