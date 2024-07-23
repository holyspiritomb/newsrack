import os
import re
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title
from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre.ebooks.BeautifulSoup import BeautifulSoup


# convenience switches for when I'm developing
if "runner" in os.environ["recipes_includes"]:
    _masthead_prefix = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos"
else:
    _masthead_prefix = f"file://{os.environ['HOME']}/git/newsrack/recipes_custom/logos"
_masthead = f"{_masthead_prefix}/advocate.svg"

_name = 'The Advocate'


class TheAdvocate(BasicNewsrackRecipe, BasicNewsRecipe):

    title = _name
    language = 'en'
    use_embedded_content = False
    recursions = 0
    remove_empty_feeds = True
    masthead_url = _masthead
    description = "Gay, lesbian, bisexual, transgender, queer news leader including politics, commentary, arts and entertainment - your source for LGBTQ news for over 50 years."
    __author__ = 'holyspiritomb'
    no_stylesheets = True
    oldest_article = 1
    # remove_javascript = False
    remove_attributes = [
        "style", "height", "width"
    ]

    # keep_only_tags = [
    #     dict(name="h1", class_="rich-text-headline"),
    #     dict(name="div", class_="widget__body"),
    #     dict(name="div", class_="body-description"),
    # ]
    remove_tags_after = [
        dict(name="div", class_="around-the-web"),
    ]
    remove_tags_before = [
        dict(name="h1", class_="widget__headline"),
    ]
    remove_tags = [
        dict(name="div", class_="custom-field-show-as-updated"),
        classes("recirculation-container latest-news-wrap author__modal footer__bottom-wrapper"),
        dict(class_="newsletter-container"),
        dict(class_="sidebar-video"),
        dict(class_="partners_wrapper"),
        dict(class_="magazine__banner"),
        dict(class_="social__links"),
        dict(name="div", class_="ad-tag"),
        dict(name="div", class_="around-the-web"),
        dict(name="a", string="Yahoo Feed")
    ]

    extra_css = """
        .social-date-modified::before {content:'Updated: '}
        .social-date::before {content:'Published: '}
        #article_source, #meta_head{font-size:0.8rem;}
        #meta_head, #meta_head > a{text-transform:uppercase;}
        div.tags{display:list}
        div.tags::before{content:"Tags:"; display:block;font-size:big; padding-top:1em;}
        div.tags .tags__item{display:list-item}
        div.tags .tags__item::before{content:"• "; text-decoration:none;}
    """

    feeds = [
        ('Politics', 'https://www.advocate.com/feeds/politics.rss'),
        ('Families', 'https://www.advocate.com/feeds/families.rss'),
        ('Trans', 'https://www.advocate.com/feeds/transgender.rss'),
        ('Bi', 'https://www.advocate.com/feeds/bisexual.rss'),
        ('Voices', 'https://www.advocate.com/feeds/voices.rss'),
        ('Arts', 'https://www.advocate.com/feeds/arts-entertainment.rss'),
        ('Religion', 'https://www.advocate.com/feeds/religion.rss'),
        ('Business', 'https://www.advocate.com/feeds/business.rss'),
        ('Main', 'https://www.advocate.com/feeds/feed.rss'),
    ]

    def preprocess_html(self, soup):
        tweets = soup.find_all("blockquote", attrs={"class": "twitter-tweet"}) or soup.find_all("blockquote", attrs={"data-twitter-tweet-id": True})
        if tweets:
            for tweet in tweets:
                tweet_link = tweet.find("a")
                tweet_url = tweet_link["href"]
                tw_user = tweet_url.split("/")[3]
                tweet_link.append("Link to Tweet by ")
                tweet_link.append(tw_user)
        # categories = soup.find(_class="all-related-sections")
        # if categories:
        #     self.log(categories)
        return soup

    def populate_article_metadata(self, article, soup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
            article.title = format_title(article.title, article.utctime)
        nyc = ZoneInfo("America/New_York")
        nyc_dt_now = datetime.astimezone(datetime.now(), nyc)
        nyc_dt = datetime.astimezone(article.utctime, nyc)
        curr_datestring = datetime.strftime(nyc_dt_now, "%b %-d, %Y at %-I:%M %p %Z")
        article_datestr = datetime.strftime(nyc_dt, "%b %-d, %Y at %-I:%M %p %Z")
        source_link_div = soup.new_tag("div")
        source_link_div["id"] = "article_source"
        source_link = soup.new_tag("a")
        source_link["href"] = article.url
        source_link.string = article.url
        source_link_div.append("This article was downloaded from ")
        source_link_div.append(source_link)
        source_link_div.append(" on ")
        source_link_div.append(curr_datestring)
        source_link_div.append(".")
        hr = soup.new_tag("hr")
        soup.append(hr)
        soup.append(source_link_div)
        header_soup = soup.new_tag("div")
        header_soup["id"] = "meta_head"
        section_raw = source_link["href"].split("/")[3]
        section = section_raw.split("-")[0]
        header_soup.append(section)
        header_soup.append(" | ")
        header_soup.append(article_datestr)
        header_soup.append(" | ")
        header_link = soup.new_tag("a")
        header_link["href"] = article.url
        header_link.append("View on Website")
        header_soup.append(header_link)
        headline = soup.find("h1")
        headline.insert_before(header_soup)
