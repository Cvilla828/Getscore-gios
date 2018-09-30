import json
import urllib
import xmltodict
import xml.etree.ElementTree as ET

class nfl_gameData(object):
    def __init__(self):
        self.week_info = {}
        self.week_info = self.get_game_week_info()
        self.scores = self.get_game_score()

    @staticmethod
    def get_game_week_info():
        url = "http://www.nfl.com/liveupdate/scorestrip/ss.json"
        info = urllib.request.urlopen(url)
        infos = json.load(info)["gms"]
        return infos

    @staticmethod
    def get_game_score():
        url = "http://www.nfl.com/liveupdate/scorestrip/ss.xml"
        info = urllib.request.urlopen(url)
        data = info.read()
        scores = xmltodict.parse(data)['ss']['gms']['g']
        week_scores = [
                        {
                                'home_t':score['@hnn'],
                                'away_t':score['@vnn'],
                                'home_s':score['@hs'],
                                'away_s': score['@vs'],
                                'h_state':score['@h'],
                                'a_state':score['@v'],
                                'quarter':score['@q'],
                                'time':score['@t'],
                                'day':score['@d'],
                                'redzone': score['@rz'],
                                'poss':(score['@p'] if '@p' in score.keys() else ''),
                                'time_left':(score['@k'] if '@k' in score.keys() else ''),
                                'winner':''
                        } for score in scores
                     ]
        for size in week_scores:
            if (size ['quarter'] == 'F'or size['quarter'] == 'FO') and (size['home_s'] > size['away_s']):
                size['winner'] = size['home_t']
            elif (size['quarter'] == 'F'or size['quarter'] == 'FO') and (size['home_s'] < size['away_s']):
                size['winner'] = size['away_t']
            elif(size['quarter'] == 'F'or size['quarter'] == 'FO'):
                size['winner'] = 'tie'
        return week_scores
    
    def get_game_score_by_team(self, team_name):
        url = "http://www.nfl.com/liveupdate/scorestrip/ss.xml"
        info = urllib.request.urlopen(url)
        data = info.read()
        scores = xmltodict.parse(data)['ss']['gms']['g']

        for score in scores:
            if team_name.lower() == score['@vnn'].lower() or team_name.lower() == score['@hnn'].lower():
                team_scores =[
                    {
                        'home_t':score['@hnn'],
                        'away_t':score['@vnn'],
                        'home_s':score['@hs'],
                        'away_s': score['@vs'],
                        'h_state':score['@h'],
                        'a_sate':score['@v'],
                        'quarter':score['@q'],
                        'time':score['@t'],
                        'day':score['@d'],
                        'redzone': score['@rz'],
                        'poss':(score['@p'] if '@p' in score.keys() else ''),
                        'time_left':(score['@k'] if '@k' in score.keys() else ''),
                        'winner':''
                        }
                     ]
        for team_score in team_scores:
            if (team_score['quarter'] == 'F'or team_score['quarter'] == 'FO') and (team_score['home_s'] > team_score['away_s']):
                team_score['winner'] = team_score['home_t']
            elif (team_score['quarter'] == 'F'or team_score['quarter'] == 'FO') and (team_score['home_s'] < team_score['away_s']):
                team_score['winner'] = team_score['away_t']
            elif(team_score['quarter'] == 'F'or team_score['quarter'] == 'FO'):
                team_score['winner'] = 'tie'
        return team_scores

    @staticmethod
    def get_game_info(eid):
        url = "http://www.nfl.com/liveupdate/game-center/%s/%s_gtd.json" % (eid, eid)
        info = urllib.request.urlopen(url)
        game_play_info = json.load(info)[eid]["drives"]
        return game_play_info
    #print(json.dumps(game_play_info, indent=4, sort_keys=True))

    def get_live_plays(self):
        eid = None
        plays = []
        current_play = None
        for game in self.week_info:
            eid = game['eid']
            game_info = self.get_game_info(str(eid))
            for i in game_info:
                if i == "crntdrv":
                    break
                current_play = [
                        {
                                'quarter': game_info[i]['plays'][str(j)]['qtr'],
                                'desc': game_info[i]['plays'][str(j)]['desc'],
                                'drive': str(i),
                                'play_num': str(j),
                                'printed':'no'
                        }for j in game_info[i]["plays"]
                        ]
            plays.insert(eid, current_play)
            #plays[eid] = current_play
        return plays

    def get_past_plays(self, team_name):
        eid = None
        for game in self.week_info:
            if team_name.lower() == game['vnn'].lower() or team_name.lower() == game['hnn'].lower():
                eid = game['eid']
                
        if eid is None:
            return -1
        game_info = self.get_game_info(str(eid))
        p = 0
        past_plays = {}
        for i in game_info:
            if i == "crntdrv":
                break
            for j in game_info[i]["plays"]:
                string = game_info[i]["plays"][str(j)]["desc"]
                if string.find("TOUCHDOWN") != -1:
                    past_plays[p] = string
                    p=+1
        return past_plays
    

    

#game_info= nfl_gameData()
#week = game_info.get_game_score_by_team('Rams')
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
