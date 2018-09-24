# Getscore-gios
Slack Bot for Yahoo Fantasy Football; Team GIOS FF

## Commands
   - `@getscore getscore`: returns the scores for all match ups in league for current week
   - `@getscore getpredictions`: returns the predicted scores for all match ups in league for current week

## Dependenies
  - rauth
  - slackclient

## Credentials file
  Client ID (Consumer Key) and Client Secret (Consumer Secret) from [Yahoo Developer Network](https://developer.yahoo.com/fantasysports/guide/) required.
  
  1. Follow the steps for [Registering Your Application](https://developer.yahoo.com/fantasysports/guide/#registering-your-application) to get your key/secret pair.
  2. Create your creds file: `cp ./credentials.json.example ./credentials.json`
  3. Replace the placeholders with your API keys from Yahoo.
  
## Planned Development
  - Alerts for major plays / score lead changes
  - NFL red zone integration
  - get roster for specified team
  - Update documentation / docstrings 
  
## The Dream Team
  - Carlos 
  - Hope
  - Schuyler
  - David
  - Tho (kinda)
