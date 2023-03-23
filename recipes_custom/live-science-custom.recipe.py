#!/usr/bin/env python
# vim:fileencoding=utf-8

import os
import sys
from datetime import datetime, timezone

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
try:
    from recipes_shared import BasicNewsrackRecipe, format_title
except ImportError:
    # just for Pycharm to pick up for auto-complete
    from includes.recipes_shared import BasicNewsrackRecipe, format_title

from calibre.web.feeds.news import BasicNewsRecipe


_name = "Live Science"


class LiveScience(BasicNewsRecipe, BasicNewsrackRecipe):
    title = _name
    description = "Live Science is a science news website that publishes stories in a wide variety of topics such as Space, Animals, Health, Archaeology, Human behavior and Planet Earth. Sourced from https://www.livescience.com/feeds/all"
    __author__ = 'yodha8'
    language = 'en'
    oldest_article = 7
    max_articles_per_feed = 100
    auto_cleanup = True

    conversion_options = {
        'tags' : 'Science, News, Live Science, Periodical',
    }
    feeds = [
        ('Live Science All Articles', 'https://www.livescience.com/feeds/all'),
    ]

    def populate_article_metadata(self, article, __, _):

        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            # self.title = format_title(_name, article.utctime)


calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
