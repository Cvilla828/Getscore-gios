import json
import urllib

class nfl_gameData(object):
    def __init__(self):
        self.week_info = {}
        self.week_info = self.get_game_week_info()
        self.scores = self.get_game_score()
        
    def get_game_week_info(self):
        url = "http://www.nfl.com/liveupdate/scorestrip/ss.json"
        info = urllib.request.urlopen(url)
        infos = json.load(info)["gms"]
        return(infos)
        
    def get_game_score(self):
        week_scores = []
        url = "http://www.nfl.com/liveupdate/scorestrip/ss.json"
        info = urllib.request.urlopen(url)
        scores = json.load(info)["gms"]
        week_scores = [
                {
                        'home_t':score['hnn'],
                        'away_t':score['vnn'],
                        'home_s':score['hs'],
                        'away_s': score['vs']
                        }for score in scores
                    ] 
        return(week_scores)
    

    def get_game_info(self, eid):
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
        return (plays)

    def get_past_plays(self, team_name):
        eid = None
        for game in self.week_info:
            if team_name.lower() == game['vnn'].lower() or team_name.lower() == game['hnn'].lower():
                eid = game['eid']
                
        if eid == None:
            return (-1)
        game_info = self.get_game_info(str(eid))
        p=0
        past_plays= {}
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
#week = game_info.week_info
#try: info = urllib.request.urlopen("http://www.nfl.com/liveupdate/game-center/2018092700/2018092700_gtd.json")
#except urllib.error.HTTPError as e:
#    print(e.reason)
#past_plays = game_info.get_past_plays("falcons")
#if past_plays != -1:
#   print(past_plays)

#plays = game_info.get_live_plays()
#print(plays)

#print(game_info.scores)