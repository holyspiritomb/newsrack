import re
import os
import sys
from calibre.web.feeds.news import BasicNewsRecipe
from calibre.web.feeds import Feed
from calibre.ebooks.BeautifulSoup import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title
# from calibre.utils.date import utcnow, parse_date
# from calibre.web.feeds import Feed

# convenience switches for when I'm developing
if "runner" in os.environ["recipes_includes"]:
    _masthead = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos/newvoices-logo.png"
else:
    _masthead = "file:///home/spiritomb/git/newsrack/recipes_custom/logos/newvoices-logo.png"


_name = "New Voices"


class NewVoices(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    language = 'en'
    description = u'Published since 1991 by the independent non-profit Jewish Student Press Service, New Voices is the only Jewish and justice-focused magazine by and for college students. https://newvoices.org'
    __author__ = 'holyspiritomb'
    category = 'news, rss'
    oldest_article = 31
    max_articles_per_feed = 50
    remove_empty_feeds = True
    resolve_internal_links = False
    use_embedded_content = True
    # scale_news_images_to_device = True
    masthead_url = _masthead
    # test = True

    feeds = [("All", "https://newvoices.org/feed/")]
