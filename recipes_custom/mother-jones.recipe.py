#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import unicode_literals, division, absolute_import, print_function
import os
import sys
from collections import OrderedDict
from datetime import datetime, timezone, tzinfo
from calibre.web.feeds.news import BasicNewsRecipe
from calibre.ebooks.BeautifulSoup import BeautifulSoup
from calibre.utils.date import utcnow, parse_date

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
try:
    from recipes_shared import BasicNewsrackRecipe, WordPressNewsrackRecipe, format_title
except ImportError:
    # just for Pycharm to pick up for auto-complete
    from includes.recipes_shared import BasicNewsrackRecipe, format_title


_name = "Mother Jones"


class MotherJones(BasicNewsRecipe, BasicNewsrackRecipe):
    title = _name
    language = 'en'
    __author__ = 'holyspiritomb'
    description = '''Mother Jones is a nonprofit magazine and news outlet that delivers original award-winning reporting on the urgent issues of our day, from politics and climate change to education and the food we eat. We investigate stories that are in the public's interest. From revelatory scoops to deep-dive investigations, Mother Jones inspires 9 million monthly readers of our print, digital, and online journalism. Generated from https://www.motherjones.com/feed'''
    oldest_article = 14
    max_articles_per_feed = 200
    no_stylesheets = True
    publication_type = 'magazine'
    use_embedded_content = False
    conversion_options = {
        'tags': 'Progressive, Politics, Periodical, Mother Jones'
    }
    feeds = [
        ('Mother Jones', 'http://feeds.feedburner.com/motherjones/feed'),
    ]
    # timefmt = ' [%b %d, %Y]'
    remove_tags_before = [
        dict(attrs={"class": "entry-header"})
    ]
    remove_tags_after = [
        dict(attrs={"class": "entry-footer"})
    ]
    remove_attributes = [
        "style", "height", "width", "decoding"
    ]
    remove_tags = [
        dict(name="div", attrs={"class": "social-container"}),
        dict(name="a", attrs={"data-ga-label": "authorPhoto"}),
        dict(name="a", attrs={"data-ga-label": "authorBio"}),
        dict(name="a", attrs={"data-ga-label": "authorTwitter"}),
        dict(attrs={"class": ["mj-floating-ad-wrapper", "mj-text-cta", "newsletter-signup", "mj-article-bottom-membership-widget", "mj-article-bottom-membership-widget-mobile", "mj-house-promo-widget", "ad", "entry-footer", "byline-pipe", "author-image"]}),
        dict(attrs={"id": ["eoa-related", "eoa-recommend", "eoa-recent", "promos-container", "sidebar-right", "site-footer-promos", "custom_html-10", "site-footer"]})
    ]

    extra_css = '''
        img{max-width:95%}
    '''

    def populate_article_metadata(self, article, soup, _):
        # if (not self.pub_date) or article.utctime > self.pub_date:
            # self.pub_date = article.utctime
            # self.title = format_title(_name, article.utctime)
        headline = soup.find("h1", attrs={"class": "entry-title"})
        if headline:
            article.title = self.tag_to_string(headline)
        modified = soup.find("meta", attrs={"property": "article:modified"})
        if modified:
            modified_date = datetime.strptime(
                modified["content"], "%Y-%m-%dT%H:%M:%S%z"
            ).replace(tzinfo=timezone.utc)
            if (not self.pub_date) or modified_date > self.pub_date:
                self.pub_date = modified_date
                self.title = format_title(_name, modified_date)
        published = soup.find("meta", attrs={"property": "article:published"})
        if published:
            published_date = datetime.strptime(
                published["content"], "%Y-%m-%dT%H:%M:%S%z"
            ).replace(tzinfo=timezone.utc)
            article.utctime = published_date
            if (not self.pub_date) or published_date > self.pub_date:
                self.pub_date = published_date
                self.title = format_title(_name, published_date)
        desc = soup.find("meta", attrs={"name": "description"})
        if desc:
            article.description = desc["content"]
            article.text_summary = desc["content"]
            article.summary = desc["content"]
        # for img in soup.find_all("img"):
            # self.add_toc_thumbnail(thumbsrc)
        author = soup.find("meta", attrs={"property": "article:author"})
        if author:
            article.author = author["content"]
        # section = soup.find("meta", attrs={"property": "article:section"})

    # def get_cover_url(self):
    #     soup = self.index_to_soup('https://www.motherjones.com/magazine')
    #     coverdiv = soup.find('div', attrs={'id': 'toc_cover'})
    #     cov_url = coverdiv.find('img', src=True)['src'].split()[0]
    #     if cov_url:
    #         self.cover_url = 'https://www.motherjones.com' + cov_url
    #     return getattr(self, "cover_url", self.cover_url)

    def preprocess_raw_html(self, raw_html, url):
        soup = BeautifulSoup(raw_html)
        published = soup.find("meta", attrs={"property": "article:published"})['content']
        # jsonurl = soup.find("link", attrs={"type": "application/json", "rel": "alternate"})['href']
        # author = soup.find("meta", attrs={"property": "article:author"})
        section = soup.find("meta", attrs={"property": "article:section"})
        # if section:
            # article_section = section['content']
        datestamp = soup.find("span", attrs={"class": "dateline"})
        if datestamp:
            date_obj = datetime.strptime(
                published, "%Y-%m-%dT%H:%M:%S%z"
            )
            date_str = datetime.strftime(date_obj, "%b %d, %Y")
            datestamp.string = date_str
        header_text = soup.find("div", attrs={"id": "header-text"})
        header_image = soup.find("div", attrs={"id": "header-image"})
        if header_text and header_image:
            header_image_extracted = header_image.extract()
            header_text.insert_after(header_image_extracted)
        for img in soup.find_all("img", attrs={"srcset": True}):
            img["src"] = img["src"].partition("?")[0]
            del img["srcset"]
            del img["sizes"]
        for img in soup.find_all("img", attrs={"data-lazy-srcset": True}):
            img['src'] = img['data-lazy-srcset'].strip().split(",")[0].strip().split(" ")[0]
            # self.log.warn(img['src'])
            del img["data-lazy-srcset"]
            del img["data-lazy-src"]
            del img["data-lazy-sizes"]
            del img["loading"]
            del img["sizes"]
            del img["decoding"]
        article_body = soup.find("div", attrs={"id": "fullwidth-body"}) or soup.find("div", attrs={"itemprop": "articleBody"})
        if article_body:
            for p in article_body.find_all("p"):
                p['class'] = "article-body-text"
            div = article_body.find("div", attrs={"class": "article__block"})
            if div:
                div.unwrap()
        return str(soup)

    def postprocess_html(self, soup, __):
        # article_body = soup.find("div", attrs={"id": "fullwidth-body"}) or soup.find("div", attrs={"itemprop": "articleBody"})
        # if article_body:
        #     for p in article_body.find_all("p"):
        #         p['class'] = "article-body-text"
        #     div = article_body.find("div", attrs={"class": "article__block"})
        #     if div:
        #         div.unwrap()
        return soup


calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
# mobile_ua = 'Mozilla/5.0 (Linux; Android 11; ONEPLUS A6013) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Mobile Safari/537.36'
