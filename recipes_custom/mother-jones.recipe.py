#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import unicode_literals, division, absolute_import, print_function
import sys
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


class MotherJones(BasicNewsRecipe, BasicNewsrackRecipe):
    title          = 'Mother Jones'
    language = 'en'
    __author__ = 'holyspiritomb'
    oldest_article = 14
    max_articles_per_feed = 200
    no_stylesheets = True
    feeds          = [
        ('Mother Jones', 'http://feeds.feedburner.com/motherjones/feed'),
    ]
    timefmt = ' [%b %d, %Y]'

    # soup = self.index_to_soup('https://www.motherjones.com/magazine')
    # coverdiv = soup.find('div', attrs={'id': 'toc_cover'})
    # cov_url = coverdiv.find('img', src=True)['src']
    # self.cover_url = 'https://www.motherjones.com' + cov_url




calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
