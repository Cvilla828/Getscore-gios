"""Welcome to our junk drawer"""


def format_scores(scores, score_type):
    """Used to format the match up scores and prediction messages"""
    # TODO: Possibly center text so it has vs in middle
    message = ''
    score_1 = score_type + '_team_1'
    score_2 = score_type + '_team_2'
    for score in scores:
        message += ("%s - %s vs %s - %s\n" % (score["name_team_1"], score[score_1], score[score_2],
                                              score["name_team_2"]))
    return '```' + message + '```'
