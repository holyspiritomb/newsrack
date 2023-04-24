__license__ = 'GPL v3'
__copyright__ = '2008-2012, Darko Miletic <darko.miletic at gmail.com>'
'''
arstechnica.com
'''
import os
import sys

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
try:
    from recipes_shared import BasicNewsrackRecipe, format_title
except ImportError:
    # just for Pycharm to pick up for auto-complete
    from includes.recipes_shared import BasicNewsrackRecipe, format_title


import re
from calibre.web.feeds.news import BasicNewsRecipe

_name = "Ars Technica"

def classes(classes):
    q = frozenset(classes.split(' '))
    return dict(attrs={
        'class': lambda x: x and frozenset(x.split()).intersection(q)})


class ArsTechnica(BasicNewsRecipe, BasicNewsrackRecipe):
    title = _name
    language = 'en'
    __author__ = 'Darko Miletic, Sujata Raman, Alexis Rohou, Tom Sparks, holyspiritomb'
    description = 'Ars Technica: Serving the technologist for 1.2 decades'
    publisher = 'Conde Nast Publications'
    oldest_article = 5
    max_articles_per_feed = 100
    no_stylesheets = True
    encoding = 'utf-8'
    use_embedded_content = False
    remove_empty_feeds = True
    conversion_options = {
        'tags': 'Technology, Science, Periodical, Ars Technica',
    }
    extra_css             = '''
    body {font-family: Lato, Roboto, Arial,sans-serif}
    .heading{font-family: Lato, Roboto, Arial,sans-serif}
    .byline{font-weight: bold; line-height: 1em; font-size: 0.625em; text-decoration: none}
    img{display: block}
    .caption-text{font-size:small; font-style:italic}
    .caption-byline{font-size:small; font-style:italic; font-weight:bold}
    .video, .page-numbers, .story-sidebar { display: none }
    .image { display: block }
    '''

    keep_only_tags = [
        dict(itemprop=['headline', 'description']),
        classes('post-meta article-guts standalone'),
    ]

    remove_tags = [
        classes('site-header video corner-info article-expander left-column related-stories ad_xrail ad_xrail_top ad_xrail_last'),
        dict(name=['object', 'link', 'embed', 'iframe', 'meta']),
        dict(id=['social-left', 'article-footer-wrap']),
        dict(name='nav', attrs={'class': 'subheading'}),
    ]
    remove_attributes = ['lang', 'style']

    # Feed are found here: http://arstechnica.com/rss-feeds/
    feeds = [
        ('Features', 'http://feeds.arstechnica.com/arstechnica/features'),
        ('Technology Lab', 'http://feeds.arstechnica.com/arstechnica/technology-lab'),
        ('Gear &amp; Gadgets', 'http://feeds.arstechnica.com/arstechnica/gadgets'),
        ('Ministry of Innovation', 'http://feeds.arstechnica.com/arstechnica/business'),
        ('Risk Assessment', 'http://feeds.arstechnica.com/arstechnica/security'),
        ('Law &amp; Disorder', 'http://feeds.arstechnica.com/arstechnica/tech-policy'),
        ('Infinite Loop', 'http://feeds.arstechnica.com/arstechnica/apple'),
        ('Opposable Thumbs', 'http://feeds.arstechnica.com/arstechnica/gaming'),
        ('Scientific Method', 'http://feeds.arstechnica.com/arstechnica/science'),
        ('The Multiverse', 'http://feeds.arstechnica.com/arstechnica/multiverse'),
        ('Staff', 'http://feeds.arstechnica.com/arstechnica/staff-blogs'),
        ('Open Source', 'http://feeds.arstechnica.com/arstechnica/open-source'),
        ('microsoft', 'http://feeds.arstechnica.com/arstechnica/microsoft'),
        ('software', 'http://feeds.arstechnica.com/arstechnica/software'),
        ('telecom', 'http://feeds.arstechnica.com/arstechnica/telecom'),
        ('Internet', 'http://feeds.arstechnica.com/arstechnica/web'),
        ('Ars Technica', 'http://feeds.arstechnica.com/arstechnica/index'),
    ]

    def populate_article_metadata(self, article, __, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)

    recursions = 1

    def is_link_wanted(self, url, tag):
        return re.search(r'/[0-9]/$', url) is not None

    def parse_feeds(self):
        feeds = BasicNewsRecipe.parse_feeds(self)
        for feed in feeds:
            for article in feed.articles[:]:
                # self.log.info(f"article.title is: {article.title}")
                if 'OBESITY' in article.title.upper() or 'WEIGHT LOSS' in article.title.upper() or 'DEALMASTER' in article.title.upper():
                    self.log.warn(f"removing {article.title} from feed")
                    feed.articles.remove(article)
        return feeds

    def postprocess_html(self, soup, first_fetch):
        if not first_fetch:
            for x in soup.findAll(itemprop=['headline', 'description']):
                x.extract()
            for x in soup.findAll(**classes('post-meta')):
                x.extract()
        return soup
