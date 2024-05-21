# https://www.them.us/feed/rss
import json
import os
import re
import sys
from collections import OrderedDict
from datetime import datetime
from zoneinfo import ZoneInfo

from calibre.ebooks.BeautifulSoup import BeautifulSoup
# from calibre.utils.date import utcnow, parse_date, strptime
from calibre.web.feeds import Feed
from calibre.web.feeds.news import BasicNewsRecipe, classes, prefixed_classes
from calibre.web.feeds.feedparser import parse as fp_parse

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title

# convenience switches for when I'm developing
if "runner" in os.environ["recipes_includes"]:
    _masthead_prefix = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos"
else:
    _masthead_prefix = f"file://{os.environ['HOME']}/git/newsrack/recipes_custom/logos"
_masthead = f"{_masthead_prefix}/them-us.svg"
_name = "Them."


class Them(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    language = 'en'
    description = u' https://www.them.us/'
    __author__ = 'holyspiritomb'
    category = 'rss'
    oldest_article = 14
    max_articles_per_feed = 40
    remove_empty_feeds = False
    resolve_internal_links = False
    use_embedded_content = False
    publisher = "Conde Nast"
    masthead_url = _masthead

    feeds = ["https://www.them.us/feed/rss"]

    conversion_options = {
        'tags' : '',
        'authors': '',
    }

    remove_tags = [
        classes("ad article-body__footer"),
        prefixed_classes("ContentHeaderContributorImage SocialIconsWrapper PersistentAsideWrapper AdWrapper ContentHeaderByline ConsumerMarketing StickyMidContentAdWrapper LinkStackWrapper RecircMostPopularWrapper GenericCalloutWrapper")
    ]

    remove_attributes = [
        "height", "width", "style"
    ]

    keep_only_tags = [
        dict(attrs={"id": "main-content"}),
    ]

    extra_css = '''
        #article_date{font-size:0.8rem;text-transform:uppercase;}
        #article_desc{font-style:italic;font-size:1.2rem}
        p{font-size:1rem}
        img {max-width: 98vw;}
        .image-caption,.kg-card-hascaption>div{
                font-size:0.8rem;font-style:italic;padding-top:1rem;padding-bottom:1rem;}
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
        date_el = soup.find(attrs={"id": "article_date"})
        date_el.string = f"{article.author} | {datestring}"
        # desc_el = soup.find(attrs={"id": "article_desc"})
        # desc_el.string = article.summary
        # article_img = soup.find("img", attrs={"alt": True})
        # if article_img:
        #     img_uri = article_img["src"]
        #     self.add_toc_thumbnail(article, img_uri)

    def get_section(self, fp_entries, regex, url):
        categories = []
        for item in fp_entries:
            if url == item.link:
                for tag in item.tags[0:1]:
                    self.log(tag["term"])
                    if "Astrology" in tag["term"]:
                        tag_term = tag["term"].split(" / ")[1]
                    elif "Celebrity" in tag["term"]:
                        tag_term = tag["term"].split(" / ")[1]
                    elif "Movies" in tag["term"]:
                        tag_term = tag["term"].split(" / ")[1]
                    else:
                        tag_term = tag["term"].split(" / ")[0]
                    self.log(tag_term)
                    if regex.match(tag_term) is not None:
                        category = tag_term
                        categories.append(category)
                        continue
                    else:
                        break
        return categories

    def parse_feeds(self):
        feeds = BasicNewsRecipe.parse_feeds(self)
        fp_feed = fp_parse(self.feeds[0])
        fp_entries = fp_feed.entries
        cat_regex = re.compile(r'^[A-Z]')
        sectioned_feeds = OrderedDict()
        for feed in feeds:
            for article in feed.articles[:]:
                sections = self.get_section(fp_entries, cat_regex, article.url)
                for section in sections:
                    if section not in sectioned_feeds:
                        sectioned_feeds[section] = []
                    sectioned_feeds[section].append(article)
        new_feeds = []
        for key in sectioned_feeds.keys():
            if "Astrology" in key or "Celebrity" in key:
                self.log("skipping articles in:", key)
                continue
            else:
                curr_feed = Feed(self)
                curr_feed.title = key
                curr_feed.articles = sectioned_feeds[key]
                curr_feed.image_url = self.masthead_url
                new_feeds.append(curr_feed)
        # new_feeds = [f for f in feeds if len(f.articles[:]) > 0]
        return new_feeds

    def preprocess_html(self, soup):
        headline = soup.find("h1")
        a_date = soup.new_tag("div")
        # a_desc = soup.new_tag("h3")
        # a_desc["id"] = "article_desc"
        a_date["id"] = "article_date"
        # headline.insert_after(a_desc)
        headline.insert_after(a_date)
        return soup

    def postprocess_html(self, soup, _):
        return soup

    def preprocess_raw_html(self, raw_html, url):
        soup = BeautifulSoup(raw_html)
        p_metadata = soup.find("meta", attrs={"name": "parsely-metadata"})
        if p_metadata:
            p_json = json.loads(p_metadata["content"])
            description = p_json["description"]
            if description:
                headline = soup.find("h1", attrs={"data-testid": "ContentHeaderHed"})
                headline["data-description"] = description
        return str(soup)
