import re
import os
import sys
from calibre.web.feeds.news import BasicNewsRecipe
from calibre.web.feeds import Feed
from calibre.ebooks.BeautifulSoup import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.append(os.environ["recipes_includes"])
from recipes_shared import WordPressNewsrackRecipe, format_title
# from calibre.utils.date import utcnow, parse_date

# convenience switches for when I'm developing
if "runner" in os.environ["recipes_includes"]:
    _masthead_prefix = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos"
else:
    _masthead_prefix = f"file://{os.environ['HOME']}/git/newsrack/recipes_custom/logos"
_masthead = f"{_masthead_prefix}/lilith-masthead.svg"

_name = "Lilith"


class Lilith(WordPressNewsrackRecipe, BasicNewsRecipe):
    title = _name
    language = 'en'
    description = u'Jewish feminist magazine. https://lilith.org'
    __author__ = 'holyspiritomb'
    category = 'news, rss'
    oldest_article = 31
    max_articles_per_feed = 50
    remove_empty_feeds = True
    resolve_internal_links = False
    # use_embedded_content = True
    # scale_news_images_to_device = True
    masthead_url = _masthead
    # test = True

    feeds = [("All", "https://lilith.org/feed/")]
    feed_url = "https://lilith.org/feed/"

    # def parse_feeds(self):
    #     feeds = self.get_posts(feed_url,oldest_article)
    #     # self.log.warn(feeds)
    #     for feed in feeds:
    #         self.log.warn(feed)
    #         for article in feed.articles[:]:
    #             self.log(article)
    #     return feeds
