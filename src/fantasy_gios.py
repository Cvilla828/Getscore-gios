import json
import webbrowser
from rauth import OAuth2Service
import os


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

        r = self.session.get(url, params={'format': 'json'})
        print(r.status_code)

    def get_standings(self, sess):
        # new_url = 'https://fantasysports.yahooapis.com/fantasy/v2/leagues;league_keys=nfl.l.159366/standings'
        s = sess.get(self.baseURI + '/standings', params={'format': 'json'})
        return s
        # print s.status_code
        # print s.json()

    def get_score(self, sess):
        s = sess.get(self.baseURI + '/scoreboard', params={'format': 'json'})
        return s
