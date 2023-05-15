
import os
import re
import sys
# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title
from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre.ebooks.BeautifulSoup import BeautifulSoup

_name = 'The Advocate'


class TheAdvocate(BasicNewsrackRecipe, BasicNewsRecipe):

    title = _name
    language = 'en'
    use_embedded_content = False
    recursions = 0
    remove_empty_feeds = True
    masthead_url = "https://raw.githubusercontent.com/holyspiritomb/newsrack/spiritomb/static/img/advocate.png"

    description = "Gay, lesbian, bisexual, transgender, queer news leader including politics, commentary, arts and entertainment - your source for LGBTQ news for over 50 years."
    __author__ = 'holyspiritomb'
    no_stylesheets = True
    oldest_article = 14
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
        # dict(name="div", class_="widget__shares"),
        dict(name="div", class_="ad-tag"),
        dict(name="div", class_="around-the-web"),
    ]

    extra_css = """
        .social-date-modified::before {content:'Updated: '}
        .social-date::before {content:'Published: '}
    """

    feeds = [
        ('Families', 'https://www.advocate.com/feeds/families.rss'),
        ('Trans', 'https://www.advocate.com/feeds/transgender.rss'),
        ('Bi', 'https://www.advocate.com/feeds/bisexual.rss'),
        ('Voices', 'https://www.advocate.com/feeds/voices.rss'),
        ('Arts', 'https://www.advocate.com/feeds/arts-entertainment.rss'),
        ('Religion', 'https://www.advocate.com/feeds/religion.rss'),
        ('Politics', 'https://www.advocate.com/feeds/politics.rss'),
        ('Business', 'https://www.advocate.com/feeds/business.rss'),
        ('Main', 'https://www.advocate.com/feeds/feed.rss'),
    ]

    def preprocess_html(self, soup):
        tweets = soup.find_all("blockquote", attrs={"class": "twitter-tweet"}) or soup.find_all("blockquote", attrs={"data-twitter-tweet-id": True})
        if tweets:
            for tweet in tweets:
                self.log(tweet)
                new_tweet = tweet.encode("utf-8").decode("unicode-escape")
                new_tweet_soup = BeautifulSoup(new_tweet, 'html5lib', from_encoding="unicode")
                tweet.insert_before(new_tweet_soup)
                self.log(tweet)
                self.log(new_tweet_soup)
                tweet.decompose()
            # twdiv = tweet.find("div")
                # if twdiv:
                    # twtxt = str(twdiv.string)
                    # twunescape = twtxt.encode("utf-8").decode("unicode-escape")
                    # twdiv.string = twunescape
        return soup

    def populate_article_metadata(self, article, __, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
            article.title = format_title(article.title, article.utctime)
