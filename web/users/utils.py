import os
import oauth2
import json
import requests


class TwitterClient:

    def __init__(self):
        self.root_url = 'https://api.twitter.com/1.1'

        self.consumer_key = os.environ['TWITTER_CONSUMER_KEY']
        self.consumer_secret = os.environ['TWITTER_CONSUMER_SECRET']

        self.token_key = os.environ['TWITTER_TOKEN_KEY']
        self.token_secret = os.environ['TWITTER_TOKEN_SECRET']

    def send(self, url_part, method='GET', data=b''):
        url = os.path.join(self.root_url, url_part)

        consumer = oauth2.Consumer(key=self.consumer_key, secret=self.consumer_secret)
        token = oauth2.Token(key=self.token_key, secret=self.token_secret)

        client = oauth2.Client(consumer, token)
        resp, content = client.request(url, method=method, body=data)
        return json.loads(content.decode())


class WatsonClient:

    def __init__(self):
        self.root_url = 'https://gateway.watsonplatform.net/personality-insights/api/v3'

        self.username = os.environ['WATSON_USERNAME']
        self.password = os.environ['WATSON_PASSWORD']

    def send(self, url_part, method='GET', data=None):
        url = os.path.join(self.root_url, url_part)

        response = requests.request(
            method=method,
            auth=(self.username, self.password),
            url=url,
            data=data,
            headers={
                'Content-Type': 'text/plain'
            }
        )
        return json.loads(response.content.decode())
