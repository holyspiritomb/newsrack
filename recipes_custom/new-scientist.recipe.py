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
import sys
from datetime import datetime, timezone

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
try:
    from recipes_shared import BasicNewsrackRecipe, format_title
except ImportError:
    # just for Pycharm to pick up for auto-complete
    from includes.recipes_shared import BasicNewsrackRecipe, format_title


import re
from calibre.web.feeds.news import BasicNewsRecipe


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
    oldest_article = 15
    max_articles_per_feed = 100
    no_stylesheets = True
    use_embedded_content = False
    encoding = 'utf-8'
    needs_subscription = 'optional'
    remove_empty_feeds = True
    ignore_duplicate_articles = {'url'}
    compress_news_images = False
    publication_type = 'magazine'
    scale_news_images = True
    resolve_internal_links = True
    reverse_article_order = True
    conversion_options = {
        'tags' : 'Science, News, New Scientist, Periodical',
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
        classes('ArticleHeader ArticleContent Barrier')
    ]

    remove_tags = [
        classes('ArticleHeader__SocialWrapper ReadMore ArticleImageCaption__Icon AdvertWrapper ArticleTopics RelatedContentWrapper'),
        dict(attrs={'alt': ['Calendar icon']})
    ]

    def preprocess_html(self, soup):
        if soup.find(name="section", id="subscription-barrier"):
            self.abort_article("Aborted because subscription required")
        if soup.find('meta', {'property': 'og:type', 'content': 'video'}):
            self.abort_article("Aborted because video")
        for img in soup.findAll('img', attrs={'data-src': True}):
            img['src'] = img['data-src']
        for img in soup.findAll('img', attrs={'data-srcset': True}):
            img['src'] = img['data-srcset'].split(',')[-1].strip().split()[0]
            img['width'] = img['height'] = ''
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

    feeds = [
        ('Physics', 'https://www.newscientist.com/subject/physics/feed/'),
        ('Technology', 'https://www.newscientist.com/subject/technology/feed/'),
        ('Space', 'https://www.newscientist.com/subject/space/feed/'),
        ('Life', 'https://www.newscientist.com/subject/life/feed/'),
        ('Earth', 'https://www.newscientist.com/subject/earth/feed/'),
        ('Health', 'https://www.newscientist.com/subject/health/feed/'),
        ('Humans', 'https://www.newscientist.com/subject/humans/feed/'),
        ('Features', 'https://www.newscientist.com/section/features/feed/'),
        ('News', 'https://www.newscientist.com/section/news/feed/'),
    ]

    def get_cover_url(self):
        soupdex = self.index_to_soup(
            'https://www.newscientist.com/issue/current/')
        div = soupdex.find('div', attrs={'class': 'ThisWeeksMagazineHero__CoverInfo'})
        cover_item = div.find('a', attrs={'class': 'ThisWeeksMagazineHero__ImageLink'})
        if cover_item:
            cover_url = cover_item["href"]
        issue_dt = div.find('h3', attrs={'class': 'ThisWeeksMagazineHero__MagInfoHeading'})
        if issue_dt:
            issue_date = issue_dt.string
            pub_date = datetime.strptime(issue_date, "%d %B %Y")
            self.title = format_title(_name, pub_date)
        # Configure series and issue number
        issue_nr = div.find('p', attrs={'class': 'ThisWeeksMagazineHero__MagInfoDescription'})
        if issue_nr:
            if issue_nr.string is not None:
                non_decimal = re.compile(r'[^\d.]+')
                nr = non_decimal.sub('', issue_nr.string)
                self.conversion_options.update({'series': 'New Scientist'})
                self.conversion_options.update({'series_index': nr})
        return cover_url

    def populate_article_metadata(self, article, __, _):

        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            # self.title = format_title(_name, article.utctime)
