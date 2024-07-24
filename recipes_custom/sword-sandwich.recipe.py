
import os
import sys
from calibre.web.feeds.news import BasicNewsRecipe, classes
from zoneinfo import ZoneInfo

sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title
from calibre.utils.date import datetime
# from calibre.web.feeds import Feed

_name = "The Sword and thw Sandwich"


class Sword(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    language = 'en'
    description = u'This is a newsletter about the dismal state of American politics, the far right, and .... sandwiches. Plus literature, whimsy, culture, and absolutely everything else you could imagine, brought to you by the mind of Talia Lavin, an overeducated, neurotic weirdo, and her beloved editor, David Swanson. https://buttondown.email/theswordandthesandwich/'
    __author__ = 'holyspiritomb'
    category = 'blogs, news, rss'
    oldest_article = 30
    max_articles_per_feed = 40
    remove_empty_feeds = True
    resolve_internal_links = False
    use_embedded_content = False

    feeds = [("Posts", "https://buttondown.email/theswordandthesandwich/rss")]

    conversion_options = {
        'tags' : 'Blog, Politics, Food',
        'authors': 'Talia Levin',
        'publisher': 'Talia Levin'
    }

    extra_css = '''
        #meta_head{font-size:0.8rem;text-transform:uppercase;}
        #article_desc{font-style:italic;font-size:1.2rem}
        div > img + div{font-size:0.8rem;padding-top:1rem;padding-bottom:1rem}
        p{font-size:1rem}
        #article_source{font-size:0.8rem;}
        '''

    remove_tags_before = [
        dict(class_="email-body-content")
    ]

    remove_tags = [
        classes("epilogue footer"),
        dict(name="date"),
        dict(name="form"),
    ]

    def populate_article_metadata(self, article, soup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
        nyc = ZoneInfo("America/New_York")
        nyc_dt = datetime.astimezone(datetime.now(), nyc)
        nyc_now_str = datetime.strftime(nyc_dt, "%b %-d, %Y at %-I:%M %p %Z")
        meta_head = soup.new_tag("div")
        meta_head["id"] = "meta_head"
        date_el = soup.new_tag("span")
        nyc_article_dt = datetime.astimezone(article.utctime, nyc)
        datestamp = datetime.strftime(nyc_article_dt, "%b %-d, %Y, %-I:%M %p %Z")
        headlink = soup.new_tag("a")
        headlink["href"] = article.url
        headlink.string = "Source"
        date_el.string = f"{article.author} | {datestamp} | "
        date_el.append(headlink)
        meta_head.append(date_el)
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
        headline = soup.find("h1")
        headline.insert_before(meta_head)
