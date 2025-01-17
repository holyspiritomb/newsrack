"""
nautil.us
"""
# Original from https://github.com/kovidgoyal/calibre/blob/946ae082e1291f61d88638ff3f3723df591da835/recipes/nautilus.recipe
import os
import sys
from urllib.parse import urljoin

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title

from calibre.web.feeds.news import BasicNewsRecipe, classes

# convenience switches for when I'm developing
if "runner" in os.environ["recipes_includes"]:
    _masthead_prefix = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos"
else:
    _masthead_prefix = f"file://{os.environ['HOME']}/git/newsrack/recipes_custom/logos"
_masthead = f"{_masthead_prefix}/nautilus.svg"

_name = "Nautilus"


class Nautilus(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    language = "en"
    __author__ = "unkn0wn"
    oldest_article = 14  # days
    max_articles_per_feed = 50
    description = (
        '''Nautilus is a different kind of science magazine. Our stories take you into the depths of science and spotlight its ripples in our lives and cultures. We believe any subject in science, no matter how complex, can be explained with clarity and vitality. https://nautil.us/'''
    )
    conversion_options = {
        'tags' : 'Science, Nautilus, Periodical',
        'authors' : 'newsrack',
    }
    use_embedded_content = False
    masthead_url = _masthead
    remove_attributes = ["height", "width"]
    ignore_duplicate_articles = {"title", "url"}
    remove_empty_feeds = True

    compress_news_images_auto_size = 10

    keep_only_tags = [classes("article-left-col feature-image article-content")]

    remove_tags = [
        classes(
            "article-action-list article-bottom-newsletter_box main-post-comments-toggle-wrap main-post-comments-wrapper social-share supported-one article-collection_box"
        )
    ]
    extra_css = """
    .breadcrumb div { margin-right: 0.5rem; }
    h1.article-title { font-size: 1.8rem; margin-bottom: 0.4rem; }
    .article-left-col p { font-size: 1.2rem; font-style: italic; margin-bottom: 1rem; }
    .article-meta {  margin-bottom: 1rem; }
    .article-meta div { display: inline-block; font-weight: bold; color: #444; margin-right: 0.5rem; }
    .article-meta div:last-child { font-weight: normal; }
    div.wp-block-image div { font-size: 0.8rem; }
    blockquote.wp-block-quote { font-size: 1.25rem; margin-left: 0; text-align: center; }
    div.feature-image img, div.wp-block-image img { display: block; max-width: 100%; height: auto; }
    .article-author { margin-top: 2rem; border-top: solid 1px; padding-top: 0.5rem; font-style: italic; }
    .breadcrumb { font-size:0.8rem; text-transform:uppercase;}
    """

    def get_feeds(self):
        soup = self.index_to_soup("https://nautil.us/")
        topics = soup.find_all(
            name="a",
            attrs={"data-ev-act": "topics", "data-ev-label": True, "href": True},
        )
        if not topics:
            return self.feeds
        feeds = [(t["data-ev-label"], urljoin(t["href"], "feed/")) for t in topics]
        return feeds

    def parse_feeds(self):
        feeds = BasicNewsRecipe.parse_feeds(self)
        for feed in feeds:
            for article in feed.articles[:]:
                if 'OBESITY' in article.title.upper() or 'WEIGHT LOSS' in article.title.upper():
                    self.log.warn(f"removing {article.title} from feed")
                    feed.articles.remove(article)
        return feeds

    def populate_article_metadata(self, article, soup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
        srclink = soup.new_tag("a")
        srclink["href"] = article.url
        srclink.append("View on Website")
        breadcrumb = soup.find(attrs={"class": "breadcrumb"})
        if breadcrumb:
            breadcrumb.append(srclink)

    def preprocess_html(self, soup):
        breadcrumb = soup.find("ul", attrs={"class": "breadcrumb"})
        if breadcrumb:
            for li in breadcrumb.find_all("li"):
                li.name = "span"
                li.append(" | ")
            breadcrumb.name = "div"

        byline = soup.find("ul", attrs={"class": "article-list_item-byline"})
        if byline:
            byline["class"] = "article-meta"
            for li in byline.find_all("li"):
                li.name = "div"
            byline.name = "div"

        author_names = soup.find_all("h6", attrs={"class": "article-author-name"})
        for a in author_names:
            a.name = "div"

        # remove empty p tags
        for p in soup.find_all("p"):
            if len(p.get_text(strip=True)) == 0:
                p.decompose()

        for img in soup.findAll("img", attrs={"data-src": True}):
            img["src"] = img["data-src"].split("?")[0]

        # convert author ul/li
        for ul in soup.find_all("ul", class_="article-author"):
            for li in ul.find_all("li", class_="article-author-box"):
                for p in li.find_all("p"):
                    p.name = "div"
                li.name = "div"
            ul.name = "div"

        return soup
