import os
import sys
import re
from datetime import datetime, timezone, tzinfo
from urllib.parse import urljoin
from calibre.web.feeds import Feed
from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre.utils.date import utcnow, parse_date
from calibre.ebooks.BeautifulSoup import BeautifulSoup

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import format_title, WordPressNewsrackRecipe

# convenience switches for when I'm developing
if "spiritomb" in os.environ["recipes_includes"]:
    _masthead = "file:///home/spiritomb/git/newsrack/recipes_custom/logos/additude.svg"
else:
    _masthead = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos/additude.svg"

_name = "ADDitude"


class ADDitude(WordPressNewsrackRecipe, BasicNewsRecipe):
    title = _name
    oldest_article = 31
    language = 'en'
    __author__ = 'holyspiritomb'
    max_articles_per_feed = 100
    masthead_url = _masthead
    # no_stylesheets = True
    # no_javascript = True
    remove_empty_feeds = True
    use_embedded_content = True
    masthead_url = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos/additude.svg"
    description = (
        '''Articles about ADHD of interest to people with ADHD.'''
    )
    feeds = [
        ("Blogs", "https://www.additudemag.com/category/blog/feed/"),
        ("Main", "https://www.additudemag.com/feed/")
    ]
    extra_css = '''
        #article_date{font-size:0.8rem;text-transform:uppercase;}
        #article_desc{font-style:italic;font-size:1.2rem}
        p{font-size:1rem}
        '''

    remove_tags = [
        dict(name="button")
    ]

    def populate_article_metadata(self, article, soup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
        date_el = soup.find(attrs={"id": "article_date"})
        datestamp = datetime.strftime(article.utctime, "%b %-d, %Y, %-I:%M %p")
        date_el.string = f"{article.author} | {datestamp}"
        desc_el = soup.find(attrs={"id": "article_desc"})
        desc_el.string = article.summary

    def preprocess_raw_html(self, raw_html, url):
        soup = BeautifulSoup(raw_html)
        imgs = soup.find_all("img")
        if imgs:
            imgreg = re.compile("^/wp-content.*")
            for img in imgs:
                src = img["src"]
                if imgreg.match(src):
                    img["src"] = f"https://additudemag.com{src}"
        return str(soup)

    def preprocess_html(self, soup):
        for p in soup.find_all("p"):
            if "SUPPORT ADDITUDE" in self.tag_to_string(p):
                p.extract()
                break
            else:
                continue
        headline = soup.find("h2")
        a_date = soup.new_tag("div")
        a_desc = soup.new_tag("h3")
        a_desc["id"] = "article_desc"
        a_date["id"] = "article_date"
        headline.insert_after(a_desc)
        headline.insert_after(a_date)
        return soup
