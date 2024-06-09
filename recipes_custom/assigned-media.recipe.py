
import os
import sys
from calibre.web.feeds.news import BasicNewsRecipe, classes
from datetime import date, timezone, timedelta, datetime
from zoneinfo import ZoneInfo

sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, WordPressNewsrackRecipe, format_title
from calibre.utils.date import utcnow, parse_date
# from calibre.web.feeds import Feed

_name = "Assigned Media"


class Assigned(BasicNewsrackRecipe, BasicNewsRecipe):
    # most of this is borrowed from ping's lithub recipe
    title = _name
    language = 'en'
    description = u'Daily coverage of anti-trans propaganda'
    __author__ = 'holyspiritomb'
    category = 'trans, news, rss'
    oldest_article = 7
    max_articles_per_feed = 40
    remove_empty_feeds = True
    resolve_internal_links = False
    use_embedded_content = True
    scale_news_images_to_device = True

    feeds = [("Breaking News", "https://www.assignedmedia.org/breaking-news?format=rss"),
             ("Newsletter", "https://www.assignedmedia.org/newsletter?format=rss")]

    conversion_options = {
        'tags' : 'Blog, Trans, LGBTQ, News',
    }

    # keep_only_tags = []

    remove_attributes = ["height", "width"]

    extra_css = '''
    p img{max-width:98vw}
    #article_meta{text-transform:uppercase;font-size:0.7em;}
    #article_source{font-size:0.8rem;}
    '''

    def populate_article_metadata(self, article, soup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
        thumb = soup.find(attrs={"class": "sqs-block-image-figure"}).find("img")
        if thumb:
            self.add_toc_thumbnail(article, thumb["src"])
        nyc = ZoneInfo("America/New_York")
        nyc_dt = datetime.astimezone(datetime.now(), nyc)
        nyc_article_dt = datetime.astimezone(article.utctime, nyc)
        datestrny = datetime.strftime(nyc_article_dt, "%b %-d, %Y, %-I:%M %p %Z")
        nyc_now_str = datetime.strftime(nyc_dt, "%b %-d, %Y, %-I:%M %p %Z")
        header = soup.new_tag("div")
        header["id"] = "article_meta"
        datetag = soup.new_tag("span")
        datetag["id"] = "date"
        datetag.string = datestrny
        srctag = soup.new_tag("a")
        srctag.string = "source"
        srctag["href"] = article.url
        header.append(datetag)
        header.append(" | ")
        header.append(article.author)
        header.append(" | ")
        header.append(srctag)
        headline = soup.find("h2")
        headline.insert_before(header)
        source_link_div = soup.new_tag("div")
        source_link_div["id"] = "article_source"
        source_link = soup.new_tag("a")
        source_link["href"] = article.url
        source_link.string = article.url
        source_link_div.append("This article was downloaded from ")
        source_link_div.append(source_link)
        source_link_div.append(" at ")
        source_link_div.append(nyc_now_str)
        source_link_div.append(".")
        hr = soup.new_tag("hr")
        soup.append(hr)
        soup.append(source_link_div)

    def preprocess_html(self, soup):
        # self.log.warn(soup)
        return soup
