#!/usr/bin/env python
# vim:fileencoding=utf-8

from calibre.web.feeds.news import BasicNewsRecipe


class LiveScience(BasicNewsRecipe):
    title = "Live Science"
    description = "For the science geek in everyone! Stories on the latest findings from science journals and institutions. Sourced from livescience.com"
    __author__ = 'yodha8'
    language = 'en'
    oldest_article = 7
    max_articles_per_feed = 100
    auto_cleanup = True

    feeds = [
        ('Live Science All Articles', 'https://www.livescience.com/feeds/all'),
    ]


calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'