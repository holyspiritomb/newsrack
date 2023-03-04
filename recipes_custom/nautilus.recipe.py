"""
nautil.us
"""
# Original from https://github.com/kovidgoyal/calibre/blob/946ae082e1291f61d88638ff3f3723df591da835/recipes/nautilus.recipe
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

_name = "Nautilus"


class Nautilus(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    language = "en"
    __author__ = "unkn0wn"
    oldest_article = 45  # days
    max_articles_per_feed = 50
    description = (
        '''Nautilus is a different kind of science magazine. Our stories take you into the depths of science and spotlight its ripples in our lives and cultures. We believe any subject in science, no matter how complex, can be explained with clarity and vitality. https://nautil.us/'''
    )
    use_embedded_content = False
    masthead_url = "https://assets.nautil.us/13891_bb83b72bf545e376f3ff9443bda39421.png"
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
    """

    feeds = [
        ("Anthropology", "https://nautil.us/topics/anthropology/feed/"),
        ("Arts", "https://nautil.us/topics/arts/feed/"),
        ("Astronomy", "https://nautil.us/topics/astronomy/feed/"),
        ("Communication", "https://nautil.us/topics/communication/feed/"),
        ("Economics", "https://nautil.us/topics/economics/feed/"),
        ("Environment", "https://nautil.us/topics/environment/feed/"),
        ("Evolution", "https://nautil.us/topics/evolution/feed/"),
        ("Genetics", "https://nautil.us/topics/genetics/feed/"),
        ("Geoscience", "https://nautil.us/topics/geoscience/feed/"),
        ("Health", "https://nautil.us/topics/health/feed/"),
        ("History", "https://nautil.us/topics/history/feed/"),
        ("Math", "https://nautil.us/topics/math/feed/"),
        ("Microbiology", "https://nautil.us/topics/microbiology/feed/"),
        ("Neuroscience", "https://nautil.us/topics/neuroscience/feed/"),
        ("Paleontology", "https://nautil.us/topics/paleontology/feed/"),
        ("Philosophy", "https://nautil.us/topics/philosophy/feed/"),
        ("Physics", "https://nautil.us/topics/physics/feed/"),
        ("Psychology", "https://nautil.us/topics/psychology/feed/"),
        ("Sociology", "https://nautil.us/topics/sociology/feed/"),
        ("Technology", "https://nautil.us/topics/technology/feed/"),
        ("Zoology", "https://nautil.us/topics/zoology/feed/"),
    ]

    def populate_article_metadata(self, article, __, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)

    def get_cover_url(self):
        soup = self.index_to_soup("https://nautil.us/shop/category/issues/")
        div = soup.find("li", **classes("product"))
        if div:
            self.cover_url = (
                div.find("img", attrs={"srcset": True})["srcset"]
                .split(",")[0]
                .split()[0]
            )
        return getattr(self, "cover_url", self.cover_url)

    def preprocess_html(self, soup):
        breadcrumb = soup.find("ul", attrs={"class": "breadcrumb"})
        if breadcrumb:
            for li in breadcrumb.find_all("li"):
                li.name = "div"
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
        return soup
