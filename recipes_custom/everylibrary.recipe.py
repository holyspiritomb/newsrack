import os
import sys

from calibre import browser
from calibre.web.feeds.news import BasicNewsRecipe, classes
from datetime import datetime

sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title
from calibre.ebooks.BeautifulSoup import BeautifulSoup

_name = "EveryLibrary"


class EveryLibrary(BasicNewsrackRecipe, BasicNewsRecipe):
    # most of this is borrowed from ping's lithub recipe
    title = _name
    description = u'EveryLibrary'
    language = 'en'
    __author__ = 'holyspiritomb'
    oldest_article = 90
    max_articles_per_feed = 40
    remove_empty_feeds = True
    resolve_internal_links = False
    remove_javascript = True
    no_stylesheets = True
    # use_embedded_content = True
    masthead_url = "https://assets.nationbuilder.com/votelibraries/sites/1019/meta_images/original/everylibrary_logo.jpg"
    feeds = [("News", "https://www.everylibrary.org/news_and_updates.rss")]
    remove_tags = [
        dict(class_="hidden"),
        dict(class_="hidden-lg"),
        dict(class_="hidden-xs"),
        dict(class_="hidden-sm"),
        dict(class_="hidden-md"),
        dict(name="img", attrs={"style": "float: left;"}),
        dict(name="div", class_="nb-btn"),
        dict(name="div", class_="like-page"),
        dict(name="iframe"),
    ]
    remove_attributes = [
        "width", "height", "style"
    ]
    keep_only_tags = [
        dict(name="h1", class_="headline"),
        dict(name="img", id="lead_img"),
        dict(name="div", class_="content"),
        dict(name="div", id="content"),
        dict(name="div", id="bt50bodywrap"),

    ]

    def populate_article_metadata(self, article, soup, _):
        self.log(article)
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
        date_el = soup.find(attrs={"id": "article_date"})
        datestamp = datetime.strftime(article.utctime, "%b %-d, %Y, %-I:%M %p")
        date_el.string = f"{article.author} | {datestamp}"
        desc_el = soup.find(attrs={"id": "article_desc"})
        desc_soup = BeautifulSoup(article.summary)
        desc_el.append(desc_soup)

    def preprocess_raw_html(self, raw_html, url):
        soup = BeautifulSoup(raw_html)
        bgimg = soup.find("main").find("div", attrs={"style": True, "id": True})
        img_url = ""
        if bgimg:
            self.log(bgimg)
            style_str = bgimg["style"]
            st = style_str.split(";")[0]
            img_url = st.split("'")[1]
            img = soup.new_tag("img")
            img["src"] = img_url
            img["id"] = "lead_img"
            head = soup.find("h1", class_="headline")
            head.insert_after(img)
            bgimg.extract()
        hrs = soup.find_all("hr")
        for hr in hrs:
            hr.extract()
        return str(soup)

    def preprocess_html(self, soup):
        headline = soup.find("h1")
        a_date = soup.new_tag("div")
        a_desc = soup.new_tag("h3")
        a_desc["id"] = "article_desc"
        a_date["id"] = "article_date"
        headline.insert_after(a_desc)
        headline.insert_after(a_date)
        return soup

    def get_browser(self, *args, **kwargs):
        return self

    def clone_browser(self, *args, **kwargs):
        return self.get_browser()

    def open_novisit(self, *args, **kwargs):
        br = browser()
        return br.open_novisit(*args, **kwargs)

    open = open_novisit


calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
