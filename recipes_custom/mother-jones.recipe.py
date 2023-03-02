#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import unicode_literals, division, absolute_import, print_function
import sys
import os
from collections import OrderedDict
from datetime import datetime, timezone

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
try:
    from recipes_shared import BasicNewsrackRecipe, WordPressNewsrackRecipe, format_title
except ImportError:
    # just for Pycharm to pick up for auto-complete
    from includes.recipes_shared import BasicNewsrackRecipe, format_title

from calibre.web.feeds.news import BasicNewsRecipe

_name = "Mother Jones"


class MotherJones(BasicNewsRecipe, BasicNewsrackRecipe):
    title = _name
    language = 'en'
    __author__ = 'holyspiritomb'
    description = '''Mother Jones is a nonprofit magazine and news outlet that delivers original award-winning reporting on the urgent issues of our day, from politics and climate change to education and the food we eat. We investigate stories that are in the public's interest. From revelatory scoops to deep-dive investigations, Mother Jones inspires 9 million monthly readers of our print, digital, and online journalism.
    Generated from https://www.motherjones.com/feed
    '''
    oldest_article = 14
    max_articles_per_feed = 200
    no_stylesheets = True
    publication_type = 'magazine'
    scale_news_images = (800, 1200)
    conversion_options = {
        'tags': 'Progressive, Politics, Periodical'
    }
    feeds = [
        ('Mother Jones', 'http://feeds.feedburner.com/motherjones/feed'),
    ]
    timefmt = ' [%b %d, %Y]'

    def populate_article_metadata(self, article, __, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)

    def get_cover_url(self):
        soup = self.index_to_soup('https://www.motherjones.com/magazine')
        coverdiv = soup.find('div', attrs={'id': 'toc_cover'})
        cov_url = coverdiv.find('img', src=True)['src'].split()[0]
        if cov_url:
            self.cover_url = 'https://www.motherjones.com' + cov_url
        return getattr(self, "cover_url", self.cover_url)


calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
