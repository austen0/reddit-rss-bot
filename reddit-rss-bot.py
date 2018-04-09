#!/usr/bin/env python

import config
import feedparser
import praw
import time


class Reddit(object):

  def __init__(self):
    self.reddit = praw.Reddit(
      client_id=config.REDDIT_CLIENT_ID,
      client_secret=config.REDDIT_CLIENT_SECRET,
      username=config.REDDIT_USERNAME,
      password=config.REDDIT_PASSWORD,
      user_agent='RSS to reddit post script'
    )

  def submit(self, sub, entries):
    subreddit = self.reddit.subreddit(sub)
    for title, url in entries.iteritems():
      try:
        subreddit.submit(
          title,
          url=url,
          resubmit=False,
          send_replies=False
        )
      except praw.exceptions.APIException:
        pass


def getFeedEntries(url):
  entries = dict()
  feed = feedparser.parse(url)
  for item in feed.entries:
    entries[item.title] = item.link
  return entries


def main():
  reddit = Reddit()

  while True:
    for subreddit, feed_url in config.FEEDS.iteritems():
      entries = getFeedEntries(feed_url)
      reddit.submit(subreddit, entries)

    time.sleep(config.RUN_FREQUENCY_MINS * 60)


if __name__ == '__main__':
  main()
