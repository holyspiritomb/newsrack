#!/usr/bin/env python
__license__ = "GPL v3"

# Original at https://github.com/kovidgoyal/calibre/blob/29cd8d64ea71595da8afdaec9b44e7100bff829a/recipes/scientific_american.recipe

import os
import sys
import json
import re
from datetime import datetime, timezone, timedelta
from os.path import splitext
from urllib.parse import urljoin

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, parse_date

from calibre.web.feeds.news import BasicNewsRecipe, prefixed_classes


_name = "Scientific American"
_issue_url = ""


class ScientificAmerican(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    description = (
        "Popular Science. Monthly magazine. Downloaded around the middle of each month. "
        "https://www.scientificamerican.com/"
    )
    category = "science"
    __author__ = "Kovid Goyal"
    language = "en"
    publisher = "Nature Publishing Group"
    masthead_url = (
        "https://static.scientificamerican.com/sciam/assets/Image/newsletter/salogo.png"
    )
    compress_news_images_auto_size = 2

    remove_attributes = ["width", "height", "style", "decoding", "loading", "fetchpriority", "sizes"]
    keep_only_tags = [
        prefixed_classes(
            'article_hed- article_dek- article_authors- lead_image- article__content- bio-'
        ),
    ]
    remove_tags = [
        dict(id=["seeAlsoLinks"]),
        dict(alt="author-avatar"),
        dict(name=['button', 'svg', 'iframe', 'source']),
    ]

    extra_css = """
        [class^="article_dek-"] { font-style:italic; color:#202020; }
        [class^="article_authors-"] {font-size:small; color:#202020; }
        [class^="article__image-"] { font-size:small; text-align:center; }
        [class^="lead_image-"] { font-size:small; text-align:center; }
        [class^="bio-"], #downloaded_from { font-size:small; color:#404040; }
        em { color:#202020; }
    """

    def get_browser(self, *a, **kw):
        kw[
            "user_agent"
        ] = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        br = BasicNewsRecipe.get_browser(self, *a, **kw)
        return br

    def preprocess_raw_html(self, raw_html, url):
        soup = self.soup(raw_html)
        art_json = soup.find("script", attrs={"type": "application/ld+json"})
        if art_json:
            info = json.loads(art_json.string)
            soup.find("h1")["modified_at"] = info["dateModified"]
            soup.find("h1")["published_at"] = info["datePublished"]
        for a in soup.findAll("a", attrs={"aria_label": "Open image in new tab"}):
            a.unwrap()
        return str(soup)

    def preprocess_html(self, soup):
        for fig in soup.findAll('figcaption'):
            for p in fig.findAll('p'):
                p.name = 'span'
                p["class"] = ["caption"]
        for pic in soup.findAll("picture"):
            pic.unwrap()
        return soup

    def postprocess_html(self, soup, first_fetch):
        hr = soup.new_tag("hr")
        hr["id"] = "end"
        soup.append(hr)
        return soup

    def populate_article_metadata(self, article, soup, first):
        published_ele = soup.find(attrs={"published_at": True})
        if published_ele:
            pub_date = parse_date(published_ele["published_at"])
            article.utctime = pub_date
            # pub date is always 1st of the coming month
            if pub_date > datetime.utcnow().replace(tzinfo=timezone.utc):
                pub_date = (pub_date - timedelta(days=1)).replace(day=1)
            if not self.pub_date or pub_date > self.pub_date:
                self.pub_date = pub_date
        source_div = soup.new_tag("div")
        source_div["id"] = "downloaded_from"
        article_link = soup.new_tag("a")
        article_link["href"] = article.url
        article_link.string = article.url
        current_dt = datetime.now(tz=timezone.utc)
        current_dt_str = datetime.strftime(current_dt, "%-d %B %Y, %-I:%M %p %Z")
        source_div.append("This article was downloaded from ")
        source_div.append(article_link)
        source_div.append(f" at {current_dt_str}")
        source_div.append(".")
        hr = soup.find("hr", attrs={"id": "end"})
        hr.insert_after(source_div)
        toc_img = soup.find("img", attrs={"class": re.compile(r"^lead_image")})
        if toc_img:
            self.log.warn(toc_img)
            self.add_toc_thumbnail(article, toc_img["src"])

    def parse_index(self):
        if not _issue_url:
            fp_soup = self.index_to_soup("https://www.scientificamerican.com")
            curr_issue_link = fp_soup.select(".tout_current-issue__cover a")
            if not curr_issue_link:
                self.abort_recipe_processing("Unable to find issue link")
            issue_url = curr_issue_link[0]["href"]
        else:
            issue_url = _issue_url

        soup = self.index_to_soup(issue_url)
        script = soup.find("script", id="__NEXT_DATA__")
        if not script:
            self.abort_recipe_processing("Unable to find script")

        issue_info = (
            json.loads(script.contents[0])
            .get("props", {})
            .get("pageProps", {})
            .get("issue", {})
        )
        if not issue_info:
            self.abort_recipe_processing("Unable to find issue info")

        image_id, ext = splitext(issue_info["image"])
        self.cover_url = f"https://static.scientificamerican.com/sciam/cache/file/{image_id}_source{ext}?w=960"

        # "%Y-%m-%d"
        issue_date = self.parse_date(issue_info["issue_date"])
        self.title = (
            f"{_name}: {issue_date:%B %Y} "
            f'Vol. {issue_info.get("volume", "")}, Issue {issue_info.get("issue", "")}'
        )

        feeds = {}
        for section in ("featured", "departments"):
            for article in issue_info.get("article_previews", {}).get(section, []):
                if section == "featured":
                    feed_name = "Features"
                else:
                    feed_name = article["category"]
                if feed_name not in feeds:
                    feeds[feed_name] = []
                feeds[feed_name].append(
                    {
                        "title": article["title"],
                        "url": urljoin(
                            "https://www.scientificamerican.com/article/",
                            article["slug"],
                        ),
                        "description": article["summary"],
                    }
                )

        return feeds.items()
