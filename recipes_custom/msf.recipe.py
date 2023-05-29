import os
import sys

from calibre.web.feeds.news import BasicNewsRecipe, classes
# from calibre import browser
# from collections import OrderedDict
from datetime import datetime, timedelta, timezone
from calibre.utils.date import utcnow, parse_date
from calibre.web.feeds import Feed
from calibre.ebooks.BeautifulSoup import BeautifulSoup


sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title

_name = 'Médecins Sans Frontières'


class MSF(BasicNewsRecipe, BasicNewsrackRecipe):
    title = _name
    __author__ = 'holyspiritomb'
    language = 'en'
    use_embedded_content = False
    no_stylesheets = True
    remove_javascript = True
    remove_attributes = ['height', 'width', 'style']
    encoding = 'utf-8'
    ignore_duplicate_articles = {'url'}
    masthead_url = "https://raw.githubusercontent.com/holyspiritomb/newsrack/spiritomb/static/img/msf.svg"
    keep_only_tags = [
        dict(name="h1", attrs={"class": "typo-headline"}),
        dict(attrs={"class": "hero__media"}),
        dict(name="article", attrs={"class": "article"}),
    ]
    remove_tags = [
        dict(name="button"),
        dict(name="source"),
        classes("eyebrow video-embed nav-in-page nav-in-page__socials nav-in-page__mobile form-field twitter-share share tags article-meta")
    ]
    remove_attributes = [
        "data-toolkit", "data-component"
    ]

    feeds = [
        ("Main", "https://www.msf.org/rss/all"),
    ]
    extra_css = '''
        #article_date{font-size:0.8rem;text-transform:uppercase;}
        #article_desc{font-style:italic;font-size:1.2rem}
        p{font-size:1rem}
        .caption, .caption ~ span{font-size:0.8rem;font-style:italic}
        '''

    def populate_article_metadata(self, article, soup, _):
        self.log(article)
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
        date_el = soup.find(attrs={"id": "article_date"})
        datestamp = datetime.strftime(article.utctime, "%b %-d, %Y, %-I:%M %p")
        if "None" in str(article.author):
            date_el.string = datestamp
        else:
            date_el.string = f"{article.author} | {datestamp}"
        # desc_el = soup.find(attrs={"id": "article_desc"})
        # desc_el.string = article.summary
        # article_img = soup.find("img")

    def preprocess_raw_html(self, raw_html, url):
        soup = BeautifulSoup(raw_html)
        headline = soup.find("h1", attrs={"class": "typo-headline"})
        headline["class"] = "typo-headline"
        return str(soup)

    def preprocess_html(self, soup):
        headline = soup.find("h1")
        a_date = soup.new_tag("div")
        # a_desc = soup.new_tag("h3")
        # a_desc["id"] = "article_desc"
        a_date["id"] = "article_date"
        # headline.insert_after(a_desc)
        headline.insert_after(a_date)
        # the css classes on MSF's site are garbage
        for element in soup.find_all(class_=True):
            classes_list = element["class"]
            for item in element["class"]:
                if "toolkit" in item or "component" in item or "container" in item:
                    element["class"].remove(item)
                if item == "[":
                    bracket_idx = int(classes_list.index("["))
                    if bracket_idx > 0:
                        del element["class"][bracket_idx:]
                    else:
                        del element["class"]
                    break
        return soup
