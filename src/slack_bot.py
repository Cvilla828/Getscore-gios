
import os
import time
import re
from slackclient import SlackClient
from fantasy_gios import FantasyGios
from yahoo_parser import *
import json

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


def parse_bot_commands(slack_events):
    """
        Parses a list of events coming from the Slack RTM API to find bot commands.
        If a bot command is found, this function returns a tuple of command and channel.
        If its not found, then this function returns None, None.
    """
    for event in slack_events:
        if event["type"] == "message" and not "subtype" in event:
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
    # Default response is help text for the user
    default_response = "Not sure what you mean. Try *{}*.".format(EXAMPLE_COMMAND + " or getpredictions")

    # Finds and executes the given command, filling in response
    response = None
    message =''
    # This is where you start to implement more commands!
    if command.startswith(EXAMPLE_COMMAND):
        response =  parse_scores(YFS.get_score(YFS.session).json())
        for i in response:
            text = "%s - %s vs %s - %s\n" %(i["name_team_1"],i["score_team_1"], i["score_team_2"], i["name_team_2"])
            message = message + text
    if command.startswith("getpredictions"):
        response =  parse_scores(YFS.get_score(YFS.session).json())
        for i in response:
            text = "%s - %s vs %s - %s\n" %(i["name_team_1"],i["pred_team_1"], i["pred_team_2"], i["name_team_2"])
            message = message + text
    if message is not '':
        response = "```" + message + "```"
    # Sends the response back to the channel
    slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=response or default_response
    )


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        while True:
            if YFS.token_is_expired():
                YFS.renew_token(YFS.session)
            command, channel = parse_bot_commands(slack_client.rtm_read())
            if command:
                handle_command(command, channel)
            time.sleep(RTM_READ_DELAY)
            # Renewing Token
            
    else:
        print("Connection failed. Exception traceback printed above.")