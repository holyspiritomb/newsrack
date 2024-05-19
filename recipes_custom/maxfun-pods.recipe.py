# https://maximumfun.org/episodes/secretly-incredibly-fascinating/secretly-incredibly-fascinating-
import re
import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
from calibre.web.feeds import Feed
from calibre.web.feeds.news import BasicNewsRecipe
from calibre.ebooks.BeautifulSoup import BeautifulSoup


# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title

# convenience switches for when I'm developing
if "runner" in os.environ["recipes_includes"]:
    _masthead_prefix = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos"
else:
    _masthead_prefix = f"file://{os.environ['HOME']}/git/newsrack/recipes_custom/logos"
# _masthead = ""

_name = "MaximumFun Podcasts"


class MaximumFun(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    language = 'en'
    description = u'Shownotes for the Maximum Fun Podcasts I listen to. https://maximumfun.org/'
    __author__ = 'holyspiritomb'
    category = 'news, rss'
    oldest_article = 90
    max_articles_per_feed = 200
    remove_empty_feeds = True
    resolve_internal_links = False
    use_embedded_content = True
    # masthead_url = _masthead
    # reverse_article_order = False

    # remove_tags =[]
    # remove_attributes = []

    feeds = [("All", "https://maximumfun.org/feed")]

    remove_attributes = ["height", "width", "style"]

    extra_css = '''
        img{max-width:98vw}
        #article_meta{text-transform:uppercase;font-size:0.7em;}
        p{font-size:1rem}
        #article_source{font-size:0.8rem;}
        '''

    # remove_tags = [
        # dict(name="img")
    # ]

    def get_article_url(self, article):
        article_url = article.link
        return article_url
    
    def populate_article_metadata(self, article, soup: BeautifulSoup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)

        nyc = ZoneInfo("America/New_York")
        nyc_dt = datetime.astimezone(article.utctime, nyc)
        datestring = datetime.strftime(nyc_dt, "%b %-d, %Y, %-I:%M %p %Z")
        nyc_dt_now = datetime.astimezone(datetime.now(), nyc)
        curr_datestring = datetime.strftime(nyc_dt_now, "%b %-d, %Y at %-I:%M %p %Z")
        article.title = format_title(article.title, nyc_dt)

        header = soup.new_tag("div")
        header["id"] = "article_meta"
        datetag = soup.new_tag("span")
        datetag["id"] = "date"
        datetag.string = datestring
        head_src = soup.new_tag("a")
        head_src["href"] = article.url
        head_src.string = "Episode Page"
        pod_src = soup.new_tag("a")
        ep_href = article.url
        pod_slug = ep_href.split("/")[4]
        pod_src["href"] = f"https://maximumfun.org/podcasts/{pod_slug}"
        pod_src.string = "Podcast"
        header.append(datetag)
        header.append(" | ")
        header.append(pod_src)
        header.append(" | ")
        header.append(head_src)
        headline = soup.find("h2")
        headline.insert_before(header)

        source_link_div = soup.new_tag("div")
        source_link_div["id"] = "article_source"
        source_link_div.append("This article was downloaded on ")
        source_link_div.append(curr_datestring)
        source_link_div.append(".")
        hr = soup.new_tag("hr")
        soup.append(hr)
        soup.append(source_link_div)

    def parse_feeds(self):
        feeds = BasicNewsRecipe.parse_feeds(self)
        parsed_feed = feeds[0]
        mf_prefix = "https://maximumfun.org/episodes/"
        pods = [
            (
                0, "Oh No, Ross and Carrie!",
                "We jump in to fringe science, spirituality, and the paranormal — so you don’t have to!",
                f"{mf_prefix}oh-no-ross-and-carrie",
                f"{_masthead_prefix}/maxfun-ohno.png"
                # "https://maximumfun.org/wp-content/uploads/2019/08/oh-no-ross-and-carrie-cover-400x400.jpg"
            ),
            (
                1, "Sawbones",
                "Join Justin and Dr. Sydnee McElroy on a marital tour of misguided medicine as they discuss the weird, gross, and sometimes downright dangerous ways we tried to solve our medical woes through the ages.",
                f"{mf_prefix}sawbones",
                f"{_masthead_prefix}/maxfun-sawbones.png"
                # "https://maximumfun.org/wp-content/uploads/2019/10/Sawbones-logo-final-1-400x400.png"
            ),
            (
                2, "Secretly Incredibly Fascinating",
                "Join Alex Schmidt and his co-host Katie Goldin for a weekly deep dive into the history, science, lore, and surprises that make everyday things secretly incredibly fascinating.",
                f"{mf_prefix}secretly-incredibly-fascinating",
                f"{_masthead_prefix}/maxfun-sif.png"
                # "https://maximumfun.org/wp-content/uploads/2023/01/Secretly-Incredibly-Fascinating-400x400.png"
            )
        ]
        pod_feeds = []
        for pod_num, pod_title, pod_desc, pod_prefix, pod_img in pods:
            pod_feed = Feed(self)
            pod_feed.title = pod_title
            pod_feed.image_url = pod_img
            pod_feed.description = pod_desc
            pod_feed.articles = []
            pod_feeds.append(pod_feed)
        for article in parsed_feed.articles[:]:
            for pod_num, pod_title, pod_desc, pod_prefix, pod_img in pods:
                if pod_prefix in article.url:
                    pod_feeds[pod_num].articles.append(article)
                # self.log.warn(f"{article.title} is subscriber-only, but that's okay")
                # feed.articles.remove(article)
        new_feeds = [f for f in pod_feeds if len(f.articles[:]) > 0]
        return new_feeds

    def preprocess_raw_html(self, raw_html, url):
        soup = BeautifulSoup(raw_html)
        for img in soup.findAll("img"):
            if img["src"] == "https://maximumfun.org/wp-content/uploads/2023/01/Secretly-Incredibly-Fascinating.png" or img["src"] == "https://maximumfun.org/wp-content/uploads/2021/02/Sawbones-logo-final-1-768x768-1.png" or img["src"] == "https://maximumfun.org/wp-content/uploads/2019/10/Sawbones-logo-final-1.png":
                img.decompose()
        return str(soup)

    def preprocess_html(self, soup):
        return soup
