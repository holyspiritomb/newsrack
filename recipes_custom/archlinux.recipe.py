#!/usr/bin/env python
# vim:fileencoding=utf-8
import os
import sys
# from datetime import timedelta, timezone

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title
# from calibre.web.feeds import Feed
from calibre.web.feeds.news import BasicNewsRecipe

_name = "Arch Linux"


class ArchLinux(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    oldest_article = 120
    max_articles_per_feed = 100
    auto_cleanup = True
    description = "Arch Linux updates and news."
    masthead_url = "https://archlinux.org/static/logos/archlinux-logo-dark-90dpi.ebdee92a15b3.png"
    conversion_options = {
        'tags': 'Arch Linux',
        'authors': 'newsrack',
    }

    feeds = [
        ("Arch Linux News", "https://archlinux.org/feeds/news/"),
    ]

    def populate_article_metadata(self, article, __, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
            # article.title = format_title(article.title, article.utctime)
