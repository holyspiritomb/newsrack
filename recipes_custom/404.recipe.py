# https://www.404media.co/rss
import os
import sys
import re
from datetime import timezone, timedelta
from datetime import datetime as dt
from zoneinfo import ZoneInfo

sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title
from calibre.web.feeds import Feed
from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre.utils.date import datetime
# from calibre.utils.date import utcnow, parse_date
from calibre.ebooks.BeautifulSoup import BeautifulSoup


# convenience switches for when I'm developing
if "runner" in os.environ["recipes_includes"]:
    _masthead_prefix = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos"
else:
    _masthead_prefix = f"file://{os.environ['HOME']}/git/newsrack/recipes_custom/logos"
_masthead = f"{_masthead_prefix}/404.svg"
_name = "404 Media"


class FourOhFour(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    language = 'en'
    description = u'404 Media is a journalist-founded digital media company exploring the ways technology is shaping–and is shaped by–our world. https://404media.co'
    __author__ = 'holyspiritomb'
    category = 'rss'
    oldest_article = 30
    max_articles_per_feed = 50
    remove_empty_feeds = True
    resolve_internal_links = False
    use_embedded_content = False
    masthead_url = _masthead

    feeds = [("404 All", "https://www.404media.co/rss")]

    extra_css = """
        #article_source,#tiny_header,.calibre-nuked-tag-figure{
            font-size:0.8rem;
        }
        img{max-width:90vw;margin-left:auto;margin-right:auto;height:auto;}
        #tiny_header{text-transform: uppercase;}
        h1{font-size:1.75rem;}
        h2{font-size:1.5rem;}
        .post-hero__excerpt{font-style:italic;font-size:1.25rem;margin-bottom:1rem}
        .post-author,.alt-text,.calibre-nuked-tag-figcaption{font-size:0.8rem;margin-top:1em;margin-bottom:1em}
        .post-author__bio-heading{font-size:1.15rem;font-weight:bold}
        .kg-card{border-width:1px;border-color:currentColor;padding:1.5rem;margin-top:1rem;margin-bottom:1rem;border-style:solid;border-radius:1.5rem}
        .kg-card span{display:block;margin-top:1rem;margin-bottom:1rem}
        p {font-size:1rem;}
    """

    keep_only_tags = [
        dict(attrs={'class': 'post-hero'}),
        dict(name="article", attrs={'class': 'post'}),
    ]

    remove_tags = [
        classes("byline__author-image byline__date byline__details-separator post-author__image-container post-hero__ad post-author__bio-cta subscribe kg-bookmark-icon")
    ]

    def populate_article_metadata(self, article, soup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
        nyc = ZoneInfo("America/New_York")
        nyc_dt = dt.astimezone(article.utctime, nyc)
        nyc_dt_now = datetime.astimezone(datetime.now(), nyc)
        nyc_now_str = datetime.strftime(nyc_dt_now, "%b %-d, %Y at %-I:%M %p %Z")
        datestring = dt.strftime(nyc_dt, "%b %-d, %Y, %-I:%M %p %Z")

        article_date = soup.find(class_="author-byline__date")
        if article_date:
            article_date.clear()
            article_date.string = datestring

        source_link_div = soup.new_tag("div")
        source_link_div["id"] = "article_source"
        source_link = soup.new_tag("a")
        source_link["href"] = article.url
        source_link.string = article.url
        source_link_div.append("This article was downloaded from ")
        source_link_div.append(source_link)
        source_link_div.append(" at ")
        source_link_div.append(nyc_now_str)
        source_link_div.append(".")
        hr = soup.new_tag("hr")
        soup.append(hr)
        soup.append(source_link_div)
        headlink = soup.find("a", attrs={"id": "headlink"})
        if headlink:
            headlink["href"] = article.url
        hero_img = soup.find(attrs={"class": "post-hero__image"})
        if hero_img:
            toc_img = hero_img.find("img")
            if toc_img:
                self.add_toc_thumbnail(article, toc_img['src'])
        hero = soup.find(attrs={'class': 'post-hero'})
        article_headline = hero.find("h1")
        if article_headline["data-paid"]:
            article_headline.append(f" ({article_headline['data-paid']})")
            if article_headline["data-paid"] == "paid":
                article.title = f"{article.title} (paid)"

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
        # for feed in new_feeds:
        #     for article in feed.articles[:]:
        #         for word in self.filter_out:
        #             if word.upper() in article.title.upper() or word.upper() in article.summary.upper():
        #                 self.log.warn(f"\t\tremoving \"{article.title}\" from _{feed.title}_ feed (keyword: {word})")
        #                 feed.articles.remove(article)
        #                 break
        #             else:
        #                 continue
        new_feeds = [f for f in new_feeds if len(f.articles[:]) > 0]
        self.log.debug("Will download:")
        for feed in new_feeds:
            self.log.debug(f"\t{feed.title}\n")
            for article in feed.articles[:]:
                self.log.debug(f"\t\t{article.title}\n\t\t{article.url}\n\n")
        return new_feeds

    def preprocess_html(self, soup):
        byline = soup.find(class_="byline")
        byline.extract()
        kgs = soup.findAll(attrs={"class": "kg-card"})
        for kg in kgs:
            if kg.find(attrs={"class": "kg-cta-sponsor-label-wrapper"}):
                kg.decompose()
        return soup

    def preprocess_raw_html(self, raw_html, url):
        soup = BeautifulSoup(raw_html)

        new_header_div = soup.new_tag("div", attrs={"id": "tiny_header"})

        hero = soup.find(attrs={'class': 'post-hero'})
        article_headline = hero.find("h1")
        section = hero.find(attrs={"class": "post-hero__tag"})
        if section:
            new_header_div.append(section)
            new_header_div.append(" | ")

        authors = hero.findAll("a", attrs={"href": re.compile("author")})
        if authors:
            if len(authors) > 1:
                new_header_div.append(authors[0])
                for a in authors[1:]:
                    new_header_div.append(", ")
                    new_header_div.append(a)
            else:
                new_header_div.append(authors[0])
            new_header_div.append(" | ")

        article_date = soup.new_tag("span")
        article_date["class"] = "author-byline__date"
        article_date.string = "Article Date Placeholder"
        new_header_div.append(article_date)
        new_header_div.append(" | ")

        article_link = soup.new_tag("a")
        article_link["id"] = "headlink"
        article_link["href"] = "#"
        article_link.string = "View on Website"
        new_header_div.append(article_link)

        article_headline.insert_before(new_header_div)
        if soup.find("h2", string="This post is for paid members only"):
            self.log.warn("paywalled article")
            article_headline["data-paid"] = "paid"
        else:
            article_headline["data-paid"] = "free"
        # for h in soup.findAll("h2"):
        #     if h.string == "This post is for paid members only":
        #         article_headline["data-paid"] = "paid"
        #         break
        #     else:
        #         continue

        for img in soup.find_all("img", attrs={"data-srcset": True}):
            dsrcset = img["data-srcset"]
            newsrc = dsrcset.split(",")[-1].strip().split()[0]
            img["src"] = newsrc
            del img["srcset"]
            del img["data-srcset"]
            del img["data-src"]
            del img["data-sizes"]
            if img["alt"]:
                if img["alt"] != article_headline.string:
                    alttxt = soup.new_tag("div")
                    alttxt["class"] = "alt-text"
                    alttxt.string = f"Alt text: {img['alt']}"
                    img.insert_after(alttxt)
        return str(soup)
