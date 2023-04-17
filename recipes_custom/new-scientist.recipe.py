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

from calibre import browser
from calibre.ebooks.BeautifulSoup import BeautifulSoup
from calibre.web.feeds.news import BasicNewsRecipe

sys.path.append(os.environ["recipes_includes"])
try:
    from recipes_shared import BasicNewsrackRecipe, format_title
except ImportError:
    # just for Pycharm to pick up for auto-complete
    from includes.recipes_shared import BasicNewsrackRecipe, format_title


def classes(classes):
    q = frozenset(classes.split(' '))
    return dict(attrs={
        'class': lambda x: x and frozenset(x.split()).intersection(q)})


_name = "New Scientist"


class NewScientist(BasicNewsRecipe, BasicNewsrackRecipe):
    title = _name
    description = '''Science news and science articles from New Scientist. https://www.newscientist.com/'''
    masthead_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c0/New_Scientist_logo.svg/1024px-New_Scientist_logo.svg.png'
    language = 'en'
    publisher = 'Reed Business Information Ltd.'
    category = 'science news, science articles, science jobs, drugs, cancer, depression, computer software'
    oldest_article = 7
    max_articles_per_feed = 25
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
    resolve_internal_links = True
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
                                 .quotebx{font-size: x-large; font-weight: bold; margin-right: 2em; margin-left: 2em}
                                 .article-title,h2,h3{font-family: "Lato Black", sans-serif}
                                 .strap{font-family: "Lato Light", sans-serif}
                                 .quote{font-family: "Lato Black", sans-serif}
                                 .box-out{font-family: "Lato Regular", sans-serif}
                                 .wp-caption-text{font-family: "Lato Bold", sans-serif; font-size:x-small;}
                                """

    keep_only_tags = [
        classes('ArticleHeader ArticleContent ArticleCorrections'),
        dict(name="article", attrs={"id": True})
    ]
    remove_tags = [
        classes('ArticleHeader__SocialWrapper ReadMore ArticleImageCaption__Icon AdvertWrapper RelatedContentWrapper NewsletterPromotion ArticleHeader__DateTimeIcon ReadMoreWithImage'),
        dict(attrs={'alt': ['Calendar icon']}),
        dict(attrs={'title': ['Calendar icon']})
    ]
    # remove_tags_after = [
        # dict(name="div", class_="ArticleTopics")
    # ]
    remove_attributes = ['width', 'height', 'data-analytics-hook', 'data-js-page-layout', 'data-js-grid-layout']

    feeds = [
        ('Features', 'https://www.newscientist.com/section/features/feed/'),
        ('Physics', 'https://www.newscientist.com/subject/physics/feed/'),
        ('Technology', 'https://www.newscientist.com/subject/technology/feed/'),
        ('Space', 'https://www.newscientist.com/subject/space/feed/'),
        ('Life', 'https://www.newscientist.com/subject/life/feed/'),
        ('Earth', 'https://www.newscientist.com/subject/earth/feed/'),
        ('Health', 'https://www.newscientist.com/subject/health/feed/'),
        ('Humans', 'https://www.newscientist.com/subject/humans/feed/'),
        ('News', 'https://www.newscientist.com/section/news/feed/'),
        # ('Other', 'https://www.newscientist.com/feed/home/')
    ]

    # def preprocess_raw_html(self, raw_html, url):
        # soup = BeautifulSoup(raw_html)
        # gcacheprefix = 'https://webcache.googleusercontent.com/search?q=cache:'
        # gcacheurl = gcacheprefix + url
        # if soup.find(name="section", id="subscription-barrier"):
        #     self.log.warn(f"Subscription barrier on {url}")
        #     self.log.warn(f"Trying {gcacheurl}")
        #     gcachesoup = self.index_to_soup(gcacheurl)
        #     return str(gcachesoup)
        # else:
        # return str(soup)

    def preprocess_html(self, soup):
        if soup.find(name="meta", attrs={"name": "ob_page_type", "content": "paywall"}):
            self.log.warn("Paywall encountered.")
            self.abort_article("Article is paywalled. Aborting.")
        if soup.find('meta', {'property': 'og:type', 'content': 'video'}) or soup.find("div", attrs={"class": "ArticleVideo"}):
            self.abort_article("Video article aborted.")
        # for img in soup.findAll('img', attrs={'data-src': True}):
            # img['src'] = img['data-src']

        for img in soup.findAll('img', attrs={'srcset': True}):
            img['src'] = img['srcset'].split(',')[-1].strip().split()[0].partition('?')[0]
            self.log(img['alt'])
            del img['srcset']
            del img['data-src']
            del img['sizes']
        return soup

    def get_article_url(self, article):
        ans = BasicNewsRecipe.get_article_url(self, article)
        return ans.partition('?')[0]

    def get_browser(self):
        br = BasicNewsRecipe.get_browser(self)
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
            self.log(cover_url)
            return cover_url

    # def get_obfuscated_article(self, url):
        # gcacheprefix = 'https://webcache.googleusercontent.com/search?q=cache:'
        # gurl = gcacheprefix + url

    def populate_article_metadata(self, article, soup, _):
        self.log(article.title)
        self.log(article.url)
        self.log(article.utctime)
        article.title = format_title(article.title, article.utctime)
        div = soup.find("div", attrs={"class": "ArticleImage"})
        toc_img = div.find("img", attrs={"class": "image"})
        if toc_img:
            thumb_src = toc_img['src']
            self.add_toc_thumbnail(article, thumb_src)
        # article_inline_date = soup.find("p", attrs={"class": "ArticleHeader__Date"})
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
