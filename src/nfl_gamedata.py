import json
import urllib

def get_game_week_info():
    url = "http://www.nfl.com/liveupdate/scorestrip/ss.json"
    info = urllib.request.urlopen(url)
    week_info = json.load(info)["gms"]
    return(week_info)

def get_game_info(eid):
    url = "http://www.nfl.com/liveupdate/game-center/%s/%s_gtd.json"
    info = urllib.request.urlopen(url)
    game_play_info = json.loa(info)["drives"]

print(get_game_week_info())
