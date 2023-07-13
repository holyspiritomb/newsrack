import os
import re
import sys
from collections import OrderedDict
from datetime import datetime, timezone

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title
from calibre.web.feeds.news import BasicNewsRecipe


_name = "The Forward"


class TheForward(BasicNewsRecipe, BasicNewsrackRecipe):
    title = _name
    __author__ = 'holyspiritomb'
    description = '''The Forward is an American news media organization for a Jewish American audience. The Forward's perspective on world and national news and its reporting on the Jewish perspective on modern United States have made it one of the most influential American Jewish publications. It is published by an independent nonprofit association. It has a politically progressive editorial focus. https://forward.com/'''
    masthead_url = "https://forward.com/wp-content/themes/studio-simpatico/svgs/logo.svg"
    language = "en"
    encoding = "utf-8"
    oldest_article = 3
    max_articles_per_feed = 50
    auto_cleanup = True
    publication_type = 'newspaper'
    scale_news_images = (800, 1200)
    conversion_options = {
        'tags': 'Jewish, The Forward, Periodical, Politics, News',
        'authors' : 'newsrack',
    }

    feeds = [
        ('News', 'https://forward.com/news/feed/'),
        ('Opinions', 'https://forward.com/opinion/feed/'),
        ('Culture', 'https://forward.com/culture/feed/'),
    ]

    def populate_article_metadata(self, article, __, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)


calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
