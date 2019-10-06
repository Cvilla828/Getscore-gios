# Getscore-gios
Slack Bot for Yahoo Fantasy Football; Team GIOS FF

## Commands
   - `@getscore getscore`: returns the scores for all match ups in league for current week
   - `@getscore getnflscores`: returns all nfl teams' match-ups, scores, and status
   - `@getscore getnflscores [team name]`: returns specified nfl team's match-ups, scores, and status
   - `@getscore getstandings`: returns the standings for the league
   - `@getscore getrost [fantasy team name]`: returns the roster with play status for each player of requested team
   - `@getscore getpastnflplays`: returns the recent scoring plays
   - `@getscore getpastnflplays [team name]`: returns this weeks scoring plays for that team's game

## Dependenies
  - rauth
  - slackclient
  - xmltodict

## Credentials file
  Client ID (Consumer Key) and Client Secret (Consumer Secret) from [Yahoo Developer Network](https://developer.yahoo.com/fantasysports/guide/) required.
  
  1. Follow the steps for [Registering Your Application](https://developer.yahoo.com/fantasysports/guide/#registering-your-application) to get your key/secret pair.
  2. Create your creds file: `cp ./credentials.json.example ./credentials.json`
  3. Replace the placeholders with your API keys from Yahoo.

  ## Setting up pyenv
  1. `python3 -m venv env`
  2. `source env/bin/activate`
  3. `pip install -r requirements.txt`
  
## Planned Development
  - Alerts for major plays / score lead changes
  - NFL red zone integration
  - Update documentation / docstrings 
  
## The Dream Team
  - Carlos 
  - Hope
  - Schuyler
  - David
  - Tho (debatable)
