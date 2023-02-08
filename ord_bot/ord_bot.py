import time

import feedparser
import tweepy
from credentials import *
from selenium import webdriver

class OrdBot:
  def __init__(self, client, feed):
    self.client = client
    self.feed = feed

    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--hide-scrollbars')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36');
    self.webdriver = webdriver.Chrome(options=options)

  def last_tweeted_inscription(self):
    last_tweet = self.client.home_timeline(count=1)[0]
    current = int(str(last_tweet.text).split()[1])

    return current

  def load_inscriptions(self):
    entries = feedparser.parse(self.feed).entries
    latest = int(entries[0]["title"].split()[1])
    offset = (latest - self.last_tweeted_inscription()) % len(entries)
    new = entries[:offset]
    new.reverse()

    return new

  def take_screenshot(self, inscription):
    protocol, rest = inscription.link.split("://")
    host, path = rest.split("/", 1)
    path_components = path.split("/")
    path_components[0] = "preview"
    preview_link = protocol + "://" + host + "/" + "/".join(path_components)
    self.webdriver.get(preview_link)
    time.sleep(3)
    self.webdriver.save_screenshot("screenshot.png")

  def group_inscriptions(self, n):
      
    group = self.load_inscriptions()[:min(n, le)]:
        


  def run(self):
    while True:
      for inscription in self.load_inscriptions():
        self.take_screenshot(inscription)
        status = "{}\n{}\n".format(inscription.title, inscription.link)
        media = self.client.media_upload(filename="screenshot.png")
        self.client.update_status(status, media_ids=[media.media_id])
        time.sleep(1)

      time.sleep(180)

def main():
  print("running ord_bot...")
  auth = tweepy.OAuth1UserHandler(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
  )
  client = tweepy.API(auth)
  bot = OrdBot(client, "https://ordinals.com/feed.xml")
  bot.run()

if __name__ == "__main__":
  main()
