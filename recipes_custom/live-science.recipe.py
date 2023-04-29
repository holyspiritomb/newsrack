#!/usr/bin/env python
# vim:fileencoding=utf-8

import os
import sys

from calibre import browser
from datetime import datetime, timezone
from calibre.ebooks.BeautifulSoup import BeautifulSoup
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
    oldest_article = 6
    max_articles_per_feed = 100
    no_stylesheets = True
    no_javascript = True
    auto_cleanup = False
    use_embedded_content = False

    conversion_options = {
        'tags' : 'Science, News, Live Science, Periodical',
    }
    feeds = [
        ('Live Science All Articles', 'https://www.livescience.com/feeds/all'),
    ]
    keep_only_tags = [
        dict(attrs={"id": "hero"}),
        dict(attrs={"class": "hero-image-wrapper"}),
        dict(attrs={"id": "article-body"}),
    ]
    remove_tags_before = [
        dict(name="div", class_="news-article")
    ]
    remove_tags = [
        dict(name="div", class_="ad-unit"),
        dict(name="nav", class_="socialite-widget"),
        dict(name="div", class_="fancy-box"),
    ]
    remove_attributes = [
        "style"
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

    def get_browser(self, *a, **kw):
        kw[
            "user_agent"
        ] = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        br = BasicNewsRecipe.get_browser(self, *a, **kw)
        return br

    def clone_browser(self, *args, **kwargs):
        return self.get_browser()

    def open_novisit(self, *args, **kwargs):
        br = browser()
        return br.open_novisit(*args, **kwargs)

    open = open_novisit


calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
