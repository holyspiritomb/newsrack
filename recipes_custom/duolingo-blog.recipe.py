import os
import sys

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
try:
    from recipes_shared import BasicNewsrackRecipe, format_title
except ImportError:
    # just for Pycharm to pick up for auto-complete
    from includes.recipes_shared import BasicNewsrackRecipe, format_title

from calibre.web.feeds.news import BasicNewsRecipe, classes

_name = "Duolingo Blog"


class Duolingo(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    __author__ = "holyspiritomb"
    language = "en"
    oldest_article = 75  # days
    publication_type = 'blog'
    resolve_internal_links = True
    use_embedded_content = True
    no_stylesheets = True
    description = (
        '''Read about how Duolingo works, and how our learning scientists are working to make education fun and accessible to everyone. https://blog.duolingo.com/rss/'''
    )
    conversion_options = {
        'linearize_tables' : False,
        'tags' : 'Duolingo, Linguistics, Education',
    }
    feeds = [
        ("Duolingo Blog", "https://blog.duolingo.com/rss/"),
    ]

    def populate_article_metadata(self, article, __, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
