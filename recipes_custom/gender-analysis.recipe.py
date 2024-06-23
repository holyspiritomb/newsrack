
import os
import sys
from zoneinfo import ZoneInfo
from calibre.web.feeds.news import BasicNewsRecipe, classes

sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, WordPressNewsrackRecipe, format_title
from calibre.utils.date import utcnow, parse_date, datetime

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
    resolve_internal_links = False
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
    p img{max-width:98%}
    #article_source{font-size:0.8rem;}
    #meta_head{
        font-size:0.8rem;text-transform:uppercase
    }
    '''

    def populate_article_metadata(self, article, soup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
        nyc = ZoneInfo("America/New_York")
        nyc_dt = datetime.astimezone(article.utctime, nyc)
        nyc_dt_now = datetime.astimezone(datetime.now(), nyc)
        datestring = datetime.strftime(nyc_dt, "%b %-d, %Y, %-I:%M %p %Z")
        datestring_now = datetime.strftime(nyc_dt_now, "%b %-d, %Y, %-I:%M %p %Z")
        source_link_div = soup.new_tag("div")
        source_link_div["id"] = "article_source"
        source_link = soup.new_tag("a")
        source_link["href"] = article.url
        source_link.string = article.url
        source_link_div.append("This article was downloaded from ")
        source_link_div.append(source_link)
        source_link_div.append(" on ")
        source_link_div.append(datestring_now)
        source_link_div.append(".")
        hr = soup.new_tag("hr")
        soup.append(hr)
        soup.append(source_link_div)

        head_link = soup.new_tag("a")
        head_link["href"] = article.url
        head_link.append("View on Website")

        meta_div = soup.new_tag("div")
        meta_div["id"] = "meta_head"
        meta_div.append(article.author)
        meta_div.append(" | ")
        meta_div.append(datestring)
        meta_div.append(" | ")
        meta_div.append(head_link)

        headline = soup.find("h1")
        headline.insert_before(meta_div)

    def preprocess_html(self, soup):
        imgs = soup.find_all("img")
        for img in imgs:
            if "zsmini.png" in img["src"]:
                img.decompose()
            else:
                continue
        return soup
