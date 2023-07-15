import os
import sys
from collections import OrderedDict
from datetime import datetime
from urllib.parse import urljoin
from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre.utils.date import utcnow, parse_date
from calibre.ebooks.BeautifulSoup import BeautifulSoup

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title


_name = "Duolingo Blog"


class Duolingo(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    __author__ = "holyspiritomb"
    language = "en"
    oldest_article = 31  # days
    # max_articles_per_feed = 50
    publication_type = 'blog'
    resolve_internal_links = True
    # use_embedded_content = False
    remove_empty_feeds = True
    remove_javascript = True
    # max_articles_per_feed = 50
    no_stylesheets = True
    remove_attributes = ["style"]
    # recursions = 1
    masthead_url = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos/duolingo.svg"
    description = (
        '''Read about how Duolingo works, and how our learning scientists are working to make education fun and accessible to everyone. Generated from https://blog.duolingo.com'''
    )
    conversion_options = {
        'linearize_tables' : False,
        'tags' : 'Duolingo, Linguistics, Education',
        'authors' : 'Duolingo',
        'change_justification': 'left',
    }
    # feeds = [
        # ("Duolingo Blog", "https://blog.duolingo.com/rss/"),
    # ]

    keep_only_tags = [
        dict(name="main", attrs={'class': 'page-body'}),
    ]

    remove_tags = [
        dict(name="section", attrs={'class': 'related-posts'}),
        dict(name="footer", attrs={'class': 'post-footer'}),
    ]

    extra_css = '''
        * {
            font-family: Lato, "Readex Pro Light", sans-serif;
        }
        table {
            border-collapse: collapse;
            width: 100%;
            border-color: #545b5e;
        }
        td, th {
            border: 1px solid rgb(140, 130, 115);
            padding: 0.7em;
        }
        img {
            max-width: 100%;
            height: auto;
        }
        '''

    BASE_URL = 'https://blog.duolingo.com'

    def populate_article_metadata(self, article, __, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)

    def parse_index(self):
        self.log("running parse_index function")
        soup = self.index_to_soup("https://blog.duolingo.com")
        sectioned_feeds = OrderedDict()
        for article_card in soup.findAll("a", attrs={'class': 'card-link'}):
            card_url = article_card['href']
            card_title = self.tag_to_string(article_card.find("h2", attrs={'class': 'card-title'}))
            section_title = self.tag_to_string(article_card.find("span", attrs={'class': 'tag-token'}))
            if section_title not in sectioned_feeds:
                sectioned_feeds[section_title] = []
            description = None
            auths = self.tag_to_string(article_card.find("span", attrs={'class': 'authors'}))
            article_date = article_card.find("time", attrs={"datetime": True})["datetime"]
            self.log(f"Found article: {section_title}, {card_title}")
            sectioned_feeds[section_title].append(
                {
                    "title": card_title,
                    "url": urljoin(self.BASE_URL, card_url),
                    "description": description,
                    "date": article_date,
                    "author": auths,
                }
            )
        return sectioned_feeds.items()
