import json
import urllib


def get_game_week_info():
    url = "http://www.nfl.com/liveupdate/scorestrip/ss.json"
    info = urllib.request.urlopen(url)
    week_info = json.load(info)["gms"]
    return(week_info)

def get_game_info(eid):
    url = "http://www.nfl.com/liveupdate/game-center/%s/%s_gtd.json" % (eid, eid)
    info = urllib.request.urlopen(url)
    game_play_info = json.load(info)[eid]["drives"]
    return game_play_info
    #print(json.dumps(game_play_info, indent=4, sort_keys=True))

game_info = get_game_info("2018091603")
d = 1
print(game_info[str(d)]["plays"])

for i in game_info:
    print(i["plays"])
    print(json.dumps(i, indent=4, sort_keys=True))
    #for j in i:
       # print(j)
