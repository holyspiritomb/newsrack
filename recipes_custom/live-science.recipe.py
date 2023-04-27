#!/usr/bin/env python
# vim:fileencoding=utf-8

import os
import sys
from datetime import datetime, timezone
from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre.utils.date import utcnow, parse_date

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title


_name = "Live Science"


class LiveScience(BasicNewsRecipe, BasicNewsrackRecipe):
    title = _name
    description = "Live Science is a science news website that publishes stories in a wide variety of topics such as Space, Animals, Health, Archaeology, Human behavior and Planet Earth. Sourced from https://www.livescience.com/feeds/all"
    __author__ = 'yodha8'
    language = 'en'
    oldest_article = 7
    max_articles_per_feed = 100
    auto_cleanup = True
    use_embedded_content = False

    conversion_options = {
        'tags' : 'Science, News, Live Science, Periodical',
    }
    feeds = [
        ('Live Science All Articles', 'https://www.livescience.com/feeds/all'),
    ]

    def populate_article_metadata(self, article, __, _):

        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)

    def parse_feeds(self):
        feeds = BasicNewsRecipe.parse_feeds(self)
        for feed in feeds:
            for article in feed.articles[:]:
                # self.log.info(f"article.title is: {article.title}")
                if 'OBESITY' in article.title.upper() or 'WEIGHT LOSS' in article.title.upper():
                    self.log.warn(f"removing {article.title} from feed")
                    feed.articles.remove(article)
        return feeds


calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
