import time
from io import BytesIO

import feedparser
import tweepy
from credentials import *
from html2image import Html2Image
from PIL import Image

class OrdBot:
  def __init__(self, client, feed, hti):
    self.client = client
    self.feed = feed
    self.hti = hti

  def get_last_tweeted_inscription(self):
    (data, _, _, _) = self.client.get_home_timeline(
      max_results=1, user_auth=True
    )
    current = int(str(data[0]).split()[1])

    return current

  def get_new_inscriptions(self):
    entries = feedparser.parse(self.feed).entries
    latest = int(entries[0]["title"].split()[1])
    offset = (latest - self.get_last_tweeted_inscription()) % len(entries)
    new = entries[:offset]
    new.reverse()

    self.hti.size = (500, 800)
    screenshot = self.hti.screenshot(url=new[0].link)
    image = Image.open(screenshot[0])
    cropped = image.crop((0, 600, 1000, 1345))
    cropped.save("cropped.png")

    return new

  def run(self):
    print("running ord_bot...")
    while True:
      for entry in self.get_new_inscriptions():
        content = "{}\n{}\n".format(entry.title, entry.link)
        print(content)
        response = self.client.create_tweet(text=content)
        print(response + "\n")
        time.sleep(10)

      time.sleep(10)

def main():
  client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
  )
  hti = Html2Image()
  bot = OrdBot(client, "https://ordinals.com/feed.xml", hti)
  bot.run()

if __name__ == "__main__":
  main()
