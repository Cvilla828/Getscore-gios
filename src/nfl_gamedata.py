import json
import urllib

class nfl_gameData(object):
    def __init__(self):
        self.week_info = {}
        self.week_info = get_game_week_info()
        
    def get_game_week_info(self):
        url = "http://www.nfl.com/liveupdate/scorestrip/ss.json"
        info = urllib.request.urlopen(url)
        infos = json.load(info)["gms"]
        return(infos)

    def get_game_info(self, eid):
        url = "http://www.nfl.com/liveupdate/game-center/%s/%s_gtd.json" % (eid, eid)
        info = urllib.request.urlopen(url)
        game_play_info = json.load(info)[eid]["drives"]
        return game_play_info
    #print(json.dumps(game_play_info, indent=4, sort_keys=True))



    def get_past_plays(self, team_name):
        eid = None
        for game in self.week_info:
            if team_name.lower() == game['vnn'].lower() or team_name.lower() == game['hnn'].lower():
                eid = game['eid']
                
        if eid == None:
            return (-1)
        game_info = get_game_info(str(eid))
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
    

    

game_info= nfl_gameData()
week = game_info.week_info

past_plays = game_info.get_past_plays("falcons")
if past_plays != -1:
   print(past_plays)
