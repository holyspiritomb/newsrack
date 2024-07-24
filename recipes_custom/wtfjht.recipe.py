import os
import sys
from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre.utils.date import utcnow, parse_date, datetime
from zoneinfo import ZoneInfo

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title

# convenience switches for when I'm developing
if "runner" in os.environ["recipes_includes"]:
    _masthead_prefix = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos"
else:
    _masthead_prefix = f"file://{os.environ['HOME']}/git/newsrack/recipes_custom/logos"
_masthead = f"{_masthead_prefix}/wtfjht-t.jpg"
_name = "WTF Just Happened Today"


class WTFJHT(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    oldest_article = 7
    language = 'en'
    __author__ = 'holyspiritomb'
    category = 'rss'
    max_articles_per_feed = 20
    no_stylesheets = True
    no_javascript = True
    remove_empty_feeds = True
    use_embedded_content = True
    publication_type = 'newspaper'
    masthead_url = _masthead
    description = (
        '''Today's essential guide to the daily shock and awe in national politics. Read in moderation. https://whatthefuckjusthappenedtoday.com/'''
    )

    feeds = [
        ('What the Fuck Just Happened Today', 'https://whatthefuckjusthappenedtoday.com/rss.xml')
    ]

    extra_css = '''
        #meta_head{font-size:0.8rem;text-transform:uppercase;}
        p{font-size:1rem}
        #article_source{font-size:0.8rem;}
        '''

    def populate_article_metadata(self, article, soup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
        nyc = ZoneInfo("America/New_York")
        nyc_dt = datetime.astimezone(datetime.now(), nyc)
        nyc_now_str = datetime.strftime(nyc_dt, "%b %-d, %Y at %-I:%M %p %Z")
        meta_head = soup.new_tag("div")
        meta_head["id"] = "meta_head"
        date_el = soup.new_tag("span")
        nyc_article_dt = datetime.astimezone(article.utctime, nyc)
        datestamp = datetime.strftime(nyc_article_dt, "%b %-d, %Y, %-I:%M %p %Z")
        headlink = soup.new_tag("a")
        headlink["href"] = article.url
        headlink.string = "View on Website"
        date_el.string = f"{article.author} | {datestamp} | "
        date_el.append(headlink)
        meta_head.append(date_el)
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
        headline = soup.find("h2")
        headline.insert_before(meta_head)
        headline.name = "h1"
        if soup.find("img"):
            toc_img = soup.find("img")
            self.add_toc_thumbnail(article, toc_img["src"])
        self.log(article)


calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
