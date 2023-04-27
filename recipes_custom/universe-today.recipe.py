import os
import sys
# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title

_name = "Universe Today"


class UniverseToday(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    language = 'en'
    description = u'Space and astronomy news. https://www.universetoday.com/feed/'
    __author__ = 'seird'
    publisher = u'universetoday.com'
    category = 'science, astronomy, news, rss'
    oldest_article = 7
    max_articles_per_feed = 40
    auto_cleanup = True
    no_stylesheets = True
    use_embedded_content = False
    remove_empty_feeds = True

    # feeds = [(u'Universe Today', u'http://feeds.feedburner.com/universetoday/pYdq')]
    feeds = [("Universe Today", "https://www.universetoday.com/feed/")]

    def populate_article_metadata(self, article, __, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
