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
    remove_tags = [
        dict(name='footer'),
        dict(name="nav")
    ]
    # BASE_TEXTONLY = "https://text.npr.org"
    # BASE_RICH = "https://npr.org"
    feeds = [
        (u'National', u'http://www.npr.org/rss/rss.php?id=1003'),
        (u'World', u'http://www.npr.org/rss/rss.php?id=1004'),
        ('Law', 'https://feeds.npr.org/1070/rss.xml'),
        ('Politics', 'https://feeds.npr.org/1014/rss.xml'),
        ('Health', 'https://feeds.npr.org/1128/rss.xml'),
        ('Science', 'https://feeds.npr.org/1007/rss.xml'),
        ('Space', 'https://feeds.npr.org/1026/rss.xml'),
        ('Climate', 'https://feeds.npr.org/1167/rss.xml'),
        # ('Global Health', 'https://feeds.npr.org/1039/rss.xml'),
        ('Education', 'https://feeds.npr.org/1013/rss.xml'),
        ('Race', 'https://feeds.npr.org/1015/rss.xml'),
        ('Religion', 'https://feeds.npr.org/1016/rss.xml'),
        ('Books', 'https://feeds.npr.org/1161/rss.xml'),
        ('Culture', 'https://feeds.npr.org/1008/rss.xml'),
    ]

    extra_css = '''
        .story-text{
        font-size: 1rem;
        }
        .slu.slug-link{
        font-size:0.75rem;
        }
        h1 {
        font-size:1.75rem;
        text-align:left;
        }
        h1.story-title ~ p{
        font-size: 0.75rem;
        }
        span#dateline, div#categ-date{
        text-transform: uppercase;
        font-size: 0.75rem;
        }
    '''

    def populate_article_metadata(self, article, soup, _):
        article_dt_el = soup.find("time")
        if article_dt_el:
            # 2023-04-21T05:10:22-04:00
            article.date = datetime.strptime(article_dt_el['datetime'], "%Y-%m-%dT%H:%M:%S%z")
            article.title = format_title(article.title, article.date)
        else:
            article.title = format_title(article.title, article.utctime)
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)

    def get_article_url(self, article):
        # self.log.warn(article.link)
        article_rich_url = article.link
        article_id = article_rich_url.split('/')[-2]
        article_textonly_url = f"https://text.npr.org/{article_id}"
        # self.log(article_textonly_url)
        return article_textonly_url

    def preprocess_raw_html(self, raw_html, url):
        soup = BeautifulSoup(raw_html, from_encoding='utf-8')
        # self.abort_recipe_processing()
        para_div = soup.find("div", attrs={"class": "paragraphs-container"})
        if len(para_div.find_all("p")) == 1:
            self.abort_article("aborting audio-only article")
        for p in para_div.find("p"):
            p.class_ = "story-text"
        related_hr = para_div.find_all("hr")
        rel_cont = soup.new_tag("div", attrs={"id": "related-story-container"})
        rel_cont_head = soup.new_tag("h3")
        rel_cont_head.append("Related")
        rel_cont_ul = soup.new_tag("ul", attrs={"id": "related-story-list"})
        rel_cont.append(rel_cont_head)
        rel_cont.append(rel_cont_ul)
        for hr in related_hr:
            if hr.next_sibling == "\n      Related Story: ":
                related_story_link = hr.find_next("a").extract()
                hr.next_sibling.replace_with("")
                li = soup.new_tag("li")
                li.append(related_story_link)
                rel_cont_ul.append(li)
                hr.find_next("hr").extract()
                hr.extract()
        if len(rel_cont_ul.contents) > 0:
            soup.find("article").insert_after(rel_cont)
        header = soup.find("div", attrs={"class": "story-head"})
        dateline = header.find_all("p")[1]
        dateline['id'] = "dateline"
        dateline.name = "span"
        dt_str = str(dateline.string)
        dt = datetime.strptime(dt_str, "%A, %B %d, %Y • %I:%M %p %Z")
        new_dt_str = datetime.strftime(dt, "%b %d %Y, %-I:%M %p")
        dateline.string = new_dt_str
        dateline_ex = dateline.extract()
        category = soup.find_all("a", attrs={"class": "slug-link"})[1]
        if category.text == "Sports":
            self.abort_article(msg="sports")
        categ_ex = category.extract()
        header_div = soup.new_tag("div", attrs={"id": "categ-date"})
        header_div.append(categ_ex)
        header_div.append(": ")
        header_div.append(dateline_ex)
        header.insert_before(header_div)
        soup.find('p', attrs={"class": "slug-line"}).decompose()
        # datep = firstp.sibling_next("p")
                # dateline = datetime.strptime(str(p.text), "%A, %B %d, %Y • %I:%M %p %Z")
                # date_str = datetime.strftime(dateline, "%b %d %Y, %-I:%M %p")
                # self.log.warn(date_str)
        return str(soup)

    def preprocess_html(self, soup):
        richlink = soup.find("a", attrs={"class": "full-version-link"})
        if richlink:
            richurl = richlink['href']
            richlink_el = soup.new_tag("a", attrs={"href": richurl})
            richlink_el.append(f"{richurl}")
            full_link_div = soup.new_tag("div", attrs={"id": "rich-link"})
            full_link_div.append("Full article: ")
            full_link_div.append(richlink_el)
            hr = soup.new_tag("hr")
            soup.find("article").append(hr)
            soup.find("article").append(full_link_div)
            soup.find("header").decompose()
        return soup


calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
