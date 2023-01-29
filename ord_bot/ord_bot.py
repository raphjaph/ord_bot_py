import time

import feedparser
import tweepy
from credentials import *
from PIL import Image
from selenium import webdriver

class OrdBot:
  def __init__(self, client, webdriver, feed):
    self.client = client
    self.feed = feed
    self.webdriver = webdriver

  def get_last_tweeted_inscription(self):
    last_tweet = self.client.home_timeline(count=1)[0]
    current = int(str(last_tweet.text).split()[1])

    return current

  def get_new_inscriptions(self):
    entries = feedparser.parse(self.feed).entries
    latest = int(entries[0]["title"].split()[1])
    offset = (latest - self.get_last_tweeted_inscription()) % len(entries)
    new = entries[:offset]
    new.reverse()

    return new

  def get_screenshot(self, inscription):
    screenshot = self.webdriver.get(inscription.link
                                    ).save_screenshot("screenshot.png")
    image = Image.open(screenshot[0])
    cropped = image.crop((0, 600, 1000, 1345))
    cropped.save("cropped.png")

    return "cropped.png"

  def run(self):
    print("running ord_bot...")
    while True:
      for inscription in self.get_new_inscriptions():
        status = "{}\n{}\n".format(inscription.title, inscription.link)
        print("Status: {}".format(status))
        # media = self.client.media_upload(
          # filename=self.get_screenshot(inscription)
        # )
        # response = self.client.update_status(status, media_ids=[media.media_id])
        # print(response + "\n\n")
        time.sleep(10)

      time.sleep(10)

def main():
  auth = tweepy.OAuth1UserHandler(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
  )
  client = tweepy.API(auth)
  driver = webdriver.Chrome()
  bot = OrdBot(client, driver, "https://ordinals.com/feed.xml")
  bot.run()

if __name__ == "__main__":
  main()
