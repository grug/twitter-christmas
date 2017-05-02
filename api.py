import ConfigParser
import requests
import json
from requests_oauthlib import OAuth1

class API:
    def __init__(self):
        settings = ConfigParser.ConfigParser()
        settings.read("config")
        consumer_key = settings.get("Twitter", "ConsumerKey")
        consumer_secret = settings.get("Twitter", "ConsumerSecret")
        access_token_key = settings.get("Twitter", "AccessTokenKey")
        access_token_secret = settings.get("Twitter", "AccessTokenSecret")
        self.auth = OAuth1(consumer_key, consumer_secret, access_token_key, access_token_secret)
    
    """
    GET search/tweets.
    """
    def searchTweets(self, options):
        url = "https://api.twitter.com/1.1/search/tweets.json"

        r = requests.get(url, params=options, auth=self.auth)
         
        if r.status_code != 200:
            print("[SearchTweets] Error: status code %s received" % r.status_code)
            print("Params: ", options)
            print("Response: ", r.text)

        return json.loads(r.text)

    """
    POST statuses/retweet/:id
    """
    def retweet(self, options):
        url = "https://api.twitter.com/1.1/statuses/retweet/%s.json" % options["id"]
        
        r = requests.post(url, auth=self.auth)

        if r.status_code != 200:
            print("[Retweet] Error: status code %s received" % r.status_code)
            print("Url: ", url)
            print("Retweet id: ", options["id"])
            print("Response: ", r.text)

        return json.loads(r.text)
    
    """
    POST friendships/create
    """
    def follow(self, options):
        url = "https://api.twitter.com/1.1/friendships/create.json"

        r = requests.post(url, params=options, auth=self.auth)

        print("Followed user %s" % options["screen_name"])

        if r.status_code != 200:
            print("[Follow] Error: status code %s received" % r.status_code)
            print("Params: ", options)
            print("Response: ", r.text)

        return json.loads(r.text)

    """
    POST favorites/create
    """
    def favourite(self, options):
        url = "https://api.twitter.com/1.1/favorites/create.json"

        r = requests.post(url, params=options, auth=self.auth)
        
        print("Favourited tweet #%s" % options["id"])

        if r.status_code != 200:
            print("[Favourite] Error: status code %s received" % r.status_code)
            print("Params: ", options)
            print("Response: ", r.text)

        return json.loads(r.text)
