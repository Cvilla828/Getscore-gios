
import os
import time
import re
from slackclient import SlackClient
from fantasy_gios import FantasyGios
from yahoo_parser import *
from slack_post import *
import json
from nflgamedata import *

# instantiate Slack client
slack_client = SlackClient(os.environ.get('SLACK_BOT_TOKEN'))
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None

# constants
RTM_READ_DELAY = 1 # 1 second delay between reading from RTM
EXAMPLE_COMMAND = "getscore"
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"
cred_file = '..\credentials.json'

YFS = FantasyGios(cred_file)
YFS.get_team_id()
nfl = NFLGameData()


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and "subtype" not in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None


def parse_direct_mention(message_text):
    """
        Finds a direct mention (a mention that is at the beginning) in message text
        and returns the user ID which was mentioned. If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)
    # the first group contains the username, the second group contains the remaining message
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def handle_command(command, channel):
    """
        Executes bot command if the command is known
    """
    post = None
    parameter = None 
    team = None
    if command.find(' ') != -1:
        parameter = command.split(' ', 1)[1]
        command = command.split(' ', 1)[0]
    
    if parameter not in YFS.team_id:
        team = parameter
    
    commands = ["getscore", "getstandings", "getnflscores", "getroster", "getrespect", "getpastnflplays"]

    if command == "getscore" or command == "getscores":
        post = ScoresPost(parse_scores(YFS.get_score().json()))
    elif command == "getstandings":
        post = StandingsPost(parse_standings(YFS.get_standings().json()))
    elif command == "getnflscores":
        if team is not None:
            post = NFLScoresPost(nfl.get_game_score_by_team(team), 'team')
        else:
            post = NFLScoresPost(nfl.get_game_score(), 'league')
    elif command == "getroster":
        if parameter is not None:
            roster_json = YFS.get_team_roster(parameter)
            if roster_json is not None:
                post = RosterPost(parse_roster(roster_json.json()), parameter)
            else:
                post = EchoPost("Sorry, I couldn't find a team for %s" % parameter)
    elif command == "getrespect":
        post = EchoPost("F", team)
    elif command == "getpastnflplays":
        if team is not None:
            post = NFLPlaysPost(nfl.get_past_plays(team), 'team')
        else:
            post = NFLPlaysPost(nfl.get_live_plays(), 'league')
   
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try one of these: *{}*.".format(", ".join(commands))

    if isinstance(post, SlackPost):
        post.send(slack_client, channel)
    else:
        # Sends the response back to the channel
        slack_client.api_call(
            "chat.postMessage",
            channel=channel,
            text=default_response
        )
    

if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("GETSCORE connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            if YFS.token_is_expired():
                YFS.renew_token()
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
            # Renewing Token
            
    else:
        print("Connection failed. Exception traceback printed above.")