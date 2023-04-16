import os
import re
import sys
from collections import OrderedDict
from urllib.parse import urlparse
from urllib.parse import urljoin
from datetime import datetime
from calibre import browser
from calibre.ebooks.BeautifulSoup import BeautifulSoup
from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre.utils.date import utcnow, parse_date


# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
try:
    from recipes_shared import BasicNewsrackRecipe, format_title
except ImportError:
    # just for Pycharm to pick up for auto-complete
    from includes.recipes_shared import BasicNewsrackRecipe, format_title

# heavily based on the recipe for wired

_name = "Teen Vogue"


class TeenVogue(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    __author__ = "holyspiritomb"
    description = (
        '''Teen magazine about fashion, culture, politics. https://www.teenvogue.com/'''
    )
    publication_type = 'magazine'
    language = "en"

    oldest_article = 14
    max_articles_per_feed = 50

    use_embedded_content = False
    remove_empty_feeds = True
    ignore_duplicate_articles = {"url"}
    # remove_javascript = True
    resolve_internal_links = False
    # use_embedded_content = False
    publisher = "Conde Nast"
    masthead_url = "https://www.teenvogue.com/verso/static/teen-vogue/assets/logo.ba28e9df68104824291913727893bf4aaf22e564.svg"
    no_stylesheets = True
    keep_only_tags = [
        classes("article__content-header content-header lead-asset article__body"),
        dict(name="div", attrs={"data-testid": "BodyWrapper"}),
        dict(name="figure", attrs={"class": "asset-embed"}),
        dict(name="h1", attrs={"data-testid": "ContentHeaderHed"}),
        dict(name="div", attrs={"data-testid": "ContentHeaderAccreditation"}),
        dict(name="time", attrs={"data-testid": "ContentHeaderPublishDate"}),
    ]
    # remove_tags_before = [
        # dict(name="div",attrs={"data-testid": "ContentHeaderTitleBlockWrapper"})
    # ]
    remove_tags = [
        classes("body__inline-barrier social-icons persistent-aside ad"),
        dict(attrs={"aria-hidden": "true"}),
        dict(attrs={"data-testid": ["PaywallInlineBarrierWrapper"]})
    #     classes(
    #         "related-cne-video-component tags-component callout--related-list iframe-embed podcast_storyboard"
    #         " inset-left-component ad consumer-marketing-component social-icons lead-asset__content__clip"
    #         "consumer-marketing-unit consumer-marketing-unit--article-mid-content"
    #     ),
    #     dict(name=["meta", "link"]),
    #     dict(id=["sharing", "social", "article-tags", "sidebar"]),
    #     dict(attrs={"data-testid": ["ContentHeaderRubric", "GenericCallout"]}),
    ]



    conversion_options = {
        'tags' : 'Young adult, Teen Vogue, Periodical, Pop Culture, Politics',
        'authors' : 'newsrack',
    }
    # feeds = [
    #     ("Teen Vogue", "https://www.teenvogue.com/feed/rss"),
    # ]

    BASE_URL = "https://www.teenvogue.com"

    def _urlize(self, url_string, base_url=None):
        if url_string.startswith("//"):
            url_string = "https:" + url_string
        if url_string.startswith("/"):
            url_string = urljoin(base_url or self.BASE_URL, url_string)
        return url_string

    def preprocess_raw_html(self, raw_html, url):
        self.log.warn("preprocess_raw_html: is this is where i figure out how to abort processing of articles that are too old?")
        soup = BeautifulSoup(raw_html)
        pub_date_meta = soup.find(
            name="meta", attrs={"property": "article:modified_time"}
        )
        post_date = datetime.strptime(pub_date_meta["content"], "%Y-%m-%dT%H:%M:%S.%fZ")
        article_age = datetime.utcnow() - post_date
        days_old = article_age.days
        self.log(f"article at {url} is {days_old} days old")
        if days_old > self.oldest_article:
            self.log.warn("this article is older than we want")
            self.abort_article("aborted article")
        if not self.pub_date or post_date > self.pub_date:
            self.pub_date = post_date
            self.title = format_title(_name, post_date)
        # authors = [b.text for b in soup.find_all(attrs={"class": "byline__name-link"})]
        # category = soup.find("a", attrs={'class': 'rubric__link'}).text
        # authors_div = soup.new_tag("div", attrs={"class": "author"})
        # authors_div.append(", ".join(authors))
        # category_div = soup.new_tag("div", attrs={"class": "category"})
        # category_div.append(category)
        # article_original_link = soup.new_tag("a", attrs={"href":url, "id": "sourcelink"})
        # pub_div = soup.new_tag("div", attrs={"class": "published-dt"})
        # pub_div.append(f"{post_date:%B %d, %Y %H:%H %p}")
        # meta_div = soup.new_tag("div", attrs={"class": "article-meta"})
        # meta_div.append(article_original_link)
        # meta_div.append(pub_div)
        header = soup.find(
            attrs={"data-testid": "ContentHeaderHed"}
        ) or soup.find("h1")
        header.wrap(soup.new_tag("a", attrs={"data-src": url,"id": "original_link"}))
        # header.insert_after(meta_div)
        # soup.find("h1").insert_before(category_div)
        return str(soup)

    def postprocess_html(self, soup, first_fetch):
        for a in soup.find_all("a", attrs={"data-src": True}):
            a["href"] = a["data-src"]
            del a["data-src"]
        return soup

    def preprocess_html(self, soup):
        for a in soup.find_all("a", attrs={"data-event-click": True}):
            del a["data-event-click"]
            del a["rel"]
            del a["target"]
            del a["data-offer-url"]
        for img in soup.find_all("img", attrs={"srcset": True}):
            img["src"] = self._urlize(
                img["srcset"].strip().split(",")[-1].strip().split(" ")[0]
            )
            del img["srcset"]
        for srcmedia in soup.find_all("source", attrs={"srcset": True, "media": "(max-width: 767px)"}):
            headerimgsrc = self._urlize(
                srcmedia["srcset"].strip().split(",")[-1].strip().split(" ")[0]
            )
            srcmedia.insert_before(soup.new_tag(name="img", attrs={"src": headerimgsrc, "class": "article-picture"}))
        for srcmed in soup.find_all("source", attrs={"srcset": True}):
            srcmed.decompose()
        for articlepicture in soup.find_all("img", class_="article-picture"):
            articlepicture.wrap(soup.new_tag("div"))
        for picture in soup.find_all("picture"):
            # take <img> tag out of <noscript> into <picture>
            noscript = picture.find(name="noscript")
            if not noscript:
                continue
            img = noscript.find(name="img")
            if not img:
                continue
            picture.append(img.extract())
            noscript.decompose()
        for aside in soup.find_all("aside"):
            # tag aside with custom css class
            aside["class"] = aside.get("class", []) + ["custom-aside"]
        for div in soup.find_all("div", class_="body__inner-container"):
            div.unwrap()
        for div in soup.find_all("div", attrs={"data-test": "aspect-ratio-container"}):
            div.unwrap()
        return soup

    def parse_tv_index_page(self, current_url, seen):
        self.log("running parse_tv_index function on", current_url)
        soup = self.index_to_soup(current_url)
        section = self.tag_to_string(soup.find("h1", attrs={'data-testid': 'SectionHeaderHed'}))
        for a in soup.find("div", attrs={"class": "multi-packages"}).findAll("a", href=True):
            url = a['href']
            if url.startswith("/story"):
                self.log(url)
                sect = a.parent.find("a", attrs={'class': 'rubric__link'})
                subsection = self.tag_to_string(sect)
                self.log(f"{section} > {subsection}")
                title = self.tag_to_string(a.find("h3"))
                self.log(title)
                description = None
                summary = a.parent.find(attrs={"class": "summary-item__dek"})
                if summary:
                    description = self.tag_to_string(summary)
                    self.log(description)
                if title and url not in seen:
                    seen.add(url)
                    self.log("Found article:", section, title)
                    yield {
                        "title": title,
                        "url": urljoin(self.BASE_URL, url),
                        "description": description,
                        "section": section,
                        "subsection": subsection,
                    }

    def parse_index(self):
        self.log("running parse_index function")
        sectioned_feeds = OrderedDict()
        articles = []
        seen = set()
        for pagenum in range(1, 4):
            articles.extend(
                self.parse_tv_index_page(
                    f"{self.BASE_URL}/news-politics?page={pagenum}", seen
                )
            )
        for pagenum in range(1, 2):
            articles.extend(
                self.parse_tv_index_page(
                    f"{self.BASE_URL}/entertainment?page={pagenum}", seen
                )
            )
            articles.extend(
                self.parse_tv_index_page(
                    f"{self.BASE_URL}/wellness/health?page={pagenum}", seen
                )
            )
            articles.extend(
                self.parse_tv_index_page(
                    f"{self.BASE_URL}/wellness/mental-health?page={pagenum}", seen
                )
            )
            articles.extend(
                self.parse_tv_index_page(
                    f"{self.BASE_URL}/wellness/sexual-health-identity?page={pagenum}", seen
                )
            )
            articles.extend(
                self.parse_tv_index_page(
                    f"{self.BASE_URL}/wellness/voices?page={pagenum}", seen
                )
            )
            articles.extend(
                self.parse_tv_index_page(
                    f"{self.BASE_URL}/wellness?page={pagenum}", seen
                )
            )
        for article in articles:
            section = article["section"]
            if section not in sectioned_feeds:
                sectioned_feeds[section] = []
                self.log("Added section:", section)
            sectioned_feeds[section].append(article)
        # booksoup = self.index_to_soup("https://www.teenvogue.com/entertainment/books")
        # healthsoup = self.index_to_soup("https://www.teenvogue.com/wellness/health")
        # wellness_soup = self.index_to_soup("https://www.teenvogue.com/wellness/mental-health")
        # voices = self.index_to_soup("https://www.teenvogue.com/wellness/voices")
        return sectioned_feeds.items()
        # return [(_name, articles)]

    def get_browser(self, *args, **kwargs):
        return self

    def clone_browser(self, *args, **kwargs):
        return self.get_browser()

    def open_novisit(self, *args, **kwargs):
        br = browser()
        return br.open_novisit(*args, **kwargs)

    open = open_novisit
