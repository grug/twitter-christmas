import time
import threading
import ConfigParser
from blacklist import blacklist
from api import API

twitter = API()

# Config settings.
settings = ConfigParser.ConfigParser()
settings.read("config")

last_id = settings.get("Tweets", "lastid") 

# List of posts to analyse.
post_list = list()

def checkForFollow(post):
    if "follow" in post["text"].lower():
        try:
            twitter.follow({"scren_name": post["retweeted_status"]["user"]["screen_name"]})
        except:
            twitter.follow({"screen_name": post["user"]["screen_name"]})

def checkForFavourite(post):
        if "favourite" in post["text"].lower() or "favorite" in post["text"].lower() or "fav" in post["text"].lower():
            try:
                twitter.favourite({"id": post["retweeted_status"]["user"]["id"]})
            except:
                twitter.favourite({"id": post["id"]})

def enterCompetitions():
    t = threading.Timer(15.0, enterCompetitions).start()

    # If we have any competitions to enter.
    if len(post_list) > 0:
        # Grab oldest post in the list.
        post = post_list[0]
        
        try:
            if post["retweeted_status"]["user"]["screen_name"] in blacklist:
                post_list.pop(0)
                return
        except:
            if post["user"]["screen_name"] in blacklist:
                post_list.pop(0)
                return
        checkForFollow(post)
        checkForFavourite(post)
        twitter.retweet({'id': post["id"]})

        print("Entered: ", post["text"])
        post_list.pop(0)


def findCompetitions():
    t = threading.Timer(10.0, findCompetitions).start()
    
    global last_id

    options = {
        "q": "retweet to win -signup -vote -bot -filter:retweets OR RT to win -signup -vote -bot -filter:retweets",
        "result_type": "mixed",
        "since_id": last_id,
        "count": 100
    }
    tweets = twitter.searchTweets(options)
    
    entered = 0

    print "Currently %s tweets in queue" % str(len(post_list))

    for tweet in tweets["statuses"]:
        # Don't retweet stuff that is a retweet.
        if not tweet["retweeted"]:
            # Let's not be the first to retweet this.
            if tweet["retweet_count"] > 0:
                # Make sure this is more recent than the last thing we entered.
                if tweet["id"] > last_id:
                    last_id = tweet["id"]
                    with open('config', 'w') as f:
                        settings.set("Tweets", "lastid", last_id)
                        settings.write(f)
                        f.close()
                exists = False 
                # We don't want to add doubles.
                for t in post_list:
                    if t["id"] == tweet["id"]:
                        exists = True
                if not exists:
                    post_list.append(tweet)
                    print("Adding tweet %s to queue" % tweet["id"]) 
                    entered += 1


def main():
    print "Starting Twitter Christmas bot..."
    # Search for competitions to enter.
    findCompetitions()
    # Go through our list of competitions and enter them.
    enterCompetitions()
    while (True):
        time.sleep(1)

if __name__ == "__main__":
    main()
