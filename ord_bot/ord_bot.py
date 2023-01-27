import time

import feedparser
import tweepy
from credentials import *

client = tweepy.Client(
  consumer_key=consumer_key,
  consumer_secret=consumer_secret,
  access_token=access_token,
  access_token_secret=access_token_secret
)

(data, _, _, _) = client.get_home_timeline(max_results=1, user_auth=True)
next_inscription_number = int(str(data[0]).split()[1]) + 1

while True:
  entries = feedparser.parse("https://ordinals.com/feed.xml").entries
  entries.reverse()
  latest_inscription_number = int(entries[-1]["title"].split()[1])

  for i in range(len(entries) - 1 -
                 (latest_inscription_number - next_inscription_number),
                 len(entries)):
    entry = entries[i]
    content = entry.title + "\n" + entry.link + "\n"
    print(content)
    response = client.create_tweet(text=content)
    print(response)
    time.sleep(10)

  next_inscription_number = latest_inscription_number + 1
  time.sleep(10)
