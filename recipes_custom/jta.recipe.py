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
    _masthead = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos/jta-masthead.svg"
else:
    _masthead = "file:///home/spiritomb/git/newsrack/recipes_custom/logos/jta-masthead.svg"


_name = "Jewish Telegraphic Agency"


class JTA(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    language = 'en'
    description = u'Global Jewish news from https://www.jta.org'
    __author__ = 'holyspiritomb'
    category = 'news, rss'
    oldest_article = 7
    max_articles_per_feed = 59
    remove_empty_feeds = True
    resolve_internal_links = False
    use_embedded_content = True
    # scale_news_images_to_device = True
    masthead_url = _masthead
    # test = True

    feeds = [("All", "https://www.jta.org/feed")]

    conversion_options = {
        'tags' : 'JTA, Jewish, News',
    }

    # keep_only_tags = []

    remove_attributes = ["height", "width"]

    remove_tags = [
        dict(name="div", id=re.compile("lightbox-inline-form"))
    ]

    extra_css = '''
    p img{max-width:98vw}
    #article_meta{text-transform:uppercase;font-size:0.7em;}
    '''

    def populate_article_metadata(self, article, soup: BeautifulSoup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
        # thumb = soup.find(attrs={"class": "sqs-block-image-figure"}).find("img")
        # thumb_url = thumb["src"]
        # self.add_toc_thumbnail(article, thumb_url)
        # self.log(article)
        nyc = ZoneInfo("America/New_York")
        nyc_dt = datetime.astimezone(article.utctime, nyc)
        # datestr = datetime.strftime(article.utctime, "%b %-d, %Y, %-I:%M %p %Z")
        datestring = datetime.strftime(nyc_dt, "%b %-d, %Y, %-I:%M %p %Z")
        header = soup.new_tag("div")
        header["id"] = "article_meta"
        datetag = soup.new_tag("span")
        datetag["id"] = "date"
        datetag.string = datestring
        srctag = soup.new_tag("a")
        srctag.string = article.url
        srctag["href"] = article.url
        header.append(article.author)
        header.append(" | ")
        header.append(datetag)
        # header.append(" | ")
        headline = soup.find("h2")
        headline.insert_before(header)
        headline.name = "h1"

    def preprocess_html(self, soup: BeautifulSoup):
        # self.log.warn(soup)
        return soup

    def parse_feeds(self):
        feeds = BasicNewsRecipe.parse_feeds(self)
        self.log.warn(feeds)
        for feed in feeds:
            self.log.warn(type(feed))
            for article in feed.articles[:]:
                self.log(type(article))
                # self.log(f"article.title is: {article.title}")
        return feeds


calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
