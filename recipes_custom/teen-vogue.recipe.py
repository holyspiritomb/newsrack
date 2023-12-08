import json
import os
import re
import sys
from collections import OrderedDict
from urllib.parse import urljoin

from calibre import browser
from calibre.ebooks.BeautifulSoup import BeautifulSoup
from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre.utils.date import utcnow, parse_date, strptime


# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title

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
    oldest_article = 7
    max_articles_per_feed = 50
    use_embedded_content = False
    remove_empty_feeds = True
    ignore_duplicate_articles = {"url"}
    # remove_javascript = False
    resolve_internal_links = False
    # use_embedded_content = False
    publisher = "Conde Nast"
    masthead_url = "https://www.teenvogue.com/verso/static/teen-vogue/assets/logo.ba28e9df68104824291913727893bf4aaf22e564.svg"
    no_stylesheets = True
    filter_out = ["horoscope", "zodiac", "retrograde", "astrological", "tampon"]
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
        dict(attrs={"data-testid": ["PaywallInlineBarrierWrapper"]}),
        # classes(
        #     "related-cne-video-component tags-component callout--related-list iframe-embed podcast_storyboard"
        #     " inset-left-component ad consumer-marketing-component social-icons lead-asset__content__clip"
        #     "consumer-marketing-unit consumer-marketing-unit--article-mid-content"
        # ),
        # dict(name=["meta", "link"]),
        # dict(id=["sharing", "social", "article-tags", "sidebar"]),
        # dict(attrs={"data-testid": ["ContentHeaderRubric", "GenericCallout"]}),
    ]

    conversion_options = {
        'tags': 'Young adult, Teen Vogue, Periodical, Pop Culture, Politics',
        'authors': 'newsrack',
    }
    # feeds = [
    #     ("Teen Vogue", "https://www.teenvogue.com/feed/rss"),
    # ]
    extra_css = '''
        h1{font-size:1.75rem;}
        h2{font-size:1.5rem;}
        h3{font-size:1.25rem;}
        .caption__text,.caption__credit{font-size:0.8rem;font-style:italic;}
        .byline,.article-byline{font-size:0.8rem;}
        time{text-transform:uppercase;}
        #article-body-container > p{font-size:1rem;}
        #article-body-container > div:not(.heading-h3){font-size:0.8rem;}
        #article-body-container > div.heading-h3{font-size:1.25rem;}
        #article-body-container > div.heading-h3 > strong{font-size:1.25rem;}
    '''

    BASE_URL = "https://www.teenvogue.com"

    def _urlize(self, url_string, base_url=None):
        if url_string.startswith("//"):
            url_string = "https:" + url_string
        if url_string.startswith("/"):
            url_string = urljoin(base_url or self.BASE_URL, url_string)
        return url_string

    def preprocess_raw_html(self, raw_html, url):
        soup = BeautifulSoup(raw_html)
        p_metadata = soup.find("meta", attrs={"name": "parsely-metadata"})
        if p_metadata:
            p_json = json.loads(p_metadata["content"])
            description = p_json["description"]
            if description:
                headline = soup.find("h1", attrs={"data-testid": "ContentHeaderHed"})
                headline["data-description"] = description
        # article_title = soup.find("h1")
        # self.log.warn(f"Preprocessing raw html for: {article_title.text}")
        pub_date_meta = soup.find(
            name="meta", attrs={"property": "article:modified_time"}
        )
        post_date = strptime(pub_date_meta["content"], "%Y-%m-%dT%H:%M:%S.%fZ")
        article_age = utcnow() - post_date
        days_old = article_age.days
        if days_old > self.oldest_article:
            self.abort_article(f"Aborting article that is {days_old} days old.")
        if not self.pub_date or post_date > self.pub_date:
            self.pub_date = post_date
            self.title = format_title(_name, post_date)
        header = soup.find(
            attrs={"data-testid": "ContentHeaderHed"}
        ) or soup.find("h1")
        header.wrap(soup.new_tag("a", attrs={"data-src": url, "id": "original_link"}))
        for srcmed in soup.find_all("source", attrs={"srcset": True}):
            srcmed.decompose()
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
        for a in soup.find_all("a", attrs={"href": "https://www.teenvogue.com/newsletter/subscribe"}):
            a_cont = a.parent
            if a_cont.name == "p":
                a_cont.decompose()
        for a in soup.find_all("a", attrs={"href": "https://www.teenvogue.com/newsletter/subscribe?sourceCode=articlelink"}):
            a_cont = a.parent
            if a_cont.name == "p":
                a_cont.decompose()
        return str(soup)

    def preprocess_html(self, soup):
        # article_title = soup.find("h1")
        # self.log.warn(f"Preprocessing html for: {article_title.text}")
        byline_div = soup.find(attrs={"data-testid": "ContentHeaderAccreditation"})
        article_subtitle = byline_div.find("div")
        article_subtitle.name = "h2"
        for pic in byline_div.find_all("picture"):
            pic.decompose()
        datestamp = byline_div.find("time")
        if datestamp:
            dt_el = datestamp.extract()
            categlink = soup.find("a", class_="rubric__link")
            categlink.insert_after(dt_el)
            categlink.insert_after(": ")
        article_container = soup.new_tag("div")
        article_container["id"] = "article-body-container"
        for div in soup.find_all("div", class_="article__body"):
            for el in div.children:
                article_container.append(el)
        soup.find("div", attrs={"class": "lead-asset"}).insert_after(article_container)
        for a in soup.find_all("a", attrs={"data-event-click": True}):
            del a["data-event-click"]
            del a["rel"]
            del a["target"]
            del a["data-offer-url"]
        for aside in soup.find_all("aside"):
            # tag aside with custom css class
            aside["class"] = aside.get("class", []) + ["custom-aside"]
        for div in soup.find_all("div", class_="body__inner-container"):
            div.unwrap()
        for div in soup.find_all("div", attrs={"data-test": "aspect-ratio-container"}):
            div.unwrap()
        subhead_byline = soup.find("div", attrs={"data-testid": "ContentHeaderAccreditation"})
        byline = subhead_byline.find("div", attrs={"data-testid": "BylinesWrapper"})
        if subhead_byline and byline:
            byline["class"] = "article-byline"
            subhead_byline.append(byline.extract())
        return soup

    def postprocess_html(self, soup, first_fetch):
        for a in soup.find_all("a", attrs={"data-src": True}):
            a["href"] = a["data-src"]
            del a["data-src"]
        for div in soup.find_all("div", class_="article__body"):
            div.decompose()
        return soup

    def populate_article_metadata(self, article, soup, _):
        article_head = soup.find("div", attrs={"data-testid": "ContentHeaderContainer"})
        article_title = article_head.find("h1")
        article.title = self.tag_to_string(article_title)
        article.description = article_title["data-description"]
        article.summary = article_title["data-description"]
        article.text_summary = article_title["data-description"]
        authors = soup.find_all("a", attrs={"class": "byline__name-link"})
        article_author = self.tag_to_string(authors[0])
        if len(authors) == 2:
            article_author = self.tag_to_string(authors[0]) + " & " + self.tag_to_string(authors[1])
        article.author = article_author
        a_pub_date = soup.find("time")
        # parsed_date = parse_date(a_pub_date.text)
        if a_pub_date:
            pub_dt = strptime(a_pub_date["datetime"], "%Y-%m-%dT%H:%M:%S%z")
            article.title = format_title(article.title, pub_dt)
            article.utctime = pub_dt
            article.date = pub_dt
        article_img_div = soup.find("div", attrs={"data-testid": "ContentHeaderLeadAsset"})
        if article_img_div:
            article_img = article_img_div.find("img")
            if article_img:
                article.toc_thumbnail = article_img["src"]

    def parse_tv_index_page(self, current_url, seen):
        soup = self.index_to_soup(current_url)
        section = self.tag_to_string(soup.find("h1", attrs={'data-testid': 'SectionHeaderHed'}))
        for a in soup.find("div", attrs={"class": "multi-packages"}).findAll("a", href=True):
            url = a['href']
            if url.startswith("/story"):
                sect = a.parent.find("a", attrs={'class': 'rubric__link'})
                subsection = self.tag_to_string(sect)
                title = self.tag_to_string(a.find("h3"))
                for word in self.filter_out:
                    word_allcaps = word.upper()
                    if word_allcaps in title.upper():
                        self.log.warn(f"Skipping article that contains '{word}' in title: {title}")
                        # the next line prevents adding the article to the yield
                        seen.add(url)
                        break
                    else:
                        continue
                description = None
                summary = a.parent.find(attrs={"class": "summary-item__dek"})
                if summary:
                    description = self.tag_to_string(summary)
                if title and url not in seen:
                    seen.add(url)
                    yield {
                        "title": title,
                        "url": urljoin(self.BASE_URL, url),
                        "section": section,
                        "description": description,
                        "subsection": subsection
                    }

    def parse_index(self):
        sectioned_feeds = OrderedDict()
        articles = []
        seen = set()
        for pagenum in range(1, 2):
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
            sectioned_feeds[section].append(article)
        return sectioned_feeds.items()

    def get_browser(self, *args, **kwargs):
        return self

    def clone_browser(self, *args, **kwargs):
        return self.get_browser()

    def open_novisit(self, *args, **kwargs):
        br = browser()
        return br.open_novisit(*args, **kwargs)

    open = open_novisit


calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
