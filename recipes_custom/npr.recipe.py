import os
import sys
from datetime import datetime, timezone, tzinfo
from urllib.parse import urljoin
from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre.utils.date import utcnow, parse_date
from calibre.ebooks.BeautifulSoup import BeautifulSoup


# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
try:
    from recipes_shared import BasicNewsrackRecipe, format_title
except ImportError:
    # just for Pycharm to pick up for auto-complete
    from includes.recipes_shared import BasicNewsrackRecipe, format_title

_name = "National Public Radio"


class NPR(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    oldest_article = 3
    language = 'en'
    __author__ = 'holyspiritomb'
    max_articles_per_feed = 100
    no_stylesheets = True
    no_javascript = True
    remove_empty_feeds = True
    use_embedded_content = False
    publication_type = 'newspaper'
    # simultaneous_downloads = 1
    masthead_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d7/National_Public_Radio_logo.svg/1024px-National_Public_Radio_logo.svg.png"
    auto_cleanuo = True
    description = (
        '''National Public Radio is an American nonprofit media organization that serves as a national syndicator to a network of over 1,000 public radio stations in the United States.'''
    )
    # remove_attributes = ["style", "sizes"]
    # remove_tags_before = dict(name="section", attrs={'id': 'main-section'})
    # remove_tags_after = dict(name='div', attrs={'id': 'storytext'})
    # remove_tags = [
    #     dict(name='source', attrs={'data-format': 'webp'}),
    #     dict(name='source', attrs={'type': 'image/webp'}),
    #     dict(name='body', attrs={'id': 'blog'}),
    #     dict(name='input', attrs={'type': 'hidden'}),
    #     dict(name='div', attrs={'class': 'enlarge_measure'}),
    #     dict(name='div', attrs={'class': 'enlarge-options'}),
    #     dict(name='div', attrs={'id': 'primaryaudio'}),
    #     # dict(name='div', attrs={'aria-label': 'advertisement'}),
    #     # dict(name='div', attrs={'class': 'ad-config'}),
    #     dict(name='div', attrs={'class': 'enlarge_html'}),
    #     dict(name='div', attrs={'class': 'bucketwrap primary'}),
    #     dict(name='div', attrs={'class': 'bucketwrap'}),
    #     classes("hide-caption toggle-caption")
    # ]
    # BASE_TEXTONLY = "https://text.npr.org"
    # BASE_RICH = "https://npr.org"
    feeds = [
        (u'National', u'http://www.npr.org/rss/rss.php?id=1003'),
        (u'World', u'http://www.npr.org/rss/rss.php?id=1004'),
        # (u'National', u'https://feeds.npr.org/1003/rss.xml'),
        # ('World', 'https://feeds.npr.org/1004/rss.xml'),
        ('Climate', 'https://feeds.npr.org/1167/rss.xml'),
        ('Health', 'https://feeds.npr.org/1128/rss.xml'),
        ('Science', 'https://feeds.npr.org/1007/rss.xml'),
        ('Race', 'https://feeds.npr.org/1015/rss.xml'),
        ('Law', 'https://feeds.npr.org/1070/rss.xml'),
        ('Space', 'https://feeds.npr.org/1026/rss.xml'),
        ('Religion', 'https://feeds.npr.org/1016/rss.xml'),
        # (u'All', u'http://www.npr.org/rss/rss.php?id=1001'),
        ('Art and Design', 'https://feeds.npr.org/1047/rss.xml'),
    ]

    # def parse_index(self):
    #     soup = self.index_to_soup("https://text.npr.org/")
    #     ans = {}
    #     articles = {}
    #     for a in soup.find_all("a", attrs={"class": "topic-title"}):
    #         article_url = "https://text.npr.org" + a['href']
    #         article_title = self.tag_to_string(a)
    #         section = self.tag_to_string(soup.find("p", attrs={"class": "topic-date"}))
    #         articles = ans.setdefault(section, [])
    #         articles.append({'title': article_title, 'url': article_url})
    #     return list(ans.items())

    def populate_article_metadata(self, article, soup, _):
        article_dt_el = soup.find("time")
        if article_dt_el:
            # 2023-04-21T05:10:22-04:00
            article.date = datetime.strptime(article_dt_el['datetime'], "%Y-%m-%dT%H:%M:%S%z")
            article.title = format_title(article.title, article.date)
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)

    def get_article_url(self, article):
        self.log.warn(article.link)
        article_rich_url = article.link
        article_id = article_rich_url.split('/')[-2]
        article_textonly_url = f"https://text.npr.org/{article_id}"
        self.log(article_textonly_url)
        return article_textonly_url

    def preprocess_html(self, soup):
        tier = soup.find("meta", attrs={"property": "article:content_tier"})
        if tier:
            if tier['content'] != "free":
                self.abort_article("Article isn't free.")
        sect = soup.find("h3", attrs={"class": "slug"})
        if sect:
            sect_str = self.tag_to_string(sect.a)
            if sect_str == "Sports":
                self.abort_article("Sports article aborted.")
        # notrans = soup.find("body", attrs={"class": "no-transcript"})
        # if notrans:
            # self.abort_article("Aborting article with no transcript.")
        return soup


calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
