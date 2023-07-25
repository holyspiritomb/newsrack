import os
import re
import sys
from collections import OrderedDict
from calibre import browser
from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre.utils.date import utcnow, parse_date, strptime
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import format_title, BasicNewsrackRecipe

_name = "Bulletin of Applied Transgender Studies"


class Bats(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    language = 'en'
    __author__ = 'holyspiritomb'
    masthead_url = 'https://bulletin.appliedtransstudies.org/img/Wordmark-Color.png'
    use_embedded_content = False
    ignore_duplicate_articles = {"url"}
    description = '''The Bulletin of Applied Transgender Studies (BATS) is the leading venue for academic research addressing the social, cultural, and political issues facing transgender and gender minority communities across the globe. The journal offers a platinum open access forum for research of all theoretical and methodological approaches oriented toward the identification, analysis, and improvement of the material conditions of transgender life. https://bulletin.appliedtransstudies.org'''
    remove_javascript = True
    no_stylesheets = True
    keep_only_tags = [
        dict(name="article", attrs={"id": "post-content"})
    ]
    # https://bulletin.appliedtransstudies.org/img/Lockup-Color.png cover
    def parse_index(self):
        url_prefix = "https://bulletin.appliedtransstudies.org"
        idx_soup = self.index_to_soup("https://bulletin.appliedtransstudies.org")
        current_div = idx_soup.find("div", attrs={"id": "current-issue"})
        cover_img = current_div.find("img", attrs={"alt": "Cover of Current Issue"})
        cover_url = cover_img["src"]
        self.cover_url = url_prefix + cover_url
        articles = []
        for article in idx_soup.findAll("article"):
            article_header = article.find("header")
            article_link = article_header.find("a")
            article_slug = article_link["href"]
            article_auth = article.find("div", attrs={"class": "content"}).find("p")
            desc = ''
            url = url_prefix + article_slug
            title = self.tag_to_string(article_link)
            articles.append({
                'title': title,
                'url': url,
                'description': desc})
        return [('Current Issue', articles)]

    def populate_article_metadata(self, article, soup, _):
        # authors = soup.find("meta", attrs={'name': 'citation_author'})
        # article.author = authors["content"]
        # desc = soup.find("meta", attrs={'property': 'twitter:description'})
        # article.description = desc["content"]
        # article.summary = desc["content"]
        # article.text_summary = desc["content"]
        pub_dt = soup.find("dt", string=re.compile("Published"))
        pub_dd = pub_dt.next_sibling.next_sibling
        dd = self.tag_to_string(pub_dd).strip()
        if dd:
            pubdate = strptime(dd, "%B %d, %Y")
            article.date = pubdate


