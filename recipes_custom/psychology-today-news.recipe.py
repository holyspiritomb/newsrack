#!/usr/bin/env python
# vim:fileencoding=utf-8

import os
import re
import sys
from calibre import browser
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title
from calibre.web.feeds.news import BasicNewsRecipe
from calibre.ebooks.BeautifulSoup import BeautifulSoup


def absurl(url):
    if url.startswith("//"):
        return "https:" + url
    if url.startswith("/"):
        return "https://www.psychologytoday.com" + url
    return url


def classes(classes):
    q = frozenset(classes.split(' '))
    return dict(attrs={
        'class': lambda x: x and frozenset(x.split()).intersection(q)})


_name = 'Psychology Today Daily'


class PsychologyTodayDaily(BasicNewsrackRecipe, BasicNewsRecipe):

    title = _name
    __author__ = 'Kovid Goyal'

    description = ('This magazine takes information from the latest research'
                   ' in the field of psychology and makes it useful to people in their everyday'
                   ' lives. Its coverage encompasses self-improvement, relationships, the mind-body'
                   ' connection, health, family, the workplace and culture.')
    language = 'en'
    no_stylesheets = True
    publication_type = 'newspaper'
    masthead_url = "https://i.imgur.com/QW9Evsi.png"
    delay = 1

    keep_only_tags = [dict(attrs={'id': 'block-pt-content'})]
    remove_tags = [classes('pt-social-media')]

    feeds = [
        ("News", "https://www.psychologytoday.com/us/news/feed")
    ]

    def get_browser(self, *args, **kwargs):
        return self

    def clone_browser(self, *args, **kwargs):
        return self.get_browser()

    def open_novisit(self, *args, **kwargs):
        br = browser()
        return br.open_novisit(*args, **kwargs)

    open = open_novisit


calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
