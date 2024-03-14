#!/usr/bin/env python
# vim:fileencoding=utf-8

import os
import sys
import json
import re

from calibre import browser
from datetime import timezone, timedelta
from calibre.ebooks.BeautifulSoup import BeautifulSoup
from calibre.web.feeds import Feed
from calibre.web.feeds.news import BasicNewsRecipe
# from calibre.utils.date import utcnow, parse_date

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title


_name = "Live Science"


class LiveScience(BasicNewsRecipe, BasicNewsrackRecipe):
    title = _name
    description = "Live Science is a science news website that publishes stories in a wide variety of topics such as Space, Animals, Health, Archaeology, Human behavior and Planet Earth. Sourced from https://www.livescience.com/feeds/all"
    __author__ = 'yodha8'
    language = 'en'
    oldest_article = 7
    max_articles_per_feed = 100
    no_stylesheets = True
    remove_javascript = False
    auto_cleanup = False
    use_embedded_content = False

    conversion_options = {
        'tags' : 'Science, News, Live Science, Periodical',
    }
    feeds = [
        ('Live Science All Articles', 'https://www.livescience.com/feeds/all'),
    ]
    keep_only_tags = [
        dict(attrs={"id": "hero"}),
        dict(attrs={"class": "hero-image-wrapper"}),
        dict(attrs={"id": "article-body"}),
    ]
    remove_tags_before = [
        dict(name="div", class_="news-article")
    ]
    remove_tags = [
        dict(name="div", class_="ad-unit"),
        dict(name="source", attrs={"type": "image/webp"}),
        dict(name="nav", class_="socialite-widget"),
        dict(name="div", class_="fancy-box"),
    ]
    remove_attributes = [
        "style"
    ]

    extra_css = """
        div.gallery-el{max-width:90vw;}
        img{max-width:90vw;}
        .gallery-el img{max-width:90vw;}
        div.image-caption,span.caption-text,span.credit,div#article_source{font-size:0.8rem;}
        #article-body p{font-size:1rem;}
        h1{font-size:1.75rem;}
        h2{font-size:1.5rem;}
        p.strapline{font-size:1.5rem;font-style:italic;}
    """

    def populate_article_metadata(self, article, soup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
        article_body = soup.find("div", attrs={"id": "article-body"})
        source_link_div = soup.new_tag("div")
        source_link_div["id"] = "article_source"
        source_link = soup.new_tag("a")
        source_link["href"] = article.url
        source_link.string = article.url
        source_link_div.append("This article was downloaded from ")
        source_link_div.append(source_link)
        source_link_div.append(".")
        hr = soup.new_tag("hr")
        article_body.append(hr)
        article_body.append(source_link_div)

    def parse_feeds(self):
        parsed_feeds = BasicNewsRecipe.parse_feeds(self)
        for feed in parsed_feeds:
            for article in feed.articles[:]:
                if 'OBESITY' in article.title.upper() or 'WEIGHT LOSS' in article.title.upper():
                    self.log.warn(f"removing {article.title} from feed")
                    feed.articles.remove(article)
        articles = []
        for feed in parsed_feeds:
            articles.extend(feed.articles)
        articles = sorted(articles, key=lambda a: a.utctime, reverse=True)
        new_feeds = []
        curr_feed = None
        parsed_feed = parsed_feeds[0]
        for i, a in enumerate(articles, start=1):
            date_published = a.utctime.replace(tzinfo=timezone.utc)
            date_published_loc = date_published.astimezone(
                timezone(offset=timedelta(hours=-4))
            )
            article_index = f"{date_published_loc:%B %-d, %Y}"
            if i == 1:
                curr_feed = Feed(log=parsed_feed.logger)
                curr_feed.title = article_index
                curr_feed.description = parsed_feed.description
                curr_feed.image_url = parsed_feed.image_url
                curr_feed.image_height = parsed_feed.image_height
                curr_feed.image_alt = parsed_feed.image_alt
                curr_feed.oldest_article = parsed_feed.oldest_article
                curr_feed.articles = []
                curr_feed.articles.append(a)
                continue
            if curr_feed.title == article_index:
                curr_feed.articles.append(a)
            else:
                new_feeds.append(curr_feed)
                curr_feed = Feed(log=parsed_feed.logger)
                curr_feed.title = article_index
                curr_feed.description = parsed_feed.description
                curr_feed.image_url = parsed_feed.image_url
                curr_feed.image_height = parsed_feed.image_height
                curr_feed.image_alt = parsed_feed.image_alt
                curr_feed.oldest_article = parsed_feed.oldest_article
                curr_feed.articles = []
                curr_feed.articles.append(a)
            if i == len(articles):
                # last article
                new_feeds.append(curr_feed)
        new_feeds = [f for f in new_feeds if len(f.articles[:]) > 0]
        return new_feeds

    def preprocess_raw_html(self, raw_html, url):
        soup = BeautifulSoup(raw_html)
        head = soup.find("head")
        ld_jsons = head.findAll("script", attrs={"type": "application/ld+json"})
        for jsontag in ld_jsons:
            jsonstr = jsontag.string
            # ld_json = json.loads(jsonstr)
            # self.log(jsonstr)
            if '"@type": "Product"' in jsonstr:
                self.abort_article("product review")
                break
        parselytags = head.find("meta", attrs={"name": "parsely-tags"})
        if parselytags:
            if "type_deal" in parselytags["content"]:
                self.abort_article("Aborting article that is just a long ad.")
        body = soup.find(attrs={"id": "article-body"})
        for img in body.find_all("img", attrs={"src": "https://vanilla.futurecdn.net/livescience/media/img/missing-image.svg"}):
            dsrcset = img["data-srcset"]
            if dsrcset:
                newsrc = dsrcset.split(",")[-1].strip().split()[0]
                img["src"] = newsrc
        div = body.find("div", attrs={"class": "imageGallery-wrapper"})
        if div:
            if div.previous_sibling.name == "script":
                imgreg = re.compile("var data = ({.*?});", re.DOTALL)
                js = div.previous_sibling.string
                matches = imgreg.search(js)
                if matches:
                    imgjson = matches.group(1)
                    galleryj = json.loads(imgjson)
                    gallerydata = galleryj["galleryData"]
                    img_total = len(gallerydata)
                    newdiv = soup.new_tag("div", attrs={"class": "gallery-el"})
                    for i in range(0, img_total):
                        imgsrc = gallerydata[i]["image"]["src"]
                        imgalt = gallerydata[i]["image"]["alt"]
                        imgcapt = gallerydata[i]["image"]["caption"]
                        thisimg = soup.new_tag("img", attrs={"src": imgsrc, "alt": imgalt})
                        cap = soup.new_tag("div", attrs={"class": "image-caption"})
                        cap.string = imgcapt
                        newdiv.append(thisimg)
                        newdiv.append(cap)
                    div.insert_before(newdiv)
                    div.extract()
        return str(soup)

    def get_browser(self, *a, **kw):
        kw[
            "user_agent"
        ] = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        br = BasicNewsRecipe.get_browser(self, *a, **kw)
        return br

    def clone_browser(self, *args, **kwargs):
        return self.get_browser()

    def open_novisit(self, *args, **kwargs):
        br = browser()
        return br.open_novisit(*args, **kwargs)

    open = open_novisit


calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
