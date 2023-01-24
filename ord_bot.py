import tweepy
import feedparser
import time
from credentials import * 

client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

(data, _, _, _) = client.get_home_timeline(max_results=1, user_auth=True)
next = int(str(data[0]).split()[1]) + 1

while True:
    entries = feedparser.parse("https://ordinals.com/feed.xml").entries
     
    latest = int(entries[0]["title"].split()[1])
    
    for i in range(latest - next, next, -1):
        entry = entries[i]
        content = entry.title + "\n" + entry.link + "\n"
        print(content)
        response = client.create_tweet(text=content)
        print(response)
        time.sleep(10)
    
    next = latest + 1
    time.sleep(10)
