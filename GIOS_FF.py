import json
import time
import webbrowser
import pandas as pd
from pandas.io.json import json_normalize
from rauth import OAuth2Service
from rauth.utils import parse_utf8_qsl

class GIOS_FF():
    def __init__(self, credentials):
        # load credentials
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
        print (r.status_code)

    def get_standings(self, sess):
        new_url = 'https://fantasysports.yahooapis.com/fantasy/v2/leagues;league_keys=nfl.l.159366/standings'
        s = sess.get(new_url, params={'format': 'json'})
        return s
        # print s.status_code
        # print s.json()


cred_file = input("Please enter the location of credentials json file: ")
test = GIOS_FF(cred_file)

response = test.get_standings(test.session)
print (json.dumps(response.json(), indent=4, sort_keys=True))

