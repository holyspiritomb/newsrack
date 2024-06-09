import os
import sys
from datetime import date, datetime
from zoneinfo import ZoneInfo

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title
from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre.ebooks.BeautifulSoup import BeautifulSoup
from calibre.utils.date import utcnow, parse_date, strftime, strptime


# convenience switches for when I'm developing~
if "runner" in os.environ["recipes_includes"]:
    _masthead_prefix = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos"
else:
    _masthead_prefix = f"file://{os.environ['HOME']}/git/newsrack/recipes_custom/logos"
_masthead = f"{_masthead_prefix}/972-logo.svg"

_name = "+972 Mag"


class NineSevenTwoMag(BasicNewsRecipe, BasicNewsrackRecipe):
    title = _name
    __author__ = 'holyspiritomb'
    description = '''Independent journalism from Israel-Palestine.'''
    masthead_url = _masthead
    language = "en"
    encoding = "utf-8"
    ignore_duplicate_articles = {"url"}
    no_javascript = True
    no_stylesheets = True
    oldest_article = 14
    max_articles_per_feed = 50
    use_embedded_content = False
    auto_cleanup = False
    resolve_internal_links = False
    scale_news_images_to_device = True
    recursions = 0
    # simultaneous_downloads = 1
    publication_type = 'newspaper'
    # scale_news_images = (800, 1200)
    conversion_options = {
        'tags': 'Jewish, 972mag, Periodical, Politics, News',
        'authors' : 'newsrack',
    }

    remove_empty_feeds = True

    feeds = [
        ('News', 'https://972mag.com/feed/'),
    ]

    keep_only_tags = [
        dict(attrs={"class": "is-article"})
    ]

    remove_tags = [
        classes("read-more-module donation-module move-newsletter social-column-module writer-thumbnail editlink related-items avatar")
    ]

    remove_attributes = ["height", "width", "decoding", "data-fb_share", "data-tw_share", "data-image_height", "data-image_width", "data-mailto", "data-article_url_http", "data-next_article_id", "data-article_title_full", "style", "data-path", "data-image_url", "loading"]

    extra_css = '''
    p{font-size:1em;}
    p img, div img{max-width:98vw}
    .article-meta,.byline{font-size:0.8em;}
    .wp-caption-text,.caption{font-size:0.8em;}
    .partnership-logo{max-width:50vw;}
    .tags span{padding-right:5px;}
    .byline,.date{text-transform:uppercase}
    '''

    def populate_article_metadata(self, article, soup: BeautifulSoup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
        headimg = soup.find("img", class_="wp-post-image")
        if headimg:
            self.add_toc_thumbnail(article, headimg["src"])
        nyc = ZoneInfo("America/New_York")
        nyc_dt = datetime.astimezone(datetime.now(), nyc)
        nyc_article_dt = datetime.astimezone(article.utctime, nyc)
        datestring = datetime.strftime(nyc_article_dt, "%b %-d, %Y, %-I:%M %p %Z")
        byline = soup.find(class_="byline")
        byline.append(" || ")
        byline_src = soup.new_tag("a")
        byline_src.append("Source")
        byline_src["href"] = article.url
        byline.append(byline_src)
        byline_date_el = byline.find(class_="date")
        byline_date_el.string = f"|| {datestring}"
        source_div = soup.new_tag("div")
        source_div["id"] = "downloaded_from"
        article_link = soup.new_tag("a")
        article_link["href"] = article.url
        article_link.string = article.url
        current_dt_str = date.strftime(nyc_dt, "%-d %B %Y, %-I:%M %p %Z")
        source_div.append("This article was downloaded from ")
        source_div.append(article_link)
        source_div.append(f" at {current_dt_str}.")
        hr = soup.new_tag("hr")
        article_meta = soup.find(class_="article-meta")
        article_meta.append(hr)
        article_meta.append(source_div)

    def preprocess_html(self, soup: BeautifulSoup):
        sticky = soup.find(class_="sticky-wrapper")
        sticky.unwrap()
        imglinks = soup.findAll("a", class_="lightbox-link")
        for a in imglinks:
            a.unwrap()
        byline = soup.find(class_="byline")
        prefix = byline.find(class_="prefix")
        prefix.extract()
        headline = soup.find("h1")
        hr = soup.new_tag("hr")
        headline.insert_before(byline)
        headline.insert_before(hr)
        article_meta = soup.find(class_="article-meta")
        hr = soup.new_tag("hr")
        author_meta = article_meta.find(class_="author-meta")
        social_auth = author_meta.find(class_="social")
        if social_auth:
            social_auth.extract()
        tags = article_meta.find(class_="tags")
        first_tag = tags.find("li")
        first_tag.insert_before("Tags: ")
        for li in tags.findAll("li"):
            li.insert_after(" ")
            li.name = "span"
            li["class"] = "article_tag"
        tags.find("ul").unwrap()
        author_meta.insert_after(tags)
        author_meta.insert_after(hr)
        hr = soup.new_tag("hr")
        article_meta.insert_before(hr)
        return soup


calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
