import time
import slackclient as SC
import operator
import json


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
            attachments=json.dumps([a.to_dict() for a in self.attachments])
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
        d['mrkdwn_in'] = []
        if self.fallback is not None: 
            d['fallback'] = self.fallback
        if self.title_link is not None:
            d['title_link'] = self.title_link
        if self.pretext is not None:
            d['pretext'] = self.pretext
            d['mrkdwn_in'].append("pretext")
        if self.fields is not None and len(self.fields)>0:
            d['fields'] = self.fields
            d['mrkdwn_in'].append("fields")
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
            d['mrkdwn_in'].append("text")
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

class EchoPost(SlackPost):
    def __init__(self, text, opt_response=None):
        if opt_response is not None:
            super(EchoPost, self).__init__("{} ({})".format(text, opt_response))
        else:
            super(EchoPost, self).__init__(text)

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
            att.add_field("", s['name'], True)
            att.add_field("", pts_wlt, True)
        self.add_attachment(att)


class RosterPost(SlackPost):
    def __init__(self, parsed_roster=None, team_name=None):
        super(RosterPost, self).__init__()
        if parsed_roster is not None and team_name is not None:
            self.set_roster(parsed_roster, team_name)

    def set_roster(self, parsed_roster, team_name):
        status_color = {
            'IR': 'danger',
            'SUSP': 'danger',
            'O': 'danger',
            'Q': 'warning'
        }
        att = SlackPostAttachment()
        att.set_title("GIOS FF - %s's Roster" % team_name, "https://football.fantasysports.yahoo.com/f1/159366")
        self.add_attachment(att)
        for player in parsed_roster:
            att = SlackPostAttachment()
            name = "%s - %s :%s:" % (player['position'], player['name_full'], player['team'].split()[-1])
            att.add_field("", name, False)
            #att.add_field(player['position'], "", True)
            #att.add_field(player['status'], '', True)
            att.set_color(status_color.get(player['status'], 'good'))
            self.add_attachment(att)


class ScoresPost(SlackPost):
    def __init__(self, parsed_scores=None):
        super(ScoresPost, self).__init__()
        if parsed_scores is not None:
            self.set_scores(parsed_scores)
    
    def set_scores(self, parsed_scores):
        att = SlackPostAttachment()
        att.set_title("GIOS FF - Current Scores", "https://football.fantasysports.yahoo.com/f1/159366")
        self.add_attachment(att)
        sel_emoji = (lambda s: (":heavy_check_mark:" if s > 0.85 else (":white_check_mark:" if s > 0.60 else ":transparent:")))
        for score in parsed_scores:
            att = SlackPostAttachment()
            chance1 = score["chance_team_1"]
            chance2 = score["chance_team_2"]
            pred1_orig = float(score["pred_team_1"]) / (float(score["pred_team_1"])+float(score["pred_team_2"]))
            pred2_orig = 1. - pred1_orig
            color = "good"
            if pred1_orig > pred2_orig:
                if chance2-chance1 > 10.:
                    color = "danger"
                elif chance2 > chance1:
                    color = "warning"
            else:
                if chance1-chance2 > 10.:
                    color = "danger"
                elif chance1 > chance2:
                    color = "warning"
            att.set_color(color)
            name1 = "{} *{}* _({})_".format(sel_emoji(chance1), score["name_team_1"].replace("*", "٭"), score["manager_team_1"])
            name2 = "{} *{}* _({})_".format(sel_emoji(chance2), score["name_team_2"].replace("*", "٭"), score["manager_team_2"])
            value1 = ":transparent: {}/{} - *{}%*".format(score["score_team_1"], score["pred_team_1"], int(100*chance1))
            value2 = ":transparent: {}/{} - *{}%*".format(score["score_team_2"],score["pred_team_2"], int(100*chance2))
            att.add_field("", name1, True)
            att.add_field("", name2, True)
            att.add_field("", value1, True)
            att.add_field("", value2, True)
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
                att.add_field('', '@' + value + 'ET', True)
                value = score['away_t'] + " :" + score['away_t'].lower() +":"
                att.add_field('', value, True)
                att.set_color('#439FE0')
            
            elif(score['quarter'] == 'F'or score['quarter'] == 'FO'):
                value = score['quarter']
                att.add_field('',value, True)
                value = score['home_t'] + " :" + score['home_t'].lower() +":" + str(score['home_s'])
                if score['winner'] == score['home_t']:
                    value = ':trophy: ' + value
                else:
                    value = ':transparent: ' + value
                att.add_field('', value, True)
                value = score['winner']
                att.add_field('', value.upper(), True)
                value = score['away_t'] + " :" + score['away_t'].lower() +":" + str(score['away_s'])
                if score['winner'] == score['away_t']:
                    value = ':trophy: ' + value
                else:
                    value = ':transparent: ' + value
                att.add_field('', value, True)
                att.set_color('#000000')
            
            else:
                value = score['quarter']
                att.add_field('','QTR: '+ value, True)
                value = score['home_t'] + " :" + score['home_t'].lower() +":" + " " + str(score['home_s'])
                if(score['poss'] == score['h_state']):
                    value = ':football: ' + value
                else:
                    value = ':transparent: ' + value
                att.add_field('', value , True)
                value = score['time_left']
                att.add_field('', value, True)
                value = score['away_t'] + " :" + score['away_t'].lower() +":"+ " " + str(score['away_s'])
                if(score['poss'] == score['a_state']):
                    value = ':football: ' + value
                else:
                    value = ':transparent: ' + value
                att.add_field('', value, True)
                if score['redzone'] == '1':
                    att.set_color('danger')
                else:
                    att.set_color('good')
            
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
                att.add_field('', '@' + value + 'ET', True)
                value = score['away_t'] + " :" + score['away_t'].lower() +":"
                att.add_field('', value, True)
                att.set_color('#439FE0')
            
            elif(score['quarter'] == 'F'or score['quarter'] == 'FO'):
                value = score['quarter']
                att.add_field('',value, True)
                value = score['home_t'] + " :" + score['home_t'].lower() +":" + str(score['home_s'])
                if score['winner'] == score['home_t']:
                    value = ':trophy: ' + value
                else:
                    value = ':transparent: ' + value
                att.add_field('', value, True)
                value = score['winner']
                att.add_field('', value.upper(), True)
                value = score['away_t'] + " :" + score['away_t'].lower() +":" + str(score['away_s'])
                if score['winner'] == score['away_t']:
                    value = ':trophy: ' + value
                else:
                    value = ':transparent: ' + value
                att.add_field('', value, True)
                att.set_color('#000000')
            
            else:
                value = score['quarter']
                att.add_field('','QTR: '+ value, True)
                value = score['home_t'] + " :" + score['home_t'].lower() +":" + " " + str(score['home_s'])
                if(score['poss'] == score['h_state']):
                    value = ':football: ' + value
                else:
                    value = ':transparent: ' + value
                att.add_field('', value , True)
                value = score['time_left']
                att.add_field('', value, True)
                value = score['away_t'] + " :" + score['away_t'].lower() +":"+ " " + str(score['away_s'])
                if(score['poss'] == score['a_state']):
                    value = ':football: ' + value
                else:
                    value = ':transparent: ' + value
                att.add_field('', value, True)
                if score['redzone'] == '1':
                    att.set_color('danger')
                else:
                    att.set_color('good')
            
            self.add_attachment(att)

class NFLPlaysPost(SlackPost):
    def __init__(self, nfl_plays=None, play_type=None):
        super(NFLPlaysPost, self).__init__()
        if nfl_plays is not None and play_type == 'league':
            self.set_nfl_plays(nfl_plays)
        if nfl_plays is not None and play_type == 'team':
            self.set_nfl_plays_by_name(nfl_plays)
        
    def set_nfl_plays(self, nfl_plays):
        title = "Past NFL Plays :nfl:" 
        att = SlackPostAttachment()
        att.set_title(title, "https://sports.yahoo.com/nfl/scoreboard/")
        self.add_attachment(att)
    
    def set_nfl_plays_by_name(self, nfl_plays):
        title = "Past NFL Plays %s vs %s :nfl:" % (nfl_plays['home_t'], nfl_plays['away_t'])
        att = SlackPostAttachment()
        att.set_title(title, "https://sports.yahoo.com/nfl/scoreboard/")
        self.add_attachment(att)
        for play in nfl_plays['plays']:
            att = SlackPostAttachment()
            value = "QTR"
            att.add_field('', value, True)
            value = 'Possession: %s' % (play['poss']) 
            att.add_field('', value, True)
            value = score['desc']
            att.add_field('', value, True)
            att.set_color('#000000')