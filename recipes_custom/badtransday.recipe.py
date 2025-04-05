import os
import sys
from calibre.web.feeds.news import BasicNewsRecipe, classes
from zoneinfo import ZoneInfo
from calibre.utils.date import datetime

sys.path.append(os.environ["recipes_includes"])
from recipes_shared import WordPressNewsrackRecipe, format_title
# from calibre.utils.date import utcnow, parse_date
# from calibre.web.feeds import Feed

_name = "Bad Trans Day"


class BadTransDay(WordPressNewsrackRecipe, BasicNewsRecipe):
    # most of this is borrowed from ping's lithub recipe
    title = _name
    language = 'en'
    description = u'It was a bad trans day and here&#039;s why https://trans.cx'
    __author__ = 'holyspiritomb'
    category = 'trans, news, rss'
    oldest_article = 14
    max_articles_per_feed = 40
    remove_empty_feeds = True
    resolve_internal_links = False
    use_embedded_content = False

    feeds = [("Posts", "https://trans.cx/feed/")]

    conversion_options = {
        'tags' : 'Blog, Trans, LGBTQ',
        'authors': 'Zinnia Jones',
        'publisher': 'Zinnia Jones'
    }

    keep_only_tags = [
        dict(name="div", attrs={"id": "article_date"}),
        dict(name="h1", attrs={"class": "entry-title"}),
        dict(name="div", attrs={"class": "entry-content"}),
    ]

    remove_attributes = [
        "height", "width"
    ]

    extra_css = '''
        #article_date{font-size:0.8rem;text-transform:uppercase;}
        #article_desc{font-style:italic;font-size:1.2rem}
        p{font-size:1rem}
        .image-caption{font-size:0.8rem;font-style:italic}
        #article_source{font-size:0.8rem;}
        '''

    def populate_article_metadata(self, article, soup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
        nyc = ZoneInfo("America/New_York")
        nyc_dt = datetime.astimezone(datetime.now(), nyc)
        nyc_now_str = datetime.strftime(nyc_dt, "%b %-d, %Y at %-I:%M %p %Z")
        date_el = soup.find(attrs={"id": "article_date"})
        nyc_article_dt = datetime.astimezone(article.utctime, nyc)
        datestamp = datetime.strftime(nyc_article_dt, "%b %-d, %Y, %-I:%M %p %Z")
        headlink = soup.new_tag("a")
        headlink["href"] = article.url
        headlink.string = "Source"
        author_el = soup.find("a", attrs={"class": "author-link"})
        author_el.string = article.author
        date_el.append(author_el)
        date_el.append(" | ")
        date_el.append(datestamp)
        date_el.append(" | ")
        date_el.append(headlink)
        article_img = soup.find("img")
        if article_img:
            self.add_toc_thumbnail(article, article_img["src"])
        source_link_div = soup.new_tag("div")
        source_link_div["id"] = "article_source"
        source_link = soup.new_tag("a")
        source_link["href"] = article.url
        source_link.string = article.url
        source_link_div.append("This article was downloaded from ")
        source_link_div.append(source_link)
        source_link_div.append(" on ")
        source_link_div.append(nyc_now_str)
        source_link_div.append(".")
        hr = soup.new_tag("hr")
        soup.append(hr)
        soup.append(source_link_div)

    def preprocess_html(self, soup):
        headline = soup.find("h1")
        a_date = soup.new_tag("div")
        a_date["id"] = "article_date"
        headline.insert_before(a_date)
        return soup
