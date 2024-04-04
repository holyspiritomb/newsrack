import os
import sys
from calibre.web.feeds.news import BasicNewsRecipe, classes
from datetime import datetime
from zoneinfo import ZoneInfo

sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title
# from calibre.utils.date import utcnow, parse_date
# from calibre.web.feeds import Feed
# from calibre.ebooks.BeautifulSoup import BeautifulSoup

# convenience switches for when I'm developing
if "runner" in os.environ["recipes_includes"]:
    _masthead_prefix = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos"
else:
    _masthead_prefix = f"file://{os.environ['HOME']}/git/newsrack/recipes_custom/logos"
_masthead = f"{_masthead_prefix}/life-is-a-sacred-text.png"
_name = "Life is a Sacred Text"


class LifeIsASacredText(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    language = 'en'
    description = u'Life is a Sacred Text is about truth & transformation, with ancient stories serving as mirrors & lights. Collective liberation. Everybody-celebratory. https://lifeisasacredtext.com/'
    __author__ = 'holyspiritomb'
    category = 'rss'
    oldest_article = 30
    max_articles_per_feed = 10
    remove_empty_feeds = True
    resolve_internal_links = True
    use_embedded_content = True
    masthead_url = _masthead

    feeds = [("Posts", "https://www.lifeisasacredtext.com/rss/")]

    conversion_options = {
        'tags' : 'Theology, Judiaism, Jewish',
        'authors': 'Rabbi Danya Ruttenberg',
    }

    remove_tags = [
        classes("kg-signup-card outpost-pub-container kg-button-card kg-callout-card")
    ]

    remove_attributes = [
        "height", "width", "style"
    ]

    extra_css = '''
        #article_date{font-size:0.8rem;text-transform:uppercase;}
        #article_desc{font-style:italic;font-size:1.2rem}
        p{font-size:1rem}
        img {max-width: 98vw;}
        .image-caption,.kg-card-hascaption>div{
                font-size:0.8rem;font-style:italic;padding-top:1rem;padding-bottom:1rem;}
        #article_source > a{word-wrap: break-word}
        '''

    def populate_article_metadata(self, article, soup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
        nyc = ZoneInfo("America/New_York")
        nyc_dt = datetime.astimezone(article.utctime, nyc)
        datestring = datetime.strftime(nyc_dt, "%b %-d, %Y, %-I:%M %p %Z")
        nyc_dt_now = datetime.astimezone(datetime.now(), nyc)
        curr_datestring = datetime.strftime(nyc_dt_now, "%b %-d, %Y at %-I:%M %p %Z")
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
        date_el = soup.find(attrs={"id": "article_date"})
        date_el.string = f"{article.author} | {datestring}"
        # desc_el = soup.find(attrs={"id": "article_desc"})
        # desc_el.string = article.summary
        article_img = soup.find("img", attrs={"alt": True})
        if article_img:
            img_uri = article_img["src"]
            self.add_toc_thumbnail(article, img_uri)

    def parse_feeds(self):
        feeds = BasicNewsRecipe.parse_feeds(self)
        for feed in feeds:
            for article in feed.articles[:]:
                # self.log(article)
                if not article.content:
                    self.log.warn(f"removing subscriber-only article {article.title} from feed")
                    feed.articles.remove(article)
        new_feeds = [f for f in feeds if len(f.articles[:]) > 0]
        return new_feeds

    def preprocess_html(self, soup):
        headline = soup.find("h2")
        a_date = soup.new_tag("div")
        # a_desc = soup.new_tag("h3")
        # a_desc["id"] = "article_desc"
        a_date["id"] = "article_date"
        # headline.insert_after(a_desc)
        headline.insert_after(a_date)
        heads = soup.find_all("h2")
        for head in heads:
            if "Like this? Get more" in self.tag_to_string(head):
                for sib in head.next_siblings:
                    # self.log(sib)
                    if sib.name:
                        if sib.name == "p":
                            if "Sending a big pile of blessings and goodness your way" not in self.tag_to_string(sib):
                                sib.string = ""
                            else:
                                break
                        elif sib.name == "h4":
                            if "A note on the subscription model" in self.tag_to_string(sib):
                                sib.extract()
                        elif sib.name == "div":
                            break
                        else:
                            continue
                    else:
                        continue
                head.extract()
        for a in soup.find_all("a"):
            if "#/portal/account/plans" in a["href"]:
                a.extract()
            else:
                continue
        return soup

    def postprocess_html(self, soup, _):
        return soup
