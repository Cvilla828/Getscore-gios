import json
import webbrowser
from rauth import OAuth2Service
import os
import time


class FantasyGios(object):
    def __init__(self, credentials):
        # load credentials
        file_path = os.path.join(os.getcwd(), credentials)
        if not os.path.exists(file_path):
            raise FileNotFoundError(
                "credentials file does not exist at: {}".format(file_path)
            )

        self.credentials_file = open(credentials)
        self.credentials = json.load(self.credentials_file)
        self.credentials_file.close()

        self.service = OAuth2Service(
            name='example',
            client_id=self.credentials["client_id"],
            client_secret=self.credentials["client_secret"],
            access_token_url='https://api.login.yahoo.com/oauth2/get_token',
            authorize_url='https://api.login.yahoo.com/oauth2/request_auth',
            base_url='http://fantasysports.yahooapis.com/')
        self.baseURI = "https://fantasysports.yahooapis.com/fantasy/v2/leagues;league_keys=nfl.l.159366"
        # the return URL is used to validate the request
        params = {'redirect_uri': 'oob',
                  'response_type': 'code'}
        url = self.service.get_authorize_url(**params)
        webbrowser.open(url)
        verify = input('Enter code: ')
        # once the above URL is consumed by a client we can ask for an access
        # token. note that the code is retrieved from the redirect URL above,
        # as set by the provider

        data = {
            'client_id': self.credentials["client_id"],
            'client_secret': self.credentials["client_secret"],
            'code': verify,
            'grant_type': 'authorization_code',
            'redirect_uri': 'oob'}
        
        self.session = self.service.get_auth_session(data=data, decoder=json.loads)
        
        # Getting the refresh_toekn so when the token expires it renews it self.
        self.credentials['access_token'] = self.service.access_token_response.json()['access_token']
        self.credentials['xoauth_yahoo_guid'] = self.service.access_token_response.json()['xoauth_yahoo_guid']
        self.credentials['refresh_token'] = self.service.access_token_response.json()['refresh_token']
        self.credentials['expire_at'] = time.time() + 3600

        r = self.session.get(url, params={'format': 'json'})
        #dict for teams
        self.team_id = {}
        self.get_team_id()
        print(r.status_code)
    
    # checks to see if token is expired
    def token_is_expired(self):
        if time.time() >= (self.credentials['expire_at'] - 1):
            return True
        else:
            return False
    
    def renew_token(self):
        data = {
            'client_id': self.credentials["client_id"],
            'client_secret': self.credentials["client_secret"],
            'grant_type': 'refresh_token',
            'redirect_uri': 'oob',
            'refresh_token' : self.credentials['refresh_token']}
        self.session = self.service.get_access_token(data=data, decoder=json.loads)
        
        # Update Credential dict
        self.credentials['access_token'] = self.service.access_token_response.json()['access_token']
        self.credentials['expire_at'] = time.time() + 3600
        self.session = self.service.get_auth_session(data=data, decoder=json.loads)
        
        

    def get_standings(self):
        # new_url = 'https://fantasysports.yahooapis.com/fantasy/v2/leagues;league_keys=nfl.l.159366/standings'
        s = self.session.get(self.baseURI + '/standings', params={'format': 'json'})
        return s
        # print s.status_code
        # print s.json()

    def get_score(self):
        s = self.session.get(self.baseURI + '/scoreboard', params={'format': 'json'})
        return s
    
    def get_teams(self):
        # new_url = 'https://fantasysports.yahooapis.com/fantasy/v2/leagues;league_keys=nfl.l.159366/standings'
        s = self.session.get(self.baseURI + '/players', params={'format': 'json'})
        return s

    #gets team and team id
    def get_team_id(self):
        s = self.session.get(self.baseURI + '/teams', params={'format': 'json'})
        temp = s.json()
        size = s.json()['fantasy_content']['leagues']['0']['league'][1]['teams']['count']
        for i in range(0,size):
            self.team_id[temp['fantasy_content']['leagues']['0']['league'][1]['teams'][str(i)]['team'][0][2]['name']] = temp['fantasy_content']['leagues']['0']['league'][1]['teams'][str(i)]['team'][0][0]['team_key']
        # print(self.team_id)
        
    def get_team_roster(self, name):
        s = self.session.get('https://fantasysports.yahooapis.com/fantasy/v2/' + 'teams;team_keys='+ self.team_id[name]  + '/players', params={'format': 'json'})
        return s
