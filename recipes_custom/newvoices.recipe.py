import re
import os
import sys
from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre.web.feeds import Feed
from calibre.ebooks.BeautifulSoup import BeautifulSoup
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title
# from calibre.utils.date import utcnow, parse_date
# from calibre.web.feeds import Feed

# convenience switches for when I'm developing
if "runner" in os.environ["recipes_includes"]:
    _masthead = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos/newvoices-logo.png"
else:
    _masthead = "file:///home/spiritomb/git/newsrack/recipes_custom/logos/newvoices-logo.png"


_name = "New Voices"


class NewVoices(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    language = 'en'
    description = u'Published since 1991 by the independent non-profit Jewish Student Press Service, New Voices is the only Jewish and justice-focused magazine by and for college students. https://newvoices.org'
    __author__ = 'holyspiritomb'
    category = 'news, rss'
    oldest_article = 31
    max_articles_per_feed = 50
    remove_empty_feeds = True
    resolve_internal_links = False
    use_embedded_content = False
    # scale_news_images_to_device = True
    masthead_url = _masthead
    # test = True

    feeds = [("All", "https://newvoices.org/feed/")]
    extra_css = '''
    p{font-size:1em;}
    p img, div img{max-width:98vw}
    .article-meta{font-size:0.8em;}
    '''
    remove_tags = [
        classes("genesis-skip-link site-header fl-subscribe-form sections-list"),
        dict(attrs={"data-type": "footer"})
    ]
    remove_tags_before = [
        dict(name="div", attrs={"class": "site-inner"})
    ]

    remove_attributes = ["height", "width", "style"]

    def get_article_url(self, article):
        article_long_url = article.link
        article_url = article_long_url.split('?')[0]
        return article_url

    def populate_article_metadata(self, article, soup: BeautifulSoup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)

    def preprocess_raw_html(self, raw_html, url):
        soup = BeautifulSoup(raw_html, from_encoding='utf-8')
        for img in soup.findAll("img", attrs={"data-lazy-src": True}):
            self.log.warn(img)
            img["src"] = img["data-lazy-src"]
        for a in soup.findAll("a", href=re.compile(r"^https\:\/\/newvoices\.org\/author\/")):
            authpic = a.find("img")
            if authpic:
                authpic.extract()
        soup.find(name="span", string=re.compile(r"Get New Voices in Your Inbox\!")).extract()
        for node_content in soup.findAll("div", class_="fl-node-content"):
            node_content.unwrap()
        for row in soup.findAll("div", class_="fl-row"):
            row.unwrap()
        for row in soup.findAll("div", class_="fl-row-content-wrap"):
            row.unwrap()
        for col in soup.findAll("div", class_="fl-col"):
            col.unwrap()
        for col in soup.findAll("div", class_="fl-col-group"):
            col.unwrap()
        # for col in soup.findAll("div", class_="fl-module"):
            # col.unwrap()
        return str(soup)
