import os
import sys
from datetime import timezone, timedelta
from urllib.parse import urljoin
from calibre.web.feeds import Feed
from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre.utils.date import utcnow, parse_date
# from calibre.ebooks.BeautifulSoup import BeautifulSoup

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title

_name = "WTF Just Happened Today"


class WTFJHT(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    oldest_article = 7
    language = 'en'
    __author__ = 'holyspiritomb'
    max_articles_per_feed = 100
    no_stylesheets = True
    no_javascript = True
    remove_empty_feeds = True
    use_embedded_content = True
    publication_type = 'newspaper'
    masthead_url = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos/wtfjht-t.jpg"
    # auto_cleanuo = True
    description = (
        '''Today's essential guide to the daily shock and awe in national politics. Read in moderation.'''
    )

    # remove_attributes = ["style", "sizes"]
    # remove_tags_before = dict(name="section", attrs={'id': 'main-section'})
    # remove_tags_after = dict(name='div', attrs={'id': 'storytext'})
    # remove_tags = []
    feeds = [
        # ('WTF', 'https://whatthefuckjusthappenedtoday.com/atom.xml'),
        ('WTF ', 'https://whatthefuckjusthappenedtoday.com/rss.xml')
    ]

    extra_css = '''
    '''

    def populate_article_metadata(self, article, __, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)

    def parse_feeds(self):
        # convert single parsed feed into date-sectioned feed
        # use this only if there is just 1 feed
        parsed_feeds = super().parse_feeds()
        if len(parsed_feeds or []) != 1:
            return parsed_feeds

        articles = []
        articles = sorted(articles, key=lambda art: art.utctime, reverse=True)
        new_feeds = []
        curr_feed = None
        parsed_feed = parsed_feeds[0]
        for i, a in enumerate(articles, start=1):
            date_published = a.utctime.replace(tzinfo=timezone.utc)
            date_published_loc = date_published.astimezone(
                timezone(offset=timedelta(hours=-7))  # PST
            )
            article_index = f"{date_published_loc:%-d %B, %Y}"
            if i == 1:
                curr_feed = Feed(log=parsed_feed.logger)
                curr_feed.title = article_index
                curr_feed.description = parsed_feed.description
                curr_feed.image_url = parsed_feed.image_url
                curr_feed.image_height = parsed_feed.image_height
                curr_feed.image_alt = parsed_feed.image_alt
                curr_feed.oldest_article = parsed_feed.oldest_article
                curr_feed.articles = []
                curr_feed.articles.append(a)
                continue
            if curr_feed.title == article_index:
                curr_feed.articles.append(a)
            else:
                new_feeds.append(curr_feed)
                curr_feed = Feed(log=parsed_feed.logger)
                curr_feed.title = article_index
                curr_feed.description = parsed_feed.description
                curr_feed.image_url = parsed_feed.image_url
                curr_feed.image_height = parsed_feed.image_height
                curr_feed.image_alt = parsed_feed.image_alt
                curr_feed.oldest_article = parsed_feed.oldest_article
                curr_feed.articles = []
                curr_feed.articles.append(a)
            if i == len(articles):
                # last article
                new_feeds.append(curr_feed)

        return new_feeds

calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
