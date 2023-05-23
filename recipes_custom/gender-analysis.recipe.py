
import os
import sys
from calibre.web.feeds.news import BasicNewsRecipe, classes
from datetime import timezone, timedelta, datetime, time

sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, WordPressNewsrackRecipe, format_title
from calibre.utils.date import utcnow, parse_date
from calibre.web.feeds import Feed

_name = "Gender Analysis"


class GenderAnalysis(WordPressNewsrackRecipe, BasicNewsRecipe):
    # most of this is borrowed from ping's lithub recipe
    title = _name
    language = 'en'
    description = u'Commentary on science and gender by Zinnia Jones. https://genderanalysis.net/feed/'
    __author__ = 'holyspiritomb'
    category = 'trans, news, rss'
    oldest_article = 60
    max_articles_per_feed = 40
    remove_empty_feeds = True
    resolve_internal_links = True
    use_embedded_content = False

    feeds = [("Posts", "https://genderanalysis.net/feed/")]

    conversion_options = {
        'tags' : 'Blog, Trans, LGBTQ, Science',
    }

    keep_only_tags = [
        dict(name="h1", attrs={"class": "entry-title"}),
        dict(name="div", attrs={"class": "entry-meta"}),
        dict(name="div", attrs={"class": "entry-content"}),
    ]

    remove_attributes = [
        "height", "width", "sizes"
    ]

    extra_css = '''
    p img{width:98%}
    '''

    def populate_article_metadata(self, article, soup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)

    def preprocess_html(self, soup):
        imgs = soup.find_all("img")
        for img in imgs:
            if "zsmini.png" in img["src"]:
                img.decompose()
            else:
                continue
        return soup
