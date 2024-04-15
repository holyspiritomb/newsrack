# TODO: https://lingthusiasm.com/rss
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
from calibre.web.feeds.news import BasicNewsRecipe
# from datetime import timezone, timedelta, datetime, time

sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title
# from calibre.utils.date import utcnow, parse_date
# from calibre.web.feeds import Feed

_name = "Lingthusiasm"


class Lingthusiasm(BasicNewsrackRecipe, BasicNewsRecipe):
    # most of this is borrowed from ping's lithub recipe
    title = _name
    language = 'en'
    description = u'Lingthusiasm podcast transcripts, show notes, and Tumblr posts by the hosts. https://lingthusiasm.com/ https://allthingslinguistic.com/ https://www.superlinguo.com/'
    __author__ = 'holyspiritomb'
    category = 'blogs, rss'
    oldest_article = 60
    max_articles_per_feed = 10
    remove_empty_feeds = True
    resolve_internal_links = False
    use_embedded_content = True
    recursions = 0

    feeds = [
        ("Posts", "https://lingthusiasm.com/rss"),
        ("All Things Linguistic", "https://allthingslinguistic.com/rss"),
        ("Superlinguo", "https://www.superlinguo.com/rss")
    ]

    conversion_options = {
        'tags' : 'Blog, Linguistics, Science',
    }

    remove_attributes = [
        "height", "width", "sizes"
    ]

    extra_css = '''
    p img{width:98%}
    #article_source{font-size:0.8rem;}
    blockquote{border-left:3px solid black; padding-left:7px}
    '''

    def populate_article_metadata(self, article, soup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
        nyc = ZoneInfo("America/New_York")
        nyc_dt_now = datetime.astimezone(datetime.now(), nyc)
        curr_datestring = datetime.strftime(nyc_dt_now, "%b %-d, %Y at %-I:%M %p %Z")
        source_link_div = soup.new_tag("div")
        source_link_div["id"] = "article_source"
        source_link = soup.new_tag("a")
        source_link["href"] = article.url
        source_link.string = article.url
        source_link_div.append("This article was downloaded from ")
        source_link_div.append(source_link)
        source_link_div.append(" on ")
        source_link_div.append(curr_datestring)
        source_link_div.append(".")
        hr = soup.new_tag("hr")
        soup.append(hr)
        soup.append(source_link_div)

    def preprocess_html(self, soup):
        links = soup.find_all("a")
        for a in links:
            if a["href"][0:16] == "https://href.li/":
                new_href = a["href"][17:]
                a["href"] = new_href
            else:
                continue
        return soup

    def parse_feeds(self):
        feeds = BasicNewsRecipe.parse_feeds(self)
        new_feeds = [f for f in feeds if len(f.articles[:]) > 0]
        return new_feeds
