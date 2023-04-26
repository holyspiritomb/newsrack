#!/usr/bin/env python
__license__ = 'GPL v3'
__copyright__ = '2008-2017, Darko Miletic <darko.miletic at gmail.com>'
'''
sciencedaily.com
'''

import os
import sys
from calibre import browser
from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre.utils.date import utcnow, parse_date

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
try:
    from recipes_shared import BasicNewsrackRecipe, format_title
except ImportError:
    # just for Pycharm to pick up for auto-complete
    from includes.recipes_shared import BasicNewsrackRecipe, format_title


_name = "Science Daily"


class ScienceDaily(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    __author__ = u'Darko Miletic'
    description = ('''ScienceDaily is one of the Internet's most popular science news web sites. Since starting in 1995, the award-winning site has earned the loyalty of students, researchers, healthcare professionals, government agencies, educators and the general public around the world. Now with more than 6 million monthly visitors worldwide, ScienceDaily generates nearly 20 million page views a month and is steadily growing in its global audience. https://www.sciencedaily.com/''')
    conversion_options = {
        'tags' : 'Science, Science Daily, Periodical',
        'authors' : 'newsrack',
    }
    masthead_url = "https://i.imgur.com/nQ1lgZZ.png"
    oldest_article = 7
    remove_empty_feeds = True
    max_articles_per_feed = 50
    use_embedded_content = False
    language = 'en'
    encoding = 'utf-8'
    delay = 3
    publication_type = 'newspaper'
    auto_cleanup = False
    resolve_internal_links = False
    recursions = 0
    remove_tags = [
        classes("logo sharing hr-logo fullstory"),
        dict(id='related_releases'),
        dict(id='related_topics'),
        dict(id='share_top'),
        dict(id='topnav'),
        dict(id='div-gpt-ad-story_bottom'),
        dict(id='div-gpt-ad-story_middle'),
        dict(id='div-gpt-ad-story_top'),
        dict(id='citation_mla'),
        dict(id='citation_chicago'),
        dict(name='ul', attrs={'role': 'tablist'}),
        dict(name='dt', attrs={'class': 'no-print'}),
        dict(name='dd', attrs={'class': 'no-print'}),
        dict(name='div', attrs={'class': 'mobile-top-rectangle'}),
        dict(name='div', attrs={'class': 'mobile-end-rectangle'}),
        dict(name='ul', attrs={'class': 'topics'}),
    ]
    remove_tags_before = [
        dict(name='h1', attrs={'id': 'headline'}),

    ]
    remove_tags_after = [
        dict(name='div', attrs={'id': 'citations'}),

    ]

    extra_css = """
        dd,dt,
        #abstract,
        #date_posted,
        #source,
        #citations,
        #journal_references
        {
            font-size:0.8rem;
        }
        h1#headline{
            font-size:1.75rem;
            text-align:left;
        }
        h2{
            text-align:left;
            font-size:1.5rem
        }
        p#first{
            font-size:1.25rem;
            text-align:left;
        }
        #text > p{
            font-size: 1rem;
            text-align:left;
        }
    """

    # Feed are found here: https://www.sciencedaily.com/newsfeeds.htm
    feeds = [
        (u'Top Science News', u'https://www.sciencedaily.com/rss/top/science.xml'),
        # (u'Top News', u'https://www.sciencedaily.com/rss/top.xml'),
        # (u'Top Health', u'https://www.sciencedaily.com/rss/top/health.xml'),
        # (u'Top Technology', u'https://www.sciencedaily.com/rss/top/technology.xml'),
        # (u'Top Society', u'https://www.sciencedaily.com/rss/top/society.xml'),
        # (u'Top Environment', u'https://www.sciencedaily.com/rss/top/environment.xml'),
        (u'Mind and Brain', u'https://www.sciencedaily.com/rss/mind_brain.xml'),
        (u'Space and Time', u'https://www.sciencedaily.com/rss/space_time.xml'),
        (u'Matter and Energy', u'https://www.sciencedaily.com/rss/matter_energy.xml'),
        (u'Computers and Math', u'https://www.sciencedaily.com/rss/computers_math.xml'),
        # ('Technology News', 'https://www.sciencedaily.com/rss/top/technology.xml'),
        # ('Earth and Climate', 'https://www.sciencedaily.com/rss/earth_climate.xml'),
        # ('Plants and Animals', 'https://www.sciencedaily.com/rss/plants_animals.xml'),
        # ('Fossils and Ruins', 'https://www.sciencedaily.com/rss/fossils_ruins.xml'),
        # ('Society News', 'https://www.sciencedaily.com/rss/science_society.xml'),
        (u'All News', u'https://www.sciencedaily.com/rss/all.xml'),
    ]

    def parse_feeds(self):
        feeds = BasicNewsRecipe.parse_feeds(self)
        for feed in feeds:
            for article in feed.articles[:]:
                # self.log.info(f"article.title is: {article.title}")
                if 'OBESITY' in article.title.upper() or 'WEIGHT LOSS' in article.title.upper():
                    self.log.warn(f"removing {article.title} from feed")
                    feed.articles.remove(article)
        return feeds

    def populate_article_metadata(self, article, __, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
            article.title = format_title(article.title, article.utctime)

    def get_browser(self, *args, **kwargs):
        return self

    def clone_browser(self, *args, **kwargs):
        return self.get_browser()

    def open_novisit(self, *args, **kwargs):
        br = browser()
        return br.open_novisit(*args, **kwargs)

    open = open_novisit


calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'