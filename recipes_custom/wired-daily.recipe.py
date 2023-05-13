__license__ = 'GPL v3'
__copyright__ = '2014, Darko Miletic <darko.miletic at gmail.com>'
'''
www.wired.com
'''
import os
import re
import sys

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title

from calibre import browser
from calibre.web.feeds.news import BasicNewsRecipe


def classes(classes):
    q = frozenset(classes.split(' '))
    return dict(attrs={
        'class': lambda x: x and frozenset(x.split()).intersection(q)})


_name = "Wired Daily Edition"


class WiredDailyNews(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    __author__ = 'Darko Miletic, PatStapleton(update 2020-05-24), modified for newsrack by holyspiritomb'
    description = (
        '''Wired is a full-color monthly American magazine, published in both print and online editions, that reports on how emerging technologies affect culture, the economy and politics. Daily edition that scrapes from the website. https://www.wired.com/'''
    )
    masthead_url = 'https://www.wired.com/images/logos/apple-touch-icon.png'
    cover_url = 'https://www.wired.com/images/logos/wired.png'
    publisher = 'Conde Nast'
    category = 'news, IT, computers, technology'
    oldest_article = 3
    max_articles_per_feed = 200
    no_stylesheets = True
    encoding = 'utf-8'
    use_embedded_content = False
    language = 'en'
    ignore_duplicate_articles = {'url'}
    remove_empty_feeds = True
    publication_type = 'newsportal'
    extra_css = """
        .entry-header{
                        text-transform: uppercase;
                        vertical-align: baseline;
                        display: inline;
                        }
        ul:not(.calibre_feed_list) li{display: inline}
    """
    conversion_options = {
        'tags' : 'Science, Technology, Wired Daily, Periodical',
        'authors' : 'newsrack',
    }

    remove_tags = [
        classes('related-cne-video-component tags-component podcast_42 storyboard inset-left-component social-icons recirc-most-popular-wrapper'),
        dict(name=['meta', 'link', 'aside']),
        dict(id=['sharing', 'social', 'article-tags', 'sidebar']),
    ]
    keep_only_tags = [
        dict(name='article', attrs={'class': 'article main-content'}),
    ]
    remove_attributes = ['srcset']
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
        regex = re.compile(r'\d+\WBest')
        for feed in feeds:
            for article in feed.articles[:]:
                # self.log.info(f"article.title is: {article.title}")
                if 'OBESITY' in article.title.upper() or 'WEIGHT LOSS' in article.title.upper():
                    self.log.warn(f"removing {article.title} from feed")
                    feed.articles.remove(article)
                    continue
                if regex.match(article.title):
                    self.log.warn(f"removing {article.title} from feed")
                    feed.articles.remove(article)
                    continue
        return feeds

    def populate_article_metadata(self, article, __, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)

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
