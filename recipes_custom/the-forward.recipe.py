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


_name = "The Forward"


class TheForward(BasicNewsRecipe, BasicNewsrackRecipe):
    title = _name
    __author__ = 'holyspiritomb'
    description = '''The Forward is an American news media organization for a Jewish American audience. The Forward's perspective on world and national news and its reporting on the Jewish perspective on modern United States have made it one of the most influential American Jewish publications. It is published by an independent nonprofit association. It has a politically progressive editorial focus.'''
    masthead_url = "https://forward.com/wp-content/themes/studio-simpatico/svgs/logo.svg"
    language = "en"
    encoding = "utf-8"
    oldest_article = 7
    max_articles_per_feed = 50
    auto_cleanup = True
    publication_type = 'newspaper'
    scale_news_images = (800, 1200)
    conversion_options = {
        'tags': 'Jewish'
    }

    feeds = [
        ('The Forward - News', 'https://forward.com/news/feed/'),
        ('The Forward - Opinions', 'https://forward.com/opinion/feed/'),
        ('The Forward - Culture', 'https://forward.com/culture/feed/'),
    ]
