
import os
import re
import sys
# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title
from calibre.web.feeds.news import BasicNewsRecipe, classes

_name = 'The Advocate'


class TheAdvocate(BasicNewsrackRecipe, BasicNewsRecipe):

    title = _name
    language = 'en'
    # use_embedded_content = False
    remove_empty_feeds = True
    masthead_url = "https://upload.wikimedia.org/wikipedia/en/4/46/Advocate1.jpg"
    # masthead_url = "https://www.advocate.com/media-library/eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpbWFnZSI6Imh0dHBzOi8vYXNzZXRzLnJibC5tcy8zMjg0MjU0OC9vcmlnaW4ucG5nIiwiZXhwaXJlc19hdCI6MTcxNDcxMzQ4MH0.rZo95Jiq6Ph8PVSZjmnPedqpyEz0RwIhb9oRpSZVIHg/image.png"

    description = "Gay, lesbian, bisexual, transgender, queer news leader including politics, commentary, arts and entertainment - your source for LGBTQ news for over 50 years."
    __author__ = 'holyspiritomb'
    no_stylesheets = True

    # Don't grab articles more than 30 days old
    oldest_article = 30

    feeds = [
        ('Families', 'https://www.advocate.com/feeds/families.rss'),
        ('Trans', 'https://www.advocate.com/feeds/transgender.rss'),
        ('Bi', 'https://www.advocate.com/feeds/bisexual.rss'),
        ('Voices', 'https://www.advocate.com/feeds/voices.rss'),
        ('Arts', 'https://www.advocate.com/feeds/arts-entertainment.rss'),
        ('Religion', 'https://www.advocate.com/feeds/religion.rss'),
        ('Politics', 'https://www.advocate.com/feeds/politics.rss'),
        ('Business', 'https://www.advocate.com/feeds/business.rss'),
        ('Main', 'https://www.advocate.com/feeds/feed.rss'),
    ]

    def populate_article_metadata(self, article, __, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
