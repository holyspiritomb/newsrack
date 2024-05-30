import os
import sys
import re
from datetime import datetime
from zoneinfo import ZoneInfo

from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre.ebooks.BeautifulSoup import BeautifulSoup

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
    # compress_news_images_auto_size = 2
    feeds = [("Posts", "https://www.aiweirdness.com/rss/")]

    remove_attributes = [
        "height", "width", "style"
    ]

    extra_css = '''
        img:not(.kg-gallery-image):not(.kg-image-card){width:98w !important}
        .kg-gallery-row{width:100w;}
        .kg-gallery-row > img.kg-gallery-image{display:inline;}
        .kg-gallery-row.kg-gallery-row-2 > img.kg-gallery-image{width:45%;}
        .kg-gallery-row.kg-gallery-row-3 > img.kg-gallery-image{width:30%;}
        #article_source{font-size:0.8rem;}
        blockquote{padding-left:7px}
        #article_meta{text-transform:uppercase;font-size:0.8rem;}
        .caption{font-style:italic;font-size:0.8rem;}
        #article_source{font-size:0.8rem;}
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

        header = soup.new_tag("div")
        header["id"] = "article_meta"
        datetag = soup.new_tag("span")
        datetag["id"] = "date"
        datetag.string = datestring
        head_src = soup.new_tag("a")
        head_src["href"] = article.url
        head_src.string = "Article source"
        header.append(datetag)
        header.append(" | ")
        header.append(head_src)
        headline = soup.find("h2")
        headline.insert_before(header)

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

        bonus_link = soup.find("a", attrs={"id": "paid_link"})
        if bonus_link:
            bonus_link["href"] = article.url
        toc_img = soup.find("img")
        if toc_img:
            self.add_toc_thumbnail(article, toc_img["src"])

    def preprocess_raw_html(self, raw_html, url):
        soup = BeautifulSoup(raw_html)
        body = soup.find("body")
        if not body.find("img"):
            headline = soup.find("h2")
            title_str = self.tag_to_string(headline)
            paid_div = soup.new_tag("div")
            paid_div["id"] = "paid_div"
            paid_link = soup.new_tag("a")
            paid_link["id"] = "paid_link"
            paid_link["href"] = "#placeholder"
            paid_link.append(title_str)
            paid_div.append("View this paid post here: ")
            paid_div.append(paid_link)
            paid_div.append(".")
            body.append(paid_div)
        else:
            for span in soup.find_all("span", string=re.compile("Image description: ")):
                span.attrs["class"] = "caption"
                span.name = "div"
            for fc in soup.find_all("figcaption"):
                fc.attrs["class"] = "caption"
                fc.name = "div"
            for div in soup.find_all("div", class_="kg-gallery-container"):
                div.unwrap()
            for div in soup.find_all("div", class_="kg-gallery-image"):
                for img in div.find_all("img"):
                    img.attrs["class"] = "kg-gallery-image"
                div.unwrap()
            for div in soup.find_all("div", class_="kg-gallery-row"):
                row_imgs = len(div.find_all("img"))
                div.attrs["class"] = "kg-gallery-row kg-gallery-row-{}".format(row_imgs)
            for img in soup.find_all("img"):
                if "w600" not in img["src"]:
                    src = img["src"]
                    src_w = src.replace("/images/", "/images/size/w600/")
                    img["src"] = src_w
        return str(soup)

    def parse_feeds(self):
        feeds = BasicNewsRecipe.parse_feeds(self)
        for feed in feeds:
            for article in feed.articles[:]:
                self.log(article)
                if not article.content:
                    self.log.warn(f"subscriber-only article {article.title}")
                    # feed.articles.remove(article)
        new_feeds = [f for f in feeds if len(f.articles[:]) > 0]
        return new_feeds
