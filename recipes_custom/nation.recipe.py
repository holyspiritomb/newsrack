__license__ = 'GPL v3'
__copyright__ = '2008 - 2011, Darko Miletic <darko.miletic at gmail.com>'
'''
thenation.com
'''
import os
import re
import sys
from collections import OrderedDict
from datetime import datetime, timezone

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
try:
    from recipes_shared import BasicNewsrackRecipe, WordPressNewsrackRecipe, format_title
except ImportError:
    # just for Pycharm to pick up for auto-complete
    from includes.recipes_shared import BasicNewsrackRecipe, WordpressNewsrackRecipe, format_title

from calibre.web.feeds.news import BasicNewsRecipe

_name = 'The Nation'


def classes(classes):
    q = frozenset(classes.split(' '))
    return dict(attrs={
        'class': lambda x: x and frozenset(x.split()).intersection(q)})


class Thenation(BasicNewsRecipe, BasicNewsrackRecipe):
    title = _name
    __author__ = 'Darko Miletic, holyspiritomb'
    description = 'Unconventional Wisdom Since 1865 http://www.thenation.com/'
    publisher = 'The Nation'
    category = 'news, politics, USA'
    oldest_article = 120
    encoding = 'utf-8'
    max_articles_per_feed = 100
    no_stylesheets = True
    language = 'en'
    use_embedded_content = False
    delay = 1
    login_url = 'http://www.thenation.com/user?destination=%3Cfront%3E'
    publication_type = 'magazine'
    needs_subscription = 'optional'
    extra_css              = """
                              body{font-family: Lato, Roboto, Arial,Helvetica,sans-serif;}
                              .print-created{font-size: small;}
                              .caption{display: block; font-size: x-small;}
                            """

    conversion_options = {
        'comment': description,
        'tags': 'Politics, The Nation, Periodical',
        'authors': 'newsrack',
        'publisher': publisher,
        'language': language
    }

    keep_only_tags = [
        classes('title subtitle byline article-body-inner'),
    ]
    remove_tags = [
        dict(name=['link', 'iframe', 'base', 'meta', 'object', 'embed', 'script']),
        classes('email-signup-module current-issue related-newarticle related-multi series-modules'),
    ]
    remove_attributes = ['lang']

    feeds = [(u"Articles", u'http://www.thenation.com/rss/articles')]

    def get_browser(self):
        br = BasicNewsRecipe.get_browser(self)
        br.open('http://www.thenation.com/')
        if self.username is not None and self.password is not None:
            br.open(self.login_url)
            br.select_form(nr=1)
            br['name'] = self.username
            br['pass'] = self.password
            br.submit()
        return br

    def populate_article_metadata(self, article, __, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)

    def get_cover_url(self):
        soup = self.index_to_soup('http://www.thenation.com/issue/')
        div = soup.find('div', **classes("issue__img"))
        if div:
            self.cover_url = (
                div.find('img')["src"]
                .split()[0]
            )
        return getattr(self, "cover_url", self.cover_url)
