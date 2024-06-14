__license__ = 'GPL v3'
__copyright__ = '2014, Darko Miletic <darko.miletic at gmail.com>'
'''
www.wired.com
'''
import os
import re
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title

from calibre import browser
from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre.ebooks.BeautifulSoup import BeautifulSoup


# convenience switches for when I'm developing
if "runner" in os.environ["recipes_includes"]:
    _masthead_prefix = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos"
else:
    _masthead_prefix = f"file://{os.environ['HOME']}/git/newsrack/recipes_custom/logos"
_masthead = f"{_masthead_prefix}/wired-daily-masthead.png"
_cover = f"{_masthead_prefix}/wired.png"

_name = "Wired Daily Edition"


class WiredDailyNews(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    __author__ = 'Darko Miletic, PatStapleton(update 2020-05-24), modified further for newsrack by holyspiritomb'
    description = (
        '''Wired is a full-color monthly American magazine, published in both print and online editions, that reports on how emerging technologies affect culture, the economy and politics. Daily edition that scrapes from the website. https://www.wired.com/'''
    )
    masthead_url = _masthead
    cover_url = _cover
    publisher = 'Conde Nast'
    category = 'news, IT, computers, technology'
    oldest_article = 7
    max_articles_per_feed = 200
    no_stylesheets = True
    encoding = 'utf-8'
    use_embedded_content = False
    language = 'en'
    ignore_duplicate_articles = {'url'}
    remove_empty_feeds = True
    publication_type = 'newsportal'
    delay = 2
    recursions = 0
    extra_css = """
        .entry-header{
                        text-transform: uppercase;
                        vertical-align: baseline;
                        display: inline;
                        }
        p {font-size: 1em}
        #lead-image, #lead-image-caption{
                        display: block;
                        }
        #lead-image-caption, #categ_date, .caption__text, .caption__credit, p.byline, .caption, #article_source{font-size:0.8em;}
        span.lead-in-text-callout, .caption__text p {font-size: 1.1em;}
        #categ_date{
                        text-transform: uppercase;
                        }
        img[alt] {max-width: 90vw; height:auto;}
        ul:not(.calibre_feed_list) li{display: inline}
    """
    conversion_options = {
        'tags' : 'Science, Technology, Wired Daily, Periodical',
        'authors' : 'newsrack',
    }

    remove_tags = [
        classes('related-cne-video-component tags-component podcast_42 storyboard inset-left-component social-icons recirc-most-popular-wrapper'),
        dict(name='button', attrs={'aria-label': 'Save'}),
        dict(name=['meta', 'link', 'aside']),
        dict(id=['sharing', 'social', 'article-tags', 'sidebar']),
    ]
    keep_only_tags = [
        dict(name='article', attrs={'class': 'article main-content'}),
    ]
    remove_attributes = ['srcset', 'sizes', 'media', 'data-event-click', 'data-offer-url']
    filter_out = ["obesity", "weight loss", "best shows", "review:", "best movies", "best deals"]
    keyword_filter = [
        "deals",
        "product reviews",
        "shopping",
        "apparel",
        "fashion",
        "culture guides",
        "buying guides",
    ]
    handle_gzip = True

    # https://www.wired.com/about/rss-feeds/
    feeds = [
        (u'AI', u'https://www.wired.com/feed/tag/ai/latest/rss'),
        (u'Business', u'https://www.wired.com/feed/category/business/latest/rss'),
        (u'Culture', u'https://www.wired.com/feed/category/culture/latest/rss'),
        (u'Ideas', u'https://www.wired.com/feed/category/ideas/latest/rss'),
        (u'Gear', u'https://www.wired.com/feed/category/gear/latest/rss'),
        (u'Science', u'https://www.wired.com/feed/category/science/latest/rss'),
        (u'Security', u'https://www.wired.com/feed/category/security/latest/rss'),
        (
            u'Transportation',
            u'https://www.wired.com/feed/category/transportation/latest/rss'
        ),
        (
            u'Backchannel',
            u'https://www.wired.com/feed/category/backchannel/latest/rss'
        ),
        (u'Top Stories', u'https://www.wired.com/feed/rss'),
        (u'WIRED Guides', u'https://www.wired.com/feed/tag/wired-guide/latest/rss'),
        #    (u'Photo', u'https://www.wired.com/feed/category/photo/latest/rss'),
    ]

    def parse_feeds(self):
        feeds = BasicNewsRecipe.parse_feeds(self)
        regex = re.compile(r'[B|b]est.+\([0-9]{4}\)')
        for feed in feeds:
            # self.log.debug(feed.title)
            for article in feed.articles[:]:
                self.log(article.title, "\n", article.url)
                if re.search(regex, article.title):
                    self.log.warn(f"removing {article.title} from feed (regex)")
                    feed.articles.remove(article)
                    continue
                else:
                    for word in self.filter_out:
                        # self.log.debug(f"checking {article.title} for {word}")
                        if word.upper() in article.title.upper():
                            self.log.warn(f"removing {article.title} from feed (keyword {word})")
                            feed.articles.remove(article)
                            break
                        else:
                            continue
                    self.log.debug(f"keeping {article.title} in feed {feed.title}")
        new_feeds = [f for f in feeds if len(f.articles[:]) > 0]
        return new_feeds

    def populate_article_metadata(self, article, soup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
        nyc = ZoneInfo("America/New_York")
        nyc_dt_now = datetime.astimezone(datetime.now(), nyc)
        curr_datestring = datetime.strftime(nyc_dt_now, "%b %-d, %Y at %-I:%M %p %Z")
        article_dt = datetime.astimezone(article.utctime, nyc)
        article_dt_str = datetime.strftime(article_dt, "%b %-d, %Y at %-I:%M %p %Z")
        a_date = soup.find(attrs={"id": "article_date"})
        if a_date:
            a_date.string = article_dt_str

        source_link_div = soup.new_tag("div")
        source_link_div["id"] = "article_source"
        source_link = soup.new_tag("a")
        source_link["href"] = article.url
        source_link.string = article.url
        header_src_a = soup.find("a", attrs={"id": "header_src_a"})
        header_src_a["href"] = article.url
        source_link_div.append("This article was downloaded from ")
        source_link_div.append(source_link)
        source_link_div.append(" on ")
        source_link_div.append(curr_datestring)
        source_link_div.append(".")
        hr = soup.new_tag("hr")
        soup.append(hr)
        soup.append(source_link_div)

    def preprocess_html(self, soup):
        a_soup = soup.find(class_='article main-content')
        headline = a_soup.find(attrs={'data-testid': "ContentHeaderHed"})
        subhead = a_soup.find(attrs={'data-testid': 'ContentHeaderAccreditation'})
        if subhead:
            subhead["id"] = "subhead"
            subhead.name = "h2"
            subhead_text = self.tag_to_string(subhead)
            subhead.clear()
            subhead.append(subhead_text)
        category = a_soup.find("a", class_='rubric__link')
        category["class"] = 'rubric__link'

        author = a_soup.find("p", attrs={'itemprop': 'author'})
        author["class"] = 'byline bylines__byline'

        lead_pic = a_soup.find("div", class_='lead-asset')
        if lead_pic:
            lead_img = lead_pic.find('img')
            lead_cap = lead_pic.find(attrs={'class': 'caption__credit'})
            if lead_img and lead_cap:
                lead_img["id"] = "lead-image"
                lead_cap["id"] = "lead-image-credit"

        a_date = a_soup.find("time")
        a_date["id"] = "article_date"
        self.log.warn(headline, "\n", a_date)

        cat_time = soup.new_tag("div")
        cat_time["id"] = "categ_date"
        cat_time.append(category)
        cat_time.append(" | ")
        cat_time.append(a_date)
        cat_time.append(" | ")
        srclink_span = soup.new_tag("span")
        srclink_span["id"] = "header_src"
        srclink_a = soup.new_tag("a")
        srclink_a["href"] = "#"
        srclink_a["id"] = "header_src_a"
        srclink_a.append("View on Wired")
        srclink_span.append(srclink_a)
        cat_time.append(srclink_span)
        new_soup = soup.new_tag("div")
        new_soup.append(cat_time)
        new_soup.append(headline)
        new_soup.append(author)

        if subhead:
            new_soup.append(subhead)
        if lead_pic:
            if lead_img:
                new_soup.append(lead_img)
                if lead_cap:
                    new_soup.append(lead_cap)

        content = a_soup.find_all("div", class_='body__inner-container')
        for piece in content:
            new_soup.append(piece)
        new_soup["class"] = 'the_article'
        for noscript in new_soup.find_all("noscript"):
            noscript["class"] = "noscript"
            noscript.name = "div"
        for div in new_soup.find_all("div", attrs={'aria-level': "3"}):
            div.name = "h3"
        a_soup.clear()
        a_soup.append(new_soup)
        return soup
    
    def preprocess_raw_html(self, raw_html, url):
        soup = BeautifulSoup(raw_html)
        head = soup.find("head")
        t = head.find("title")
        metas = head.findAll("meta", attrs={"name": re.compile("keyword")})
        for m in metas:
            for k in self.keyword_filter:
                if k in m["content"]:
                    # self.log.warn(f"Matched keyword {k} in article {t.string}.")
                    self.abort_article(f"Article '{t.string}' matched keyword filter for {k}.")
                else:
                    # self.log.info(f"Didn't find keyword {k} in article {t.string}.")
                    continue
        return str(soup)

    def get_article_url(self, article):
        return article.get('link', None)

    # Wired changes the content it delivers based on cookies, so the
    # following ensures that we send no cookies
    def get_browser(self, *a, **kw):
        kw[
            "user_agent"
        ] = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        br = BasicNewsRecipe.get_browser(self, *a, **kw)
        return br

    def clone_browser(self, *args, **kwargs):
        return self.get_browser()

    def open_novisit(self, *args, **kwargs):
        br = browser()
        return br.open_novisit(*args, **kwargs)

    open = open_novisit
