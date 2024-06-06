import os
import sys
from calibre.web.feeds.news import BasicNewsRecipe, classes
from datetime import timezone, timedelta, datetime, time
from zoneinfo import ZoneInfo

sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title
from calibre.utils.date import utcnow, parse_date
from calibre.web.feeds import Feed

_name = "Erin in the Morning"


class ErinInTheMorning(BasicNewsrackRecipe, BasicNewsRecipe):
    # most of this is borrowed from ping's lithub recipe
    title = _name
    language = 'en'
    description = u'News and discussion on trans legislation and life. https://www.erininthemorning.com/feed'
    __author__ = 'holyspiritomb'
    category = 'trans, news, rss'
    oldest_article = 14
    max_articles_per_feed = 40
    remove_empty_feeds = True
    resolve_internal_links = False
    use_embedded_content = True

    feeds = [("Posts", "https://www.erininthemorning.com/feed")]

    conversion_options = {
        'tags' : 'Blog, Trans, LGBTQ',
        'authors': 'Erin Reed',
        'publisher': 'Erin Reed'
    }

    remove_tags = [
        dict(name="div", attrs={"class": "subscription-widget-wrap"}),
        dict(name="div", attrs={"class": "image-link-expand"}),
        classes("subscription-widget-wrap-editor")
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
        curr_datestring = datetime.strftime(nyc_dt, "%b %-d, %Y at %-I:%M %p %Z")
        date_el = soup.find(attrs={"id": "article_date"})
        nyc_article_dt = datetime.astimezone(article.utctime, nyc)
        datestamp = datetime.strftime(nyc_article_dt, "%b %-d, %Y, %-I:%M %p %Z")
        headlink = soup.new_tag("a")
        headlink["href"] = article.url
        headlink.string = "Source"
        date_el.string = f"{article.author} | {datestamp} | "
        date_el.append(headlink)
        desc_el = soup.find(attrs={"id": "article_desc"})
        desc_el.string = article.summary
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
        source_link_div.append(".")
        hr = soup.new_tag("hr")
        soup.append(hr)
        soup.append(source_link_div)

    def preprocess_html(self, soup):
        headline = soup.find("h2")
        a_date = soup.new_tag("div")
        a_desc = soup.new_tag("h3")
        a_desc["id"] = "article_desc"
        a_date["id"] = "article_date"
        headline.insert_after(a_desc)
        headline.insert_after(a_date)
        return soup
