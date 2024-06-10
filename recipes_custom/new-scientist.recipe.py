##
# Title:        New Scientist RSS recipe
# Contact:      AprilHare, Darko Miletic <darko.miletic at gmail.com>
##
# License:      GNU General Public License v3 - http://www.gnu.org/copyleft/gpl.html
# Copyright:    2008-2016, AprilHare, Darko Miletic <darko.miletic at gmail.com>
##
# Written:      2008
# Last Edited:  2023
##

'''
01-19-2012: Added GrayScale Image conversion and Duplicant article removals
12-31-2015: Major rewrite due to massive changes in site structure
01-27-2016: Added support for series index and minor cleanup
03-02-2023: Modified for newsrack usage
'''

__license__ = 'GNU General Public License v3 - http://www.gnu.org/copyleft/gpl.html'
__copyright__ = '2008-2016, AprilHare, Darko Miletic <darko.miletic at gmail.com>'
__version__ = 'v0.6.1'
__date__ = '2016-01-27'
__author__ = 'Darko Miletic, modified 2023 for newsrack by holyspiritomb'

'''
newscientist.com
'''
import os
import re
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

from calibre import browser
from calibre.ebooks.BeautifulSoup import BeautifulSoup
from calibre.web.feeds import Feed
from calibre.web.feeds.news import BasicNewsRecipe, classes

sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title


# convenience switches for when I'm developing
if "runner" in os.environ["recipes_includes"]:
    _masthead_prefix = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos"
else:
    _masthead_prefix = f"file://{os.environ['HOME']}/git/newsrack/recipes_custom/logos"
_masthead = f"{_masthead_prefix}/new-scientist.svg"

_name = "New Scientist"


class NewScientist(BasicNewsRecipe, BasicNewsrackRecipe):
    title = _name
    description = '''Science news and science articles from New Scientist. https://www.newscientist.com/'''
    masthead_url = _masthead
    language = 'en'
    publisher = 'Reed Business Information Ltd.'
    category = 'science news, science articles, science jobs, drugs, cancer, depression, computer software'
    oldest_article = 7
    max_articles_per_feed = 15
    no_stylesheets = True
    use_embedded_content = False
    encoding = 'utf-8'
    needs_subscription = 'optional'
    remove_empty_feeds = True
    ignore_duplicate_articles = {'url'}
    # timefmt = ' %a, %b %d, %Y'
    compress_news_images = False
    publication_type = 'magazine'
    scale_news_images = True
    resolve_internal_links = False
    reverse_article_order = False
    delay = 1
    simultaneous_downloads = 1
    conversion_options = {
        'tags': 'Science, News, New Scientist, Periodical',
        'series': 'New Scientist',
        'series_index': ''
    }
    extra_css = """
                                 body{font-family: "Lato", "Roboto", sans-serif}
                                 img{margin-bottom: 0.8em; display: block}
                                 h1{font-size:1.75rem;text-align:left}
                                 #url_div{padding-top:5px; font-size:0.8em;}
                                 h4 > a + span{font-weight:normal; text-transform: uppercase;font-family:sans-serif}
                                 h1 + p{font-size:1.5rem;font-style:italic;}
                                 h1 + p + p {font-size:1rem;border-bottom:1px dashed black;padding-bottom:0.7rem}
                                 div[data-method='caption-shortcode'] p{font-size: 0.8rem; line-height:0.7rem;font-style:italic}
                                 div[data-method='caption-shortcode'] p:last-of-type{border-bottom:1px dashed black; padding-bottom:0.5rem}
                                 h4{font-size: 0.8rem;}
                                 div[data-method='caption-shortcode'] ~ p{font-size:1rem;text-align:left}
                                 .quotebx{font-size: x-large; font-weight: bold; margin-right: 2em; margin-left: 2em}
                                 .article-title,h2,h3{font-family: "Lato Black", sans-serif}
                                 .strap{font-family: "Lato Light", sans-serif}
                                 .quote{font-family: "Lato Black", sans-serif}
                                 .box-out{font-family: "Lato Regular", sans-serif}
                                 .wp-caption-text{font-family: "Lato Bold", sans-serif; font-size:x-small;}
                                 div[data-method='caption-shortcode'] ~ div{border-top:1px dashed black;}
                                 div[data-method='caption-shortcode'] ~ div div > p:first-of-type{font-size: 1.2rem;font-weight:bold}
                                 div[data-method='caption-shortcode'] img{max-width:95%;margin-left:auto;margin-right:auto;}
                                 #article_meta{text-transform:uppercase;font-size:0.8rem}
                                """

    keep_only_tags = [
        classes('ArticleHeader ArticleContent ArticleCorrections'),
        dict(name="article", attrs={"id": True})
    ]
    remove_tags = [
        classes('ArticleHeader__SocialWrapper ReadMore ArticleImageCaption__Icon AdvertWrapper RelatedContentWrapper NewsletterPromotion ArticleHeader__DateTimeIcon ReadMoreWithImage SidebarNewsletterWrapper'),
        dict(attrs={'alt': ['Calendar icon']}),
        dict(attrs={'title': ['Calendar icon']})
    ]
    # remove_tags_after = [
        # dict(name="div", class_="ArticleTopics")
    # ]
    remove_attributes = ['width', 'height', 'data-analytics-hook', 'data-js-page-layout', 'data-js-grid-layout']

    feeds = [
        ('Features', 'https://www.newscientist.com/section/features/feed/'),
        ('News', 'https://www.newscientist.com/section/news/feed/'),
        ('Physics', 'https://www.newscientist.com/subject/physics/feed/'),
        ('Technology', 'https://www.newscientist.com/subject/technology/feed/'),
        ('Space', 'https://www.newscientist.com/subject/space/feed/'),
        ('Humans', 'https://www.newscientist.com/subject/humans/feed/'),
        ('Life', 'https://www.newscientist.com/subject/life/feed/'),
        ('Earth', 'https://www.newscientist.com/subject/earth/feed/'),
        ('Health', 'https://www.newscientist.com/subject/health/feed/'),
        # ('Other', 'https://www.newscientist.com/feed/home/')
    ]

    def preprocess_raw_html(self, raw_html, url):
        soup = BeautifulSoup(raw_html)
        if soup.find(name="meta", attrs={"name": "ob_page_type", "content": "paywall"}):
            # self.log.warn("Paywall encountered.")
            self.abort_article("Article is paywalled. Aborting.")
        if soup.find('meta', {'property': 'og:type', 'content': 'video'}) or soup.find("div", attrs={"class": "ArticleVideo"}):
            self.abort_article("Video article aborted.")
        header = soup.find(attrs={"class": "ArticleHeader"})
        headline = header.find("h1")
        headline["data-url"] = url
        meta_desc = soup.find('meta', {'property': 'og:description'})
        if meta_desc:
            headline["data-desc"] = meta_desc["content"]
        for img in soup.findAll('img', attrs={'srcset': True}):
            if "?" in img["src"]:
                a_src = img["src"].split("?")[0]
                img["src"] = a_src
        for div in soup.findAll(attrs={"class": "article-image-inline"}):
            for img in div.findAll("img", attrs={"loading": "lazy"}):
                if "?" in img["data-src"]:
                    imgsrc = img["data-src"].split("?")[0]
                    img["data-src"] = imgsrc
                img["src"] = img["data-src"]
        return str(soup)

    def preprocess_html(self, soup):
        header = soup.find("section", attrs={"class": "ArticleHeader"})
        categ = header.find("a", attrs={"class": "ArticleHeader__CategoryLink"})
        article_date = header.find("p", attrs={"class": "ArticleHeader__Date"})
        article_date.name = "span"
        date_elem = article_date.extract()
        categ.insert_after(date_elem)
        categ.insert_after(" | ")
        for img in soup.findAll('img', attrs={'srcset': True}):
            # img['src'] = img['srcset'].split(',')[-1].strip().split()[0].partition('?')[0]
            # self.log(img['alt'])
            del img['srcset']
            del img['data-src']
            del img['sizes']
            alt_txt = img["alt"]
            if alt_txt:
                alt_div = soup.new_tag("div", attrs={"class": "img-alt-text"})
                alt_div.append(alt_txt)
                img.insert_after(alt_div)
        topics = soup.find("section", attrs={"class": "ArticleTopics"})
        url = soup.find("h1")["data-url"]
        orig_url_div = soup.new_tag("div")
        orig_url_div["id"] = "url_div"
        srclink = soup.new_tag("a")
        srclink["id"] = "original_url"
        srclink.append(url)
        srclink_wrapper = soup.new_tag("span")
        srclink_wrapper.append("Downloaded from ")
        srclink_wrapper.append(srclink)
        srclink_wrapper.append(".")
        orig_url_div.append(srclink_wrapper)
        # self.log(orig_url_div)
        topics.insert_after(orig_url_div)
        hr = soup.new_tag("hr")
        topics.insert_after(hr)
        topics.extract()
        return soup

    def postprocess_html(self, soup, _):
        orig_link = soup.find("a", attrs={"id": "original_url"})
        a_url = self.tag_to_string(orig_link)
        orig_link["href"] = a_url
        return soup

    def get_article_url(self, article):
        ans = BasicNewsRecipe.get_article_url(self, article)
        return ans.partition('?')[0]

    def get_browser(self, *a, **kw):
        kw[
            "user_agent"
        ] = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        br = BasicNewsRecipe.get_browser(self, *a, **kw)
        if self.username is not None and self.password is not None:
            def is_login_form(form):
                return "action" in form.attrs and form.attrs['action'] == "/login/"
            br.open('https://www.newscientist.com/login/')
            br.select_form(predicate=is_login_form)
            br['email'] = self.username
            br['password'] = self.password
            res = br.submit().read()
            if b'>Log out<' not in res:
                raise ValueError('Failed to log in to New Scientist, check your username and password')
        return br

    def clone_browser(self, *args, **kwargs):
        return self.get_browser()

    def open_novisit(self, *args, **kwargs):
        br = browser()
        return br.open_novisit(*args, **kwargs)

    open = open_novisit

    def get_cover_url(self):
        soupdex = self.index_to_soup(
            'https://www.newscientist.com/issue/current/')
        div = soupdex.find('div', attrs={'class': 'ThisWeeksMagazineHero__CoverInfo'})
        # issue_dt = div.find('h3', attrs={'class': 'ThisWeeksMagazineHero__MagInfoHeading'})
        # if issue_dt:
            # issue_date = issue_dt.string
            # pub_date = datetime.strptime(issue_date, "%d %B %Y")
            # self.title = format_title(_name, pub_date)
        # Configure series and issue number
        issue_nr = div.find('p', attrs={'class': 'ThisWeeksMagazineHero__MagInfoDescription'})
        if issue_nr:
            self.log(issue_nr)
            if issue_nr.string is not None:
                non_decimal = re.compile(r'[^\d.]+')
                nr = non_decimal.sub('', issue_nr.string)
                self.conversion_options.update({'series': 'New Scientist'})
                self.conversion_options.update({'series_index': nr})
        cover_item = div.find('a', attrs={'class': 'ThisWeeksMagazineHero__ImageLink'})
        if cover_item:
            cover_url = cover_item["href"]
            # self.log(cover_url)
            return cover_url

    def parse_feeds(self):
        seen_urls = []
        feeds = BasicNewsRecipe.parse_feeds(self)
        for feed in feeds:
            initial_art = len(feed.articles[:])
            for article in feed.articles[:]:
                if article.url in seen_urls:
                    feed.articles.remove(article)
                    # self.log.warn("\t", article.title, " (already seen)")
                    continue
                else:
                    seen_urls.append(article.url)
                if 'OBESITY' in article.title.upper() or 'WEIGHT LOSS' in article.title.upper() or "Watch" in article.title:
                    feed.articles.remove(article)
                    continue
                elif "newscientist.com/video" in article.url:
                    # self.log.warn(f"\t\tremoving {article.url} from feed")
                    feed.articles.remove(article)
                    continue
                elif "PREMIUM ARTICLE" in article.summary.upper():
                    feed.articles.remove(article)
                    continue
                else:
                    continue
            final_art = len(feed.articles[:])
            if initial_art != final_art:
                removed_articles = initial_art - final_art
                self.log.debug("removed {} articles from {} feed".format(removed_articles, feed.title))
        new_feeds = [f for f in feeds if len(f.articles[:]) > 0]
        self.log("\n-----------\nTo Generate:")
        for feed in new_feeds:
            self.log("\t", feed.title)
            for article in feed.articles[:]:
                self.log("\t\t", article.title)
            self.log("\n")
        return new_feeds

    def populate_article_metadata(self, article, soup, _):
        nyc = ZoneInfo("America/New_York")
        nyc_dt = datetime.astimezone(article.utctime, nyc)
        datestring = datetime.strftime(nyc_dt, "%b %-d, %Y, %-I:%M %p %Z")
        header = soup.find(attrs={"class": "ArticleHeader__Category"})
        header["id"] = "article_meta"
        article_date = header.find(attrs={"class": "ArticleHeader__Date"})
        article_date.string = datestring
        meta_src = soup.new_tag("a")
        meta_src["href"] = article.url
        meta_src.append("View on New Scientist")
        article_date.insert_after(meta_src)
        article_date.insert_after(" | ")
        auths = []
        for a in soup.find_all("a"):
            if "author" in a["href"]:
                auth = self.tag_to_string(a)
                auths.append(auth)
        if len(auths) > 0:
            article.author = auths[0]
            if len(auths) > 1:
                for x in range(1, len(auths) - 1):
                    article.author = article.author + " & " + auths[x]
        article.title = format_title(article.title, article.utctime)
        headline = soup.find("h1")
        article.description = headline["data-desc"]
        toc_img = soup.find("img", attrs={"class": "image"})
        if toc_img:
            self.add_toc_thumbnail(article, toc_img['src'])
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
