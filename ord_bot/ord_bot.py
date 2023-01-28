import time

import feedparser
import tweepy
from credentials import *

class OrdBot:
  def __init__(self, client, feed):
    self.client = client
    self.feed = feed

  def get_last_tweeted_inscription(self):
    (data, _, _, _) = self.client.get_home_timeline(
      max_results=1, user_auth=True
    )
    current = int(str(data[0]).split()[1])

    return current

  def get_new_inscriptions(self):
    entries = feedparser.parse(self.feed).entries
    latest = int(entries[0]["title"].split()[1])
    

    return entries


  def run(self):
    print("running ord_bot...")
    while True:
      entries = self.get_new_inscriptions()
      current = self.get_last_tweeted_inscription()
      latest = self.get_latest_inscription()
      print("latest: {}\nnext: {}".format(latest, current))

      offset = len(entries) - latest + current

      for i in range(offset, len(entries)):
        content = "{}\n{}\n".format(entries[i].title, entries.link)
        print(content)
        # response = self.client.create_tweet(text=content)
        # print(response)
        time.sleep(10)

      current = latest + 1
      time.sleep(10)

def main():
  client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
  )

  bot = OrdBot(client, "https://ordinals.com/feed.xml")
  bot.run()

if __name__ == "__main__":
  main()
