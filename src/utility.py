"""Welcome to our junk drawer"""

import time

GREEN_CHECK_THRESHOLD = 0.85
WHITE_CHECK_THRESHOLD = 0.60
ENABLE_EMOJI = True

def format_scores(scores, score_type):
    """Used to format the match up scores and prediction messages"""
    # TODO: Possibly center text so it has vs in middle
    att = {}
    att['fallback'] = "no thanks"
    att['title'] = "GIOS FF - Current Results"
    att['title_link'] = "https://football.fantasysports.yahoo.com/f1/159366"
    fields = []
    for score in scores:
        fields.append(get_field(score, score_type, 1))
        fields.append(get_field(score, score_type, 2))
    att['fields'] = fields
    return [att]

def get_field(score, score_type, num):
    d = {}
    chance = score["chance_team_{}".format(num)]
    curr_score = score["{}_team_{}".format(score_type, num)]
    name = score["name_team_{}".format(num)]
    emoji = "" if not ENABLE_EMOJI else (":heavy_check_mark: " if chance > GREEN_CHECK_THRESHOLD else (":white_check_mark: " if chance > WHITE_CHECK_THRESHOLD else ":transparent: "))
    d['title'] = emoji + name
    d['value'] = ":transparent:{} _({}%)_".format(curr_score, int(100*chance))
    d['short'] = True
    return d