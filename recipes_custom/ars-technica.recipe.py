__license__ = 'GPL v3'
__copyright__ = '2008-2012, Darko Miletic <darko.miletic at gmail.com>'
# modified by spiritomb for newsrack use
'''
arstechnica.com
'''
import json
import os
import re
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
from calibre.ebooks.BeautifulSoup import BeautifulSoup

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title
from calibre.web.feeds.news import BasicNewsRecipe, classes


# convenience switches for when I'm developing
if "runner" in os.environ["recipes_includes"]:
    _masthead_prefix = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos"
else:
    _masthead_prefix = f"file://{os.environ['HOME']}/git/newsrack/recipes_custom/logos"
_masthead = f"{_masthead_prefix}/arstechnica.svg"

_name = "Ars Technica"


class ArsTechnica(BasicNewsRecipe, BasicNewsrackRecipe):
    title = _name
    language = 'en'
    __author__ = 'Darko Miletic, Sujata Raman, Alexis Rohou, Tom Sparks, holyspiritomb'
    description = 'Ars Technica: Serving the technologist for 1.2 decades'
    publisher = 'Conde Nast Publications'
    masthead_url = _masthead
    oldest_article = 3
    max_articles_per_feed = 100
    no_stylesheets = True
    encoding = 'utf-8'
    use_embedded_content = False
    remove_empty_feeds = True
    conversion_options = {
        'tags': 'Technology, Science, Periodical, Ars Technica',
    }
    extra_css = '''
    body {font-family: Lato, Roboto, Arial,sans-serif}
    .heading{font-family: Lato, Roboto, Arial,sans-serif}
    .byline{font-weight: bold; line-height: 1em; font-size: 0.625em; text-decoration: none}
    img{display: block; max-width:98vw}
    .caption-text{font-size:small; font-style:italic}
    .caption-byline{font-size:small; font-style:italic; font-weight:bold}
    .video, .page-numbers, .story-sidebar { display: none }
    .image { display: block }
    #article_source{font-size:0.8rem;}
    '''

    keep_only_tags = [
        dict(itemprop=['headline', 'description']),
        classes('post-meta article-guts standalone'),
    ]

    remove_tags = [
        classes('site-header video corner-info article-expander left-column related-stories ad_xrail ad_xrail_top ad_xrail_last ad_notice'),
        dict(name=['object', 'link', 'embed', 'iframe', 'meta']),
        dict(id=['social-left', 'article-footer-wrap']),
        dict(name='nav', attrs={'class': 'subheading'}),
    ]
    remove_attributes = ['lang', 'style', 'height', 'width']

    # Feed are found here: http://arstechnica.com/rss-feeds/
    feeds = [
        ('Features', 'http://feeds.arstechnica.com/arstechnica/features'),
        ('Technology Lab', 'http://feeds.arstechnica.com/arstechnica/technology-lab'),
        ('Gear &amp; Gadgets', 'http://feeds.arstechnica.com/arstechnica/gadgets'),
        ('Ministry of Innovation', 'http://feeds.arstechnica.com/arstechnica/business'),
        # ('Risk Assessment', 'http://feeds.arstechnica.com/arstechnica/security'),
        ('Law &amp; Disorder', 'http://feeds.arstechnica.com/arstechnica/tech-policy'),
        ('Infinite Loop', 'http://feeds.arstechnica.com/arstechnica/apple'),
        ('Opposable Thumbs', 'http://feeds.arstechnica.com/arstechnica/gaming'),
        ('Scientific Method', 'http://feeds.arstechnica.com/arstechnica/science'),
        # ('The Multiverse', 'http://feeds.arstechnica.com/arstechnica/multiverse'),
        ('Staff', 'http://feeds.arstechnica.com/arstechnica/staff-blogs'),
        # ('Open Source', 'http://feeds.arstechnica.com/arstechnica/open-source'),
        ('microsoft', 'http://feeds.arstechnica.com/arstechnica/microsoft'),
        # ('software', 'http://feeds.arstechnica.com/arstechnica/software'),
        # ('telecom', 'http://feeds.arstechnica.com/arstechnica/telecom'),
        # ('Internet', 'http://feeds.arstechnica.com/arstechnica/web'),
        ('Ars Technica', 'http://feeds.arstechnica.com/arstechnica/index'),
    ]

    def populate_article_metadata(self, article, soup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
        # nyc_dt = datetime.astimezone(article.utctime, nyc)
        # datestring = datetime.strftime(nyc_dt, "%b %-d, %Y, %-I:%M %p %Z")
        nyc = ZoneInfo("America/New_York")
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
        thumb = soup.find("img", attrs={"id": "toc_image"})
        if thumb:
            thumb_src = thumb["src"]
            self.add_toc_thumbnail(article, thumb_src)
            thumb.extract()

    recursions = 1

    def is_link_wanted(self, url, tag):
        return re.search(r'/[0-9]/$', url) is not None

    def parse_feeds(self):
        feeds = BasicNewsRecipe.parse_feeds(self)
        for feed in feeds:
            for article in feed.articles[:]:
                if 'OBESITY' in article.title.upper() or 'WEIGHT LOSS' in article.title.upper() or 'DEALMASTER' in article.title.upper():
                    self.log.warn(f"removing {article.title} from feed")
                    feed.articles.remove(article)
        new_feeds = [f for f in feeds if len(f.articles[:]) > 0]
        return new_feeds

    def postprocess_html(self, soup, first_fetch):
        if not first_fetch:
            for x in soup.findAll(itemprop=['headline', 'description']):
                x.extract()
            for x in soup.findAll(**classes('post-meta')):
                x.extract()
        return soup

    def preprocess_raw_html(self, raw_html, url):
        soup = BeautifulSoup(raw_html)
        p_metadata = soup.find("meta", attrs={"name": "parsely-metadata"})
        if p_metadata:
            p_json = json.loads(p_metadata["content"])
            imgurl = p_json["listing_image_url"]
            if imgurl:
                article_guts = soup.find(attrs={"class": "article-guts"})
                self.log("***", url, imgurl)
                toc_img = soup.new_tag("img")
                toc_img["src"] = imgurl
                toc_img["id"] = "toc_image"
                article_guts.append(toc_img)
        return str(soup)