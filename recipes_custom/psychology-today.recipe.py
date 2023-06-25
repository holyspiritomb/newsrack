#!/usr/bin/env python
# vim:fileencoding=utf-8

import os
import re
import sys
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


_name = 'Psychology Today'


class PsychologyToday(BasicNewsrackRecipe, BasicNewsRecipe):

    title = _name
    __author__ = 'Kovid Goyal'

    description = ('This magazine takes information from the latest research'
                   ' in the field of psychology and makes it useful to people in their everyday'
                   ' lives. Its coverage encompasses self-improvement, relationships, the mind-body'
                   ' connection, health, family, the workplace and culture.')
    language = 'en'
    encoding = 'UTF-8'
    no_stylesheets = True
    publication_type = 'magazine'
    masthead_url = "https://raw.githubusercontent.com/holyspiritomb/newsrack/spiritomb/recipes_custom/logos/psych.svg"

    keep_only_tags = [dict(attrs={'id': 'block-pt-content'})]
    remove_tags = [classes('pt-social-media')]

    def parse_index(self):
        presoup = self.index_to_soup('https://www.psychologytoday.com/us/magazine/archive')
        a_div = presoup.find("div", class_='magazine-thumbnail')
        a = a_div.find("a")
        # self.timefmt = ' [%s]' % a['title']
        self.title = f"{_name}: {a['title']}"
        self.cover_url = absurl(a.img['src'])
        soup = self.index_to_soup(absurl(a['href']))
        articles = []
        for article in soup.findAll('div', attrs={'class': 'article-text'}):
            self.log(article)
            title = self.tag_to_string(article.find(class_=['h2', 'h3'])).strip()
            url = absurl(article.find(class_=['h2', 'h3']).a['href'])
            self.log('\n', title, 'at', url)
            desc = self.tag_to_string(article.find('p', class_='description')).strip()
            author = self.tag_to_string(article.find('p', class_='byline').a).strip()
            if desc:
                self.log(desc)
            else:
                desc = ''
            articles.append({'title': title, 'url': url, 'description': desc, 'author': author})
        return [('Current Issue', articles)]
