import os
import sys
from calibre.web.feeds.news import BasicNewsRecipe, classes
from datetime import timezone, timedelta, datetime, time

sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title
from calibre.utils.date import utcnow, parse_date
from calibre.web.feeds import Feed

_name = "Erin in the Morning"


class ErinInTheMorning(BasicNewsrackRecipe, BasicNewsRecipe):
    # most of this is borrowed from ping's lithub recipe
    title = _name
    language = 'en'
    description = u'News and discussion on trans legislation and life. https://www.erininthemorning.com/feed'
    __author__ = 'holyspiritomb'
    category = 'trans, news, rss'
    oldest_article = 31
    max_articles_per_feed = 40
    remove_empty_feeds = True
    resolve_internal_links = True
    use_embedded_content = True

    feeds = [("Posts", "https://www.erininthemorning.com/feed")]

    conversion_options = {
        'tags' : 'Blog, Trans, LGBTQ',
    }

    remove_tags = [
        dict(name="div", attrs={"class": "subscription-widget-wrap"}),
        dict(name="div", attrs={"class": "image-link-expand"}),
    ]

    remove_attributes = [
        "height", "width"
    ]

    extra_css = '''
        #article_date{font-size:0.8rem;text-transform:uppercase;}
        #article_desc{font-style:italic;font-size:1.2rem}
        p{font-size:1rem}
        .image-caption{font-size:0.8rem;font-style:italic}
        '''

    def populate_article_metadata(self, article, soup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
        date_el = soup.find(attrs={"id": "article_date"})
        datestamp = datetime.strftime(article.utctime, "%b %-d, %Y, %-I:%M %p")
        date_el.string = f"{article.author} | {datestamp}"
        desc_el = soup.find(attrs={"id": "article_desc"})
        desc_el.string = article.summary
        # article_img = soup.find("img")

    def preprocess_html(self, soup):
        headline = soup.find("h2")
        a_date = soup.new_tag("div")
        a_desc = soup.new_tag("h3")
        a_desc["id"] = "article_desc"
        a_date["id"] = "article_date"
        headline.insert_after(a_desc)
        headline.insert_after(a_date)
        return soup
