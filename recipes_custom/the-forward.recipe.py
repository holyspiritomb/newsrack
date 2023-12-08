import os
import re
import json
import sys
from collections import OrderedDict
from datetime import datetime, timezone

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title
from calibre.web.feeds.news import BasicNewsRecipe
from calibre.ebooks.BeautifulSoup import BeautifulSoup
from calibre.utils.date import utcnow, parse_date, strftime, strptime


# convenience switches for when I'm developing
if "spiritomb" in os.environ["recipes_includes"]:
    _masthead = "file:///home/spiritomb/git/newsrack/recipes_custom/logos/forward-masthead.svg"
else:
    _masthead = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos/forward-masthead.svg"


_name = "The Forward"


class TheForward(BasicNewsRecipe, BasicNewsrackRecipe):
    title = _name
    __author__ = 'holyspiritomb'
    description = '''The Forward is an American news media organization for a Jewish American audience. The Forward's perspective on world and national news and its reporting on the Jewish perspective on modern United States have made it one of the most influential American Jewish publications. It is published by an independent nonprofit association. It has a politically progressive editorial focus. https://forward.com/'''
    masthead_url = _masthead
    language = "en"
    encoding = "utf-8"
    ignore_duplicate_articles = {"url"}
    no_javascript = True
    no_stylesheets = True
    oldest_article = 4
    max_articles_per_feed = 50
    use_embedded_content = False
    auto_cleanup = False
    resolve_internal_links = False
    recursions = 0
    # simultaneous_downloads = 1
    publication_type = 'newspaper'
    # scale_news_images = (800, 1200)
    conversion_options = {
        'tags': 'Jewish, The Forward, Periodical, Politics, News',
        'authors' : 'newsrack',
    }

    remove_empty_feeds = True

    feeds = [
        ('News', 'https://forward.com/news/feed/'),
        ('Opinions', 'https://forward.com/opinion/feed/'),
        ('Culture', 'https://forward.com/culture/feed/'),
    ]

    remove_attributes = ["sizes", "height", "width", "style", "decoding"]

    remove_tags = [
        dict(name="div", attrs={"class": "related-articles"}),
        dict(name="div", attrs={"class": "newsletter-wrapper"}),
        dict(name="div", attrs={"class": "sponsored-content"}),
        dict(name="script", attrs={"type": "text/javascript"}),
        dict(name="script", attrs={"type": False}),
        dict(name="ul", attrs={"class": "share-post"}),
    ]
    # remove_attributes = ["style", "sizes"]
    remove_tags_before = dict(name="div", attrs={'class': 'headings'})
    remove_tags_after = dict(name='div', attrs={'class': 'ending-byline'})

    extra_css = '''
        p {
                font-size:1rem;
                }
        p.caption, p.wp-caption-text,div.caption {
                font-size:0.8rem;
                font-style: italic;
                }
        #tinyheader {
                font-size:0.7rem;
                text-transform:uppercase;
                }
        img {
                max-width:98vw;
                }

        div#author {
                font-size:0.9rem;
                margin-bottom:5px;
                }
        div.ending-byline p{
                font-size:0.9rem;
                }
    '''

    def populate_article_metadata(self, article, soup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
        article_img_div = soup.find("div", attrs={"class": "featured-image"})
        if article_img_div:
            toc_img = article_img_div.find("img")
            self.add_toc_thumbnail(article, toc_img["src"])
        end_byline = soup.find("div", attrs={"class": "ending-byline"})
        source_p = soup.new_tag("p")
        source_p["id"] = "source_link"
        source_a = soup.new_tag("a")
        source_a["href"] = article.url
        source_a.string = article.url
        source_p.append("This article was downloaded from ")
        source_p.append(source_a)
        source_p.append(".")
        end_byline.append(source_p)
        self.log.debug(article)

    def preprocess_raw_html(self, raw_html, url):
        soup = BeautifulSoup(raw_html, from_encoding='utf-8')
        article_json = soup.find("script", attrs={"type": "application/ld+json"})
        article_data = json.loads(article_json.string)
        article_info = article_data["@graph"][0]
        self.log.warn(article_info)
        pubdate = article_info["datePublished"]
        pubdate_dt = parse_date(pubdate)
        moddate = article_info["dateModified"]
        moddate_dt = parse_date(moddate)
        headings = soup.find("div", attrs={"class": "headings"})
        headline = headings.find("h1")
        headline["id"] = "headline"
        subhead = headings.find("div", attrs={"class": "heading-5"})
        if subhead:
            subhead["id"] = "subhead"
        category = headings.find("a", attrs={"class": "eyebrow"})
        if category:
            category["id"] = "article_category"
            category.extract()
        else:
            category = soup.new_tag("a")
            category["id"] = "article_category"
            category.string = article_info["articleSection"][0]
        tinyheader = soup.new_tag("div")
        tinyheader["id"] = "tinyheader"
        if category:
            tinyheader.append(category)
            tinyheader.append(" | ")
        datestamp = soup.new_tag("span")
        datestamp["id"] = "pub_date"
        datestamp["title"] = "published"
        datestamp_str = datetime.strftime(pubdate_dt, "%b %-d, %Y, %-I:%M %p")
        datestamp.string = datestamp_str
        tinyheader.append(datestamp)
        if moddate_dt != pubdate_dt:
            modstamp = soup.new_tag("span")
            modstamp["id"] = "mod_date"
            modstamp["title"] = "modified"
            modstamp_str = datetime.strftime(moddate_dt, "%b %-d, %Y, %-I:%M %p")
            modstamp.string = modstamp_str
            datestamp.insert_after(modstamp)
            datestamp.insert_after(" | updated ")
        headline.insert_before(tinyheader)
        byline_div = soup.find("div", attrs={"class": "post-author"})
        author_link = byline_div.find("a", href=re.compile("author"))
        new_byline = soup.new_tag("div")
        new_byline["id"] = "author"
        new_byline.append(author_link)
        byline_div.extract()
        if subhead:
            subhead.insert_after(new_byline)
            subhead.name = "h2"
        else:
            headline.insert_after(new_byline)
        content_container = soup.find("div", attrs={"class": "content-container"})
        for h in content_container.findAll("h2"):
            h.name = "h3"
        return str(soup)

    def preprocess_html(self, soup):
        end_byline = soup.find("div", attrs={"class": "ending-byline"})
        hr = soup.new_tag("hr")
        if end_byline:
            end_byline.insert_before(hr)
        # self.abort_recipe_processing("okay")
        # article_container = soup.find("article")
        return soup


calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
