import json
import urllib
import xmltodict
import xml.etree.ElementTree as ET


class NFLGameData(object):
    def __init__(self):
        self.week_info = self.get_game_week_info()
        self.scores = self.get_game_score()
        self.teams = {
            "KC": "chiefs",
            "NE": "patriots",
            "LA": "rams",
            "DEN": "broncos",
            "JAX": "jaguars",
            "DAL": "cowboys",
            "BAL": "ravens",
            "TEN": "titans",
            "TB": "buccaneers",
            "ATL": "falcons",
            "PIT": "steelers",
            "CIN": "bengals",
            "LAC": "chargers",
            "CLE": "browns",
            "ARI": "cardinals",
            "CHI": "bears",
            "BUF": "bills",
            "IND": "colts",
            "HOU": "texans",
            "DET": "lions",
            "MIA": "dolphins",
            "MIN": "vikings",
            "NYJ": "jets",
            "CAR": "panthers",
            "PHI": "eagles",
            "NO": "saints",
            "WAS": "redskins",
            "SF": "49ers",
            "NYG": "giants",
            "ATL": "falcons",
            "GB": "packers",
            "OAK": "raiders",
            "SEA": "seahawks"
        }

    @staticmethod
    def get_game_week_info():
        url = "http://www.nfl.com/liveupdate/scorestrip/ss.json"
        info = urllib.request.urlopen(url)
        return json.load(info)["gms"]

    @staticmethod
    def get_game_score():
        url = "http://www.nfl.com/liveupdate/scorestrip/ss.xml"
        info = urllib.request.urlopen(url)
        data = info.read()
        scores = xmltodict.parse(data)['ss']['gms']['g']
        week_scores = [
                        {
                                'home_t': score['@hnn'],
                                'away_t': score['@vnn'],
                                'home_s': score['@hs'],
                                'away_s': score['@vs'],
                                'h_state': score['@h'],
                                'a_state': score['@v'],
                                'quarter': score['@q'],
                                'time': score['@t'],
                                'day': score['@d'],
                                'redzone': score['@rz'],
                                'poss': (score['@p'] if '@p' in score.keys() else ''),
                                'time_left': (score['@k'] if '@k' in score.keys() else ''),
                                'winner': ''
                        } for score in scores
                     ]
        for size in week_scores:
            if(size['quarter'] == 'F'or size['quarter'] == 'FO') and (int(size['home_s'], 10) > int(size['away_s'], 10)):
                size['winner'] = size['home_t']
            elif (size['quarter'] == 'F'or size['quarter'] == 'FO') and (int(size['home_s'], 10) < int(size['away_s'], 10)):
                size['winner'] = size['away_t']
            elif size['quarter'] == 'F'or size['quarter'] == 'FO':
                size['winner'] = 'tie'
        return week_scores

    @staticmethod
    def get_game_score_by_team(team_name):
        url = "http://www.nfl.com/liveupdate/scorestrip/ss.xml"
        info = urllib.request.urlopen(url)
        data = info.read()
        scores = xmltodict.parse(data)['ss']['gms']['g']

        for score in scores:
            if team_name.lower() == score['@vnn'].lower() or team_name.lower() == score['@hnn'].lower():
                team_scores = [
                    {
                        'home_t': score['@hnn'],
                        'away_t': score['@vnn'],
                        'home_s': score['@hs'],
                        'away_s': score['@vs'],
                        'h_state': score['@h'],
                        'a_state': score['@v'],
                        'quarter': score['@q'],
                        'time': score['@t'],
                        'day': score['@d'],
                        'redzone': score['@rz'],
                        'poss': (score['@p'] if '@p' in score.keys() else ''),
                        'time_left': (score['@k'] if '@k' in score.keys() else ''),
                        'winner': ''
                        }
                     ]
        for team_score in team_scores:
            if (team_score['quarter'] == 'F'or team_score['quarter'] == 'FO') and (int(team_score['home_s'], 10) > int(team_score['away_s'], 10)):
                team_score['winner'] = team_score['home_t']
            elif (team_score['quarter'] == 'F'or team_score['quarter'] == 'FO') and (int(team_score['home_s'], 10) < int(team_score['away_s'], 10)):
                team_score['winner'] = team_score['away_t']
            elif team_score['quarter'] == 'F'or team_score['quarter'] == 'FO':
                team_score['winner'] = 'tie'
        return team_scores

    @staticmethod
    def get_game_info(eid):
        url = "http://www.nfl.com/liveupdate/game-center/%s/%s_gtd.json" % (eid, eid)
        game_play_info = None
        home_info = None
        away_info = None
        try:
            info = urllib.request.urlopen(url)
            game_play_info = json.load(info)[eid]["drives"]
            info = urllib.request.urlopen(url)
            home_info = json.load(info)[eid]["home"]
            info = urllib.request.urlopen(url)
            away_info = json.load(info)[eid]["away"]
        except urllib.error.HTTPError:
            # print("Cannot Load %s, game not found" % (url))
            pass
        return game_play_info, home_info, away_info
    # print(json.dumps(game_play_info, indent=4, sort_keys=True))

    def get_live_plays(self):
        plays = {}
        all_plays = {}
        self.week_info = self.get_game_week_info()
        for game in self.week_info:
            eid = game['eid']
            game_info, home_info, away_info = self.get_game_info(str(eid))
#            for i in game_info:
#                if i == "crntdrv":
#                    break
#                current_play = [
#                        {
#                                'quarter': game_info[i]['plays'][str(j)]['qtr'],
#                                'desc': game_info[i]['plays'][str(j)]['desc'],
#                                'drive': str(i),
#                                'play_num': str(j),
#                                'printed':'no'
#                        }for j in game_info[i]["plays"]
#                        ]
            if game_info is not None:
                info = {}
                info['home_t'] = home_info['abbr']
                info['away_t'] = away_info['abbr']
                for i in game_info:
                    if i == "crntdrv":
                        break
                    for j in game_info[i]["plays"]:
                        string = game_info[i]["plays"][str(j)]["desc"]
                        if string.find("TOUCHDOWN") != -1:
                            past_plays = {}
                            past_plays['desc'] = string
                            past_plays['quarter'] = game_info[i]["plays"][str(j)]['qtr']
                            past_plays['poss'] = game_info[i]["plays"][str(j)]['posteam']
                            past_plays['play'] = "TOUCHDOWN"
                            past_plays['poss_alias'] = self.teams.get(past_plays['poss'], "")

                            # print(string + '\n')
                            plays[str(j)] = past_plays

                        # New line
                        elif string.upper().find("INTERCEPT") != -1:
                            past_plays = {}
                            past_plays['desc'] = string
                            past_plays['quarter'] = game_info[i]["plays"][str(j)]['qtr']
                            past_plays['poss'] = game_info[i]["plays"][str(j)]['posteam']
                            past_plays['play'] = "INTERCEPTION"
                            past_plays['poss_alias'] = self.teams.get(past_plays['poss'], "")
                            # print(string + '\n')
                            plays[str(j)] = past_plays
                        elif string.upper().find("FIELD GOAL") != -1 and string.upper().find("NULL") == -1:
                            past_plays = {}
                            past_plays['desc'] = string
                            past_plays['quarter'] = game_info[i]["plays"][str(j)]['qtr']
                            past_plays['poss'] = game_info[i]["plays"][str(j)]['posteam']
                            past_plays['play'] = "FIELD GOAL"
                            past_plays['poss_alias'] = self.teams.get(past_plays['poss'], "")
                            # print(string + '\n')
                            plays[str(j)] = past_plays
                info['plays'] = plays
                all_plays[str(eid)] = info
            # plays[eid] = current_play
        return all_plays

    def get_past_plays(self, team_name):
        eid = None
        self.week_info = self.get_game_week_info()
        for game in self.week_info:
            if team_name.lower() == game['vnn'].lower() or team_name.lower() == game['hnn'].lower():
                eid = game['eid']
                
        if eid is None:
            return -1
        game_info, home_info, away_info = self.get_game_info(str(eid))
        plays = {}
#        past_plays = {}
        info = {}
        info['home_t'] = home_info['abbr']
        info['away_t'] = away_info['abbr']
        for i in game_info:
            if i == "crntdrv":
                break
            for j in game_info[i]["plays"]:
                
                string = game_info[i]["plays"][str(j)]["desc"]
                if string.upper().find("TOUCHDOWN") != -1 and string.upper().find("NULL") == -1:
                    past_plays = {}
                    past_plays['desc'] = string
                    past_plays['quarter'] = game_info[i]["plays"][str(j)]['qtr']
                    past_plays['poss'] = game_info[i]["plays"][str(j)]['posteam']
                    past_plays['play'] = "TOUCHDOWN"
                    past_plays['poss_alias'] = self.teams.get(past_plays['poss'], "")
                    # print(string + '\n')
                    plays[str(j)] = past_plays
                #New line
                elif string.upper().find("INTERCEPT") != -1:
                    past_plays = {}
                    past_plays['desc'] = string
                    past_plays['quarter'] = game_info[i]["plays"][str(j)]['qtr']
                    past_plays['poss'] = game_info[i]["plays"][str(j)]['posteam']
                    past_plays['play'] = "INTERCEPTION"
                    past_plays['poss_alias'] = self.teams.get(past_plays['poss'], "")
                    # print(string + '\n')
                    plays[str(j)] = past_plays
                elif string.upper().find("FIELD GOAL") != -1 and string.upper().find("NULL") == -1:
                    past_plays = {}
                    past_plays['desc'] = string
                    past_plays['quarter'] = game_info[i]["plays"][str(j)]['qtr']
                    past_plays['poss'] = game_info[i]["plays"][str(j)]['posteam']
                    past_plays['play'] = "FIELD GOAL"
                    past_plays['poss_alias'] = self.teams.get(past_plays['poss'], "")
                    # print(string + '\n')
                    plays[str(j)] = past_plays
            info['plays'] = plays
        return info
    

    

#game_info= NFLGameData()
#week = game_info.get_past_plays('rams')
#for i in week['plays']:
#    print(week['plays'][i]['quarter'])

# file=open('test.json', 'w')
# file.write(json.dumps(week, sort_keys=True, indent=4))
# file.close()
#week = game_info.get_game_score()
#print(week)
#try: info = urllib.request.urlopen("http://www.nfl.com/liveupdate/game-center/2018092700/2018092700_gtd.json")
#except urllib.error.HTTPError as e:
#    print(e.reason)
#past_plays = game_info.get_past_plays("falcons")
#if past_plays != -1:
#   print(past_plays)

#plays = game_info.get_live_plays()
#print(plays)

#print(game_info.scores)
