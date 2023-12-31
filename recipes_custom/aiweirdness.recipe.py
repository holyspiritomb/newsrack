import os
import sys

from calibre.web.feeds.news import BasicNewsRecipe, classes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title

_name = 'AI Weirdness'
# convenience switches for when I'm developing
if "runner" in os.environ["recipes_includes"]:
    _masthead_prefix = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos"
else:
    _masthead_prefix = f"file://{os.environ['HOME']}/git/newsrack/recipes_custom/logos"
_masthead = f"{_masthead_prefix}/aiweirdness.png"


class AIWeirdness(BasicNewsrackRecipe, BasicNewsRecipe):

    title = _name
    language = 'en'
    use_embedded_content = True
    recursions = 0
    remove_empty_feeds = True
    masthead_url = _masthead
    description = "AI Weirdness: the strange side of machine learning. https://www.aiweirdness.com/"
    __author__ = 'holyspiritomb'
    no_stylesheets = True
    oldest_article = 31
    feeds = [("Posts", "https://www.aiweirdness.com/rss/")]
    
    def populate_article_metadata(self, article, __, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)

    def parse_feeds(self):
        feeds = BasicNewsRecipe.parse_feeds(self)
        for feed in feeds:
            for article in feed.articles[:]:
                self.log(article)
                if not article.content:
                    self.log.warn(f"removing subscriber-only article {article.title} from feed")
                    feed.articles.remove(article)
        return feeds
