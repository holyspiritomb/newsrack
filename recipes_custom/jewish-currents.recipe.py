import os
import json
import sys
import re
from collections import OrderedDict
from datetime import date, datetime
from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre.utils.date import utcnow, parse_date
from calibre import browser

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title


_name = "Jewish Currents"


class JewishCurrents(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    __author__ = "holyspiritomb"
    language = "en"
    oldest_article = 31  # days
    # max_articles_per_feed = 50
    publication_type = 'magazine'
    resolve_internal_links = False
    # use_embedded_content = False
    remove_empty_feeds = True
    remove_javascript = False
    # max_articles_per_feed = 50
    no_stylesheets = True
    remove_attributes = ["style"]
    # recursions = 1
    masthead_url = "https://jewishcurrents.org/img/jewish-currents.svg"
    description = (
        '''Breaking news, analysis, art, and culture from a progressive Jewish perspective.'''
    )
    conversion_options = {
        'tags' : 'Jewish Currents, Jewish',
        'authors' : 'newsrack',
    }
    # feeds = [
        # ("Duolingo Blog", "https://blog.duolingo.com/rss/"),
    # ]

    # keep_only_tags = [
        # dict(name="div", attrs={"id": "content"})
    # ]

    remove_tags_before = [
        dict(name="div", attrs={"id": "content"})
    ]

    # remove_tags_after = [
    #     dict(name="div", attrs={"class": "bioblock"})
    # ]
    remove_tags = [
        dict(name="div", attrs={"id": "letters"}),
        dict(name="div", attrs={"class": "footblurb"}),
        dict(name="div", attrs={"class": "social"}),
        dict(attrs={"class": "hidden"}),
        dict(name="svg", attrs={"height": False}),
        dict(name="script", attrs={"type": False}),
        dict(name="script", attrs={"src": True}),
        dict(name="iframe"),
        dict(name="footer"),
    ]

    extra_css = '''
        * {
            font-family: Lato, "Readex Pro Light", sans-serif;
        }
        img {
            max-width: 100%;
            height: auto;
        }

        #article_headline {}

        .image-caption p {
            font-size: 0.8rem;
        }
        .image-credit {
            font-size: 0.7rem;
        }

        .bodytext p:not(.pullquote) {
            font-size: 1rem;
        }

        p.pullquote {
            font-size: 1.3rem;
            font-family: serif;
            font-style: italic;
            font-weight: bold;
            text-align: center;
            padding-left: 10vw;
            padding-right: 10vw;
        }

        .bioblock p, .bioblock span {
            font-size: 0.8rem;
        }

        #category_date {
            font-size:0.8rem;
            text-transform: uppercase;
        }
        '''

    BASE_URL = 'https://jewishcurrents.org'

    def populate_article_metadata(self, article, soup, _):
        # self.log.warn(soup)
        toc_thumb = soup.find("img", attrs={"id": "toc_thumb"})
        thumb_src = toc_thumb["src"]
        self.add_toc_thumbnail(article, thumb_src)
        json_info = soup.find("script", attrs={"type": "application/ld+json"})
        json_data = json_info.string
        article_data = json.loads(json_data)
        # self.log.warn(article_data["@graph"])
        article_pubdate_str = article_data["@graph"][0]["datePublished"]
        article_mod_str = article_data["@graph"][0]["dateModified"]
        if article_pubdate_str == article_mod_str:
            article_dt = parse_date(article_pubdate_str)
        else:
            article_dt = parse_date(article_mod_str)
        date_el = soup.find(attrs={"id": "article_date"})
        if date_el:
            date_el["href"] = article.url
            date_local = datetime.strptime(article_pubdate_str, "%Y-%m-%dT%H:%M:%S%z")
            self.log(article_pubdate_str, date_local)
            self.log(date_local.tzinfo)
            date_el.string = date.strftime(date_local, "%d %B %Y, %-I:%M %p %Z")
        article.utctime = article_dt
        article.date = article_dt
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)

    def preprocess_html(self, soup):
        content = soup.find("div", attrs={"id": "content"})
        lockup = content.find("div", attrs={"class": "lockup"})
        if lockup:
            head_authors = lockup.findAll("a", href=re.compile("author"))
            date_el = lockup.find("div", string=re.compile(r"[0-9]{4}$"))
            if date_el:
                self.log(date_el)
                date_el["id"] = "article_date"
                date_el.name = "a"
                date_el.extract()
            for auth in head_authors:
                auth["class"] = "header-author"
            headline = lockup.find("h1")
            headline["id"] = "article_headline"
            subhead = lockup.find("h2")
            if subhead:
                subhead["id"] = "article_subhead"
            category_link = lockup.find("a", href=re.compile("category"))
            category_link["id"] = "article_category"
            if category_link.string != "Comic / ":
                tinyheader = soup.new_tag("div")
                tinyheader["id"] = "category_date"
                category_link.wrap(tinyheader)
                category_link.insert_after(date_el)
                category_link.insert_after(" | ")
        toc_thumb = content.find("img")
        toc_thumb["id"] = "toc_thumb"
        imgcap = toc_thumb.find_next_sibling("div", class_="text-sm")
        if imgcap:
            imgcap["class"] = "image-caption"
        imgcred = toc_thumb.find_next_sibling("div", class_="text-xs")
        if imgcred:
            imgcred["class"] = "image-credit"
        for img in content.findAll("img", attrs={"height": True}):
            del img["height"]
            del img["width"]
        img_auth = content.findAll("img", attrs={"data-srcset": True})
        for img in img_auth:
            if "/imager/cloud/authors" in img["data-srcset"]:
                img.extract()
        bioblocks = soup.findAll(attrs={"class": "bioblock"})
        if bioblocks:
            for bioblock in bioblocks:
                # author_names = bioblock.findAll("a", href=re.compile("author"))
                twitter_handles = bioblock.findAll("a", href=re.compile("twitter"))
                if twitter_handles:
                    for tw in twitter_handles:
                        br = soup.new_tag("br")
                        tw.insert_after(br)
        article_main = content.find("main")
        if article_main:
            hr = soup.new_tag("hr")
            article_main.insert_after(hr)
        pullquotes = content.findAll(class_="pullquote")
        for pq in pullquotes:
            pull_par = pq.find("p")
            if pull_par:
                pull_par["class"] = "pullquote"
                pull_par.parent.unwrap()
        # self.log.warn(content)
        return soup

    def parse_index(self):
        # self.log("running parse_index function")
        soup = self.index_to_soup("https://jewishcurrents.org/archive")
        sectioned_feeds = OrderedDict()
        for article_card in soup.findAll("a", attrs={'class': 'leading-snug'}):
            card_url = article_card['href']
            card_title = self.tag_to_string(article_card.find("div", attrs={'class': 'font-display'}))
            section_title = self.tag_to_string(article_card.find("span", attrs={'class': 'pr-3'}))
            if section_title not in sectioned_feeds:
                sectioned_feeds[section_title] = []
            description = self.tag_to_string(article_card.find("div", attrs={"class": "font-sans"}))
            block = article_card.find("span", attrs={'class': 'block'})
            auths = block.contents[0].strip()
            article_date_span = self.tag_to_string(block.find("span"))
            article_date = datetime.strptime(article_date_span, "%B %d, %Y")
            # self.log(f"Found article: {section_title}, {card_title}")
            sectioned_feeds[section_title].append(
                {
                    "title": card_title,
                    "url": card_url,
                    "description": description,
                    "date": article_date_span,
                    "author": auths,
                }
            )
        return sectioned_feeds.items()

    def get_browser(self, *a, **kw):
        # kw[
        #     "user_agent"
        # ] = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        br = BasicNewsRecipe.get_browser(self, *a, **kw)
        return br

    def clone_browser(self, *args, **kwargs):
        return self.get_browser()

    def open_novisit(self, *args, **kwargs):
        br = browser()
        return br.open_novisit(*args, **kwargs)

    open = open_novisit
