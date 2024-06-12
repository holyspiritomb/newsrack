#!/usr/bin/env python
# vim:fileencoding=utf-8

import os
import sys
import json
import re

from calibre import browser
from datetime import timezone, timedelta
from datetime import datetime as dt
from zoneinfo import ZoneInfo

from calibre.ebooks.BeautifulSoup import BeautifulSoup
from calibre.web.feeds import Feed
from calibre.web.feeds.news import BasicNewsRecipe, classes
# from calibre.utils.date import utcnow, parse_date

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title, parse_date


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
    resolve_internal_links = False

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
        dict(name="source", attrs={"type": "image/webp"}),
        dict(attrs={"id": re.compile("taboola")}),
        dict(attrs={"class": re.compile("jwplayer")}),
        dict(attrs={"aria-label": "Breadcrumbs"}),
        classes("newsletter-form__wrapper newsletter-inbodyContent-slice ad-unit socialite-widget fancy-box hawk-nest"),
    ]
    remove_attributes = [
        "data-before-rewrite-localise",
        "data-bordeaux-image-check",
        "data-hl-processed",
        "data-skip",
        "referrerpolicy",
        "style",
        "target",
    ]

    filter_out = ["obesity", "wegovy", "weight loss"]

    extra_css = """
        div.gallery-el{max-width:90vw;}
        img{max-width:90vw;}
        .gallery-el img{max-width:90vw;}
        .image-caption,
        .caption-text,
        .credit,
        #article_source,#tiny_header{
            font-size:0.8rem;
        }
        #article-body p{font-size:1rem;}
        h1{font-size:1.75rem;}
        h2{font-size:1.5rem;}
        .strapline{font-size:1.25rem;font-style:italic;}
        #tiny_header{text-transform: uppercase;}
    """

    def populate_article_metadata(self, article, soup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
        nyc = ZoneInfo("America/New_York")
        nyc_dt = dt.astimezone(article.utctime, nyc)
        datestring = dt.strftime(nyc_dt, "%b %-d, %Y, %-I:%M %p %Z")

        article_date = soup.find(class_="author-byline__date")
        article_date.clear()
        article_date.string = datestring

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
        headlink = soup.find("a", attrs={"id": "headlink"})
        if headlink:
            headlink["href"] = article.url
        toc_img = soup.find("img", attrs={"class": "image-hero"})
        if toc_img:
            self.add_toc_thumbnail(article, toc_img['src'])

    def parse_feeds(self):
        parsed_feeds = BasicNewsRecipe.parse_feeds(self)
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
        for feed in new_feeds:
            for article in feed.articles[:]:
                for word in self.filter_out:
                    if word.upper() in article.title.upper() or word.upper() in article.summary.upper():
                        self.log.warn(f"\t\tremoving \"{article.title}\" from _{feed.title}_ feed (keyword: {word})")
                        feed.articles.remove(article)
                        break
                    else:
                        continue
        new_feeds = [f for f in new_feeds if len(f.articles[:]) > 0]
        return new_feeds

    def preprocess_html(self, soup):
        return soup

    def preprocess_raw_html(self, raw_html, url):
        soup = BeautifulSoup(raw_html)

        ld_json = self.get_ld_json(soup, str)
        if ld_json["@type"] == "Product":
            self.abort_article("Aborting product review article.")

        parsely_tags = soup.find(attrs={"name": "parsely-tags"})
        if "type_deal" in parsely_tags["content"]:
            self.abort_article("Aborting product review article.")

        article_headline = soup.find("h1")

        section = ld_json["articleSection"]

        new_header_div = soup.new_tag("div", attrs={"id": "tiny_header"})

        if section:
            section_div = soup.new_tag("div", attrs={"id": "article_section"})
            section_div.string = section
            new_header_div.append(section_div)

        section_type = soup.find("a", class_="byline-article-type")
        if section_type:
            section_type.extract()
            new_header_div.append(section_type)
            new_header_div.append(" | ")

        authors = soup.findAll(class_="author-byline__author-name")
        if authors:
            if len(authors) > 1:
                new_header_div.append(authors[0])
                for a in authors[1:]:
                    new_header_div.append(", ")
                    new_header_div.append(a)
            else:
                new_header_div.append(authors[0])
            new_header_div.append(" | ")

        article_date = soup.find(class_="author-byline__date")
        if article_date:
            article_date.extract()
            new_header_div.append(article_date)
            new_header_div.append(" | ")

        article_link = soup.new_tag("a")
        article_link["id"] = "headlink"
        article_link["href"] = "#"
        article_link.string = "View on LiveScience"
        new_header_div.append(article_link)

        article_headline.insert_before(new_header_div)

        strapline = soup.find(class_="strapline")
        if strapline:
            strapline.name = "h3"

        bl = soup.find(class_="byline")
        if bl:
            bl.extract()

        body = soup.find(attrs={"id": "article-body"})
        for s in soup.find_all("style"):
            s.decompose()
        for s in soup.find_all("link", attrs={"rel": "preconnect"}):
            s.decompose()
        for s in soup.find_all("link", attrs={"rel": "preload"}):
            s.decompose()
        for s in soup.find_all("link", attrs={"rel": "dns-prefetch"}):
            s.decompose()
        for news in body.findAll(class_=re.compile("newsletter-form__wrapper")):
            news.decompose()
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
        for s in soup.find_all("script"):
            s.decompose()
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
