import os
import sys
from calibre.web.feeds.news import BasicNewsRecipe, classes
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title
# from calibre.utils.date import utcnow, parse_date
# from calibre.web.feeds import Feed
# from calibre.ebooks.BeautifulSoup import BeautifulSoup

# convenience switches for when I'm developing
if "runner" in os.environ["recipes_includes"]:
    _masthead_prefix = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos"
else:
    _masthead_prefix = f"file://{os.environ['HOME']}/git/newsrack/recipes_custom/logos"
_masthead = f"{_masthead_prefix}/conspirituality-masthead.jpg"
_name = "Conspirituality Show Notes"


class Conspirituality(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    language = 'en'
    description = u'Show notes from the Conspirituality podcast. https://www.conspirituality.net/'
    __author__ = 'holyspiritomb'
    category = 'rss'
    oldest_article = 90
    max_articles_per_feed = 90
    remove_empty_feeds = True
    use_embedded_content = True
    masthead_url = _masthead

    conversion_options = {
        'tags' : 'Science',
    }

    feeds = [
        ("Conspirituality", "https://www.conspirituality.net/episodes?format=rss")
    ]

    extra_css = '''
        #article_date,#article_meta{font-size:0.8rem;text-transform:uppercase;}
        #article_desc{font-style:italic;font-size:1.2rem}
        p{font-size:1rem}
        img {max-width: 98vw;}
        .image-caption,.kg-card-hascaption>div{
                font-size:0.8rem;font-style:italic;padding-top:1rem;padding-bottom:1rem;}
        #article_source {font-size:0.8rem;}
        #article_source > a{word-wrap: break-word}
        '''

    def populate_article_metadata(self, article, soup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
        nyc = ZoneInfo("America/New_York")
        nyc_dt = datetime.astimezone(article.utctime, nyc)
        datestring = datetime.strftime(nyc_dt, "%b %-d, %Y, %-I:%M %p %Z")
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
        header = soup.new_tag("div")
        header["id"] = "article_meta"
        datetag = soup.new_tag("span")
        datetag["id"] = "article_date"
        datetag.string = datestring
        byline = soup.new_tag("span")
        byline["id"] = "article_auth"
        byline.string = article.author
        header.append(datetag)
        header.append(" | ")
        header.append(byline)
        headline = soup.find("h2")
        headline.insert_before(header)
