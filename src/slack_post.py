import time
import slackclient as SC
import operator
import json

GREEN_CHECK_THRESHOLD = 0.85
WHITE_CHECK_THRESHOLD = 0.60
ENABLE_EMOJI = True

class SlackPost(object):

    def __init__(self, text=None):
        self.text = text
        self.attachments = []
    
    def add_attachment(self, att):
        self.attachments.append(att)
    
    def send(self, slack_client, channel):
        if self.text is None and len(self.attachments) < 1:
            raise AttributeError
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=self.text,
            attachments=json.dumps([a.to_dict() for a in self.attachments]),
        )


class SlackPostAttachment(object):

    def __init__(self, title=""):
        self.fields = []
        self.set_title(title, None)
        self.set_fallback(None)
        self.set_pretext(None)
        self.set_color(None)
        self.set_author(None)
        self.set_text(None)
        self.set_image()
        self.set_footer()
    
    def add_field(self, title, value, two_col=False):
        self.fields.append({
            'title': title,
            'value': value,
            'short': two_col
        })

    def set_title(self, title, title_link=None):
        self.title = title
        self.title_link = title_link
    
    def set_fallback(self, fallback):
        self.fallback = fallback

    def set_pretext(self, pretext):
        self.pretext = pretext

    def set_color(self, color):
        self.color = color

    def set_author(self, name, link=None, icon_url=None):
        self.author_name = name
        self.author_link = link
        self.author_icon = icon_url
    
    def set_text(self, text):
        self.text = text
    
    def set_image(self, image_url=None, thumb_url=None):
        self.image_url = image_url
        self.thumb_url = thumb_url
    
    def set_footer(self, text=None, icon_url=None, show_timestamp=False):
        self.footer = text
        self.footer_icon = icon_url
        self.show_timestamp = show_timestamp

    def to_dict(self):
        d = {}
        d['title'] = self.title
        if self.fallback is not None: 
            d['fallback'] = self.fallback
        if self.title_link is not None:
            d['title_link'] = self.title_link
        if self.pretext is not None:
            d['pretext'] = self.pretext
        if self.fields is not None and len(self.fields)>0:
            d['fields'] = self.fields
        if self.color is not None:
            d['color'] = self.color
        if self.author_name is not None:
            d['author_name'] = self.author_name
        if self.author_link is not None:
            d['author_link'] = self.author_link
        if self.author_icon is not None:
            d['author_icon'] = self.author_icon
        if self.text is not None:
            d['text'] = self.text
        if self.image_url is not None:
            d['image_url'] = self.image_url
        if self.thumb_url is not None:
            d['thumb_url'] = self.thumb_url
        if self.footer is not None:
            d['footer'] = self.footer
        if self.footer_icon is not None:
            d['footer_icon'] = self.footer_icon
        if self.show_timestamp:
            d['ts'] = int(time.time())
        return d

class StandingsPost(SlackPost):
    def __init__(self, parsed_standings=None):
        super(StandingsPost, self).__init__()
        if parsed_standings is not None:
            self.set_standings(parsed_standings)
    
    def set_standings(self, parsed_standings):
        # 'name': base_json[str(i)]['team'][0][2]['name'],
        # 'wins': base_json[str(i)]['team'][2]['team_standings']['outcome_totals']['wins'],
        # 'losses': base_json[str(i)]['team'][2]['team_standings']['outcome_totals']['losses'],
        # 'ties': base_json[str(i)]['team'][2]['team_standings']['outcome_totals']['ties'],
        # 'points_for': base_json[str(i)]['team'][2]['team_standings']['points_for'],
        # 'points_against': base_json[str(i)]['team'][2]['team_standings']['points_against'],
        # 'rank': base_json[str(i)]['team'][2]['team_standings']['rank'],
        # 'streak': base_json[str(i)]['team'][2]['team_standings']['streak']
        emoji = {
            1: ":first_place_medal:",
            2: ":second_place_medal:",
            3: ":third_place_medal:",
            10: ":rip:"
        }
        ordered = sorted(parsed_standings, key=operator.itemgetter('rank'))
        att = SlackPostAttachment()
        att.set_title("GIOS FF - Current Standings", "https://football.fantasysports.yahoo.com/f1/159366")
        for s in ordered:
            pts_wlt = "{:3.2f} ({}-{}-{}) {}".format(s['points_for'], s['wins'], s['losses'], s['ties'], emoji.get(s['rank'], ":transparent:"))
            att.add_field(s['name'], "", True)
            att.add_field(pts_wlt, "", True)
        self.add_attachment(att)


class RosterPost(SlackPost):
    def __init__(self, parsed_roster=None, team_name=None):
        super(RosterPost, self).__init__()
        if parsed_roster is not None and team_name is not None:
            self.set_roster(parsed_roster, team_name)

    def set_roster(self, parsed_roster, team_name):
        att = SlackPostAttachment()
        att.set_title("GIOS FF - %s's Roster" % team_name, "https://football.fantasysports.yahoo.com/f1/159366")
        self.add_attachment(att)
        for player in parsed_roster:
            att = SlackPostAttachment()
            name = "%s - %s :%s:" % (player['position'], player['name_full'], player['team'].split()[-1])
            att.add_field(name, "", True)
            #att.add_field(player['position'], "", True)
            att.add_field(player['status'], '', True)
            if(player['status'] == 'IR' or player['status'] == 'O' or player['status']=='SUSP'):
                att.set_color('danger')
            elif(player['status'] == 'Q'):
                att.set_color('warning')
            else:
                att.set_color('good')
            self.add_attachment(att)


class ScoresPost(SlackPost):
    def __init__(self, parsed_scores=None, score_type=None):
        super(ScoresPost, self).__init__()
        if parsed_scores is not None and score_type is not None:
            self.set_scores(parsed_scores, score_type)
    
    def set_scores(self, parsed_scores, score_type):
        title = "Current Scores" if score_type=="score" else ("Initial Predictions" if score_type=="pred" else "???")
        att = SlackPostAttachment()
        att.set_title("GIOS FF - {0}".format(title), "https://football.fantasysports.yahoo.com/f1/159366")
        for score in parsed_scores:
            title = score["name_team_1"] + ("" if not ENABLE_EMOJI else (" :heavy_check_mark:" if score["chance_team_1"] > GREEN_CHECK_THRESHOLD else (" :white_check_mark:" if score["chance_team_1"] > WHITE_CHECK_THRESHOLD else "")))
            value = "{} _({}%)_".format(score["{}_team_1".format(score_type)], int(100*score["chance_team_1"]))
            att.add_field(title, value, True)
            title = score["name_team_2"] + ("" if not ENABLE_EMOJI else (" :heavy_check_mark:" if score["chance_team_2"] > GREEN_CHECK_THRESHOLD else (" :white_check_mark:" if score["chance_team_2"] > WHITE_CHECK_THRESHOLD else "")))
            value = "{} _({}%)_".format(score["{}_team_2".format(score_type)], int(100*score["chance_team_2"]))
            att.add_field(title, value, True)
        self.add_attachment(att)


class NFLScoresPost(SlackPost):
    def __init__(self, nfl_scores=None, score_type=None):
        super(NFLScoresPost, self).__init__()
        if nfl_scores is not None and score_type == 'league':
            self.set_nfl_scores(nfl_scores)
        if nfl_scores is not None and score_type == 'team':
            self.set_nfl_scores_by_name(nfl_scores)
            
    def set_nfl_scores(self, nfl_scores):
        title = "Current NFL Scores :nfl:"
        att = SlackPostAttachment()
        att.set_title(title, "https://sports.yahoo.com/nfl/scoreboard/")
        self.add_attachment(att)
        for score in nfl_scores:
            att = SlackPostAttachment()
            if score['quarter'] == 'P':
                value = score['day']
                att.add_field('', value, True)
                value = score['home_t'] + " :" + score['home_t'].lower() +":"
                att.add_field('', value, True)
                value = score['time']
                att.add_field('', value, True)
                value = score['away_t'] + " :" + score['away_t'].lower() +":"
                att.add_field('', value, True)
            else:
                value = score['quarter']
                att.add_field('','QTR: '+ value, True)
                value = score['home_t'] + " :" + score['home_t'].lower() +":" + " " + score['home_s']
                att.add_field('', value , True)
                value = score['time']
                att.add_field('', value, True)
                value = score['away_t'] + " :" + score['away_t'].lower() +":"+ " " + score['away_s']
                att.add_field('', value, True)
            
            self.add_attachment(att)
            
    def set_nfl_scores_by_name(self, team_score):
        title = "Current NFL Scores :nfl:"
        att = SlackPostAttachment()
        att.set_title(title, "https://sports.yahoo.com/nfl/scoreboard/")
        self.add_attachment(att)
        for score in team_score:
            att = SlackPostAttachment()
            if score['quarter'] == 'P':
                value = score['day']
                att.add_field('', value, True)
                value = score['home_t'] + " :" + score['home_t'].lower() +":"
                att.add_field('', value, True)
                value = score['time']
                att.add_field('', value, True)
                value = score['away_t'] + " :" + score['away_t'].lower() +":"
                att.add_field('', value, True)
            else:
                value = score['quarter']
                att.add_field('','QTR: '+ value, True)
                value = score['home_t'] + " :" + score['home_t'].lower() +":" + " " + score['home_s']
                att.add_field('', value , True)
                value = score['time']
                att.add_field('', value, True)
                value = score['away_t'] + " :" + score['away_t'].lower() +":"+ " " + score['away_s']
                att.add_field('', value, True)
            
            self.add_attachment(att)
