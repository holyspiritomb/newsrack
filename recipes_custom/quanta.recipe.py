# Original at https://raw.githubusercontent.com/kovidgoyal/calibre/1ca6887e6c9f83a05cafe1fba8bae6de9bd2773c/recipes/quanta_magazine.recipe

import os
import sys
from datetime import timezone, timedelta

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title

from calibre.web.feeds.news import BasicNewsRecipe

# convenience switches for when I'm developing
if "runner" in os.environ["recipes_includes"]:
    _masthead_prefix = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos"
else:
    _masthead_prefix = f"file://{os.environ['HOME']}/git/newsrack/recipes_custom/logos"
_masthead = f"{_masthead_prefix}/quanta.svg"

_name = "Quanta Magazine"


class QuantaMagazine(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    __author__ = "lui1"
    description = (
        '''Quanta Magazine is committed to in-depth, accurate journalism that serves the public interest. Each article braids the complexities of science with the malleable art of storytelling and is meticulously reported, edited and fact-checked. https://www.quantamagazine.org/'''
    )
    conversion_options = {
        'tags' : 'Quanta Magazine, Science, News, Periodical',
        'authors' : 'newsrack',
    }
    publication_type = "magazine"
    language = "en"
    encoding = "UTF-8"
    # masthead_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1f/Quanta_Magazine_Logo_05.2022.svg/320px-Quanta_Magazine_Logo_05.2022.svg.png"
    masthead_url = _masthead
    auto_cleanup = False
    use_embedded_content = False

    oldest_article = 30
    max_articles_per_feed = 100

    keep_only_tags = [
        dict(name="div", attrs={"id": "postBody"}),
    ]
    remove_tags = [
        dict(name=["script", "noscript", "style", "svg", "form", "button"]),
        dict(class_=["post__title__actions", "post__sidebar__content", "video"]),
    ]

    extra_css = """
    .component-img img {
        display: block; margin-bottom: 0.3rem; max-width: 100%; height: auto;
        box-sizing: border-box;
    }
    .caption, .attribution { font-size: 0.8rem; margin: 0; }
    .post__title__kicker {font-size: 0.8rem; text-transform: uppercase;}
    """

    feeds = [
        (_name, "https://api.quantamagazine.org/feed/"),
    ]

    def populate_article_metadata(self, article, soup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
        eyebrow = soup.find("div", class_="post__title__kicker")
        eyebrow.append(" | ")
        srclink = soup.new_tag("a")
        srclink["href"] = article.url
        srclink.append("View on Website")
        eyebrow.append(srclink)

    def parse_feeds(self):
        feeds = self.group_feeds_by_date()
        for feed in feeds:
            for article in feed.articles[:]:
                if 'OBESITY' in article.title.upper() or 'WEIGHT LOSS' in article.title.upper():
                    self.log.warn(f"removing {article.title} from feed")
                    feed.articles.remove(article)
        return feeds
