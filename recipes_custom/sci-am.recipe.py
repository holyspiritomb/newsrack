#!/usr/bin/env python
__license__ = "GPL v3"

# Original at https://github.com/kovidgoyal/calibre/blob/3ad4759cbf9f1ead68c9897ba4ceda5bf5025e6b/recipes/scientific_american.recipe

import os
import sys
import json
import re
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
# from os.path import splitext
from urllib.parse import urljoin

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, parse_date, format_title

from calibre.web.feeds.news import BasicNewsRecipe, prefixed_classes


# convenience switches for when I'm developing
if "runner" in os.environ["recipes_includes"]:
    _masthead_prefix = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos"
else:
    _masthead_prefix = f"file://{os.environ['HOME']}/git/newsrack/recipes_custom/logos"
_masthead = f"{_masthead_prefix}/sci-am.svg"

_name = "Scientific American"
_issue_url = ""


class ScientificAmerican(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    description = (
        "Popular Science. Monthly magazine. Downloaded around the middle of each month. https://www.scientificamerican.com/"
    )
    category = "science"
    __author__ = "Kovid Goyal"
    no_stylesheets = True
    language = "en"
    publisher = "Nature Publishing Group"
    remove_empty_feeds = True
    remove_javascript = True
    timefmt = ": %B %Y"
    remove_attributes = ["width", "height", "style", "decoding", "loading", "fetchpriority", "sizes"]
    # masthead_url = (
    #     "https://static.scientificamerican.com/sciam/assets/Image/newsletter/salogo.png"
    # )
    masthead_url = _masthead
    compress_news_images_auto_size = 2
    extra_css = """
        h1[class^="article_hed-"] { font-size: 1.8rem; margin-bottom: 0.4rem; }
        [class^="article_dek-"] p { font-size: 1.2rem; font-style: italic; margin-bottom: 1rem; }
        [class^="article_authors-"] { padding-left: 0; margin-bottom: 1rem; }
        [class^="lead_image-"] img, [class^="article_image-"] img, [class^="article__image-"] img { max-width: 100%; height: auto; }
        div[class^="lead_image__figcaption"], .t_caption, .caption { font-size: 0.8rem; margin-top: 0.2rem; margin-bottom: 0.5rem; }
        [class^="bio-"], #downloaded_from { font-size:0.8rem; }
        #article_meta{text-transform:uppercase;font-size:0.7em;}
        #article_source{font-size:0.8rem;}
        p.caption{font-size:0.8rem; font-style:italic;}
    """

    needs_subscription = "optional"

    keep_only_tags = [
        prefixed_classes(
            'article_hed- article_dek- article_authors- lead_image- article__content- bio-'
        ),
    ]
    remove_tags = [
        # dict(id=["seeAlsoLinks"]),
        # dict(alt="author-avatar"),
        # prefixed_classes('breakoutContainer- readThisNext- newsletterSignup-'),
        dict(name=['button', 'svg', 'iframe', 'source'])
    ]

    def preprocess_html(self, soup):
        for fig in soup.findAll('figcaption'):
            for p in fig.findAll('p'):
                p.name = 'span'
                p["class"] = ["caption"]
        # for pic in soup.findAll("picture"):
        #     pic.unwrap()
        return soup

    def get_browser(self, *args):
        br = BasicNewsRecipe.get_browser(self)
        if self.username and self.password:
            br.open("https://www.scientificamerican.com/account/login/")
            br.select_form(predicate=lambda f: f.attrs.get("id") == "login")
            br["emailAddress"] = self.username
            br["password"] = self.password
            br.submit()
        return br

    # def get_browser(self, *a, **kw):
    #     kw[
    #         "user_agent"
    #     ] = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
    #     br = BasicNewsRecipe.get_browser(self, *a, **kw)
    #     return br

    def preprocess_raw_html(self, raw_html, url):
        soup = self.soup(raw_html)
        info = self.get_ld_json(soup, lambda d: d.get("dateModified"))
        if info:
            soup.find("h1")["published_at"] = info["datePublished"]
            soup.find("h1")["modified_at"] = info["dateModified"]

        # shift article media to after heading
        article_media = soup.find(class_=re.compile("lead_image-"))
        article_heading = soup.find(class_=re.compile("article_authors-"))
        if article_heading and article_media:
            article_heading.insert_after(article_media)

        for a in soup.findAll("a", attrs={"aria_label": "Open image in new tab"}):
            a.unwrap()
        return str(soup)

    def postprocess_html(self, soup, _):
        hr = soup.new_tag("hr")
        hr["id"] = "end"
        soup.append(hr)
        return soup

    def populate_article_metadata(self, article, soup, _):
        published_ele = soup.find(attrs={"published_at": True})
        if published_ele:
            pub_date = parse_date(published_ele["published_at"])
            article.utctime = pub_date
        #     # pub date is always 1st of the coming month
            # if pub_date > datetime.utcnow().replace(tzinfo=timezone.utc):
                # pub_date = (pub_date - timedelta(days=1)).replace(day=1)
            if not self.pub_date or pub_date > self.pub_date:
                self.pub_date = pub_date
        nyc = ZoneInfo("America/New_York")
        nyc_dt = datetime.astimezone(article.utctime, nyc)
        datestring = datetime.strftime(nyc_dt, "%b %-d, %Y, %-I:%M %p %Z")
        nyc_dt_now = datetime.astimezone(datetime.now(), nyc)
        curr_datestring = datetime.strftime(nyc_dt_now, "%b %-d, %Y at %-I:%M %p %Z")
        article.title = format_title(article.title, nyc_dt)
        self.log.warn('\t', article.title, '\n', article.date, '\n', article.utctime)

        header = soup.new_tag("div")
        header["id"] = "article_meta"
        datetag = soup.new_tag("span")
        datetag["id"] = "date"
        datetag.string = datestring
        head_src = soup.new_tag("a")
        head_src["href"] = article.url
        head_src.string = "Article source"
        header.append(datetag)
        header.append(" | ")
        header.append(head_src)
        headline = soup.find("h1")
        headline.insert_before(header)

        source_link_div = soup.new_tag("div")
        source_link_div["id"] = "article_source"
        source_link = soup.new_tag("a")
        source_link["href"] = article.url
        source_link.string = article.url
        source_link_div.append("This article was downloaded from ")
        source_link_div.append(source_link)
        source_link_div.append(" on ")
        source_link_div.append(curr_datestring)
        source_link_div.append(".")
        hr = soup.new_tag("hr")
        soup.append(hr)
        soup.append(source_link_div)
        toc_img = soup.find("img", attrs={"class": re.compile(r"^lead_image")})
        if toc_img:
            # self.log.warn(toc_img)
            self.add_toc_thumbnail(article, toc_img["src"])

    def parse_index(self):
        # Get the cover, date and issue URL
        fp_soup = self.index_to_soup("https://www.scientificamerican.com")
        curr_issue_link = fp_soup.find(**prefixed_classes('latest_issue_links-'))
        if not curr_issue_link:
            self.abort_recipe_processing("Unable to find issue link")
        issue_url = 'https://www.scientificamerican.com' + curr_issue_link.a["href"]
        # for past editions https://www.scientificamerican.com/archive/issues/
        # issue_url = 'https://www.scientificamerican.com/issue/sa/2024/01-01/'
        soup = self.index_to_soup(issue_url)
        # info = self.get_script_json(soup, "", attrs={"id": "__DATA__"})
        # if not info:
        #     self.abort_recipe_processing("Unable to find script")
        #
        # issue_info = info.get("props", {}).get("pageProps", {}).get("issue", {})
        script = soup.find("script", id="__DATA__")
        if not script:
            self.abort_recipe_processing("Unable to find script")

        JSON = script.contents[0].split('JSON.parse(`')[1].replace("\\\\", "\\")
        data = json.JSONDecoder().raw_decode(JSON)[0]
        issue_info = (
            data
            .get("initialData", {})
            .get("issueData", {})
        )
        if not issue_info:
            self.abort_recipe_processing("Unable to find issue info")

        self.cover_url = issue_info["image_url"] + "?w=800"

        edition_date = datetime.strptime(issue_info["issue_date"], "%Y-%m-%d")
        self.timefmt = f" [{edition_date:%B %Y}]"
        # "%Y-%m-%d"
        # issue_date = self.parse_date(issue_info["issue_date"])
        # self.title = (
        #     f"{_name}: {issue_date:%B %Y} "
        #     f'Vol. {issue_info.get("volume", "")}, Issue {issue_info.get("issue", "")}'
        # )

        feeds = {}
        for section in ("featured", "departments"):
            for article in issue_info.get("article_previews", {}).get(section, []):
                self.log('\t', article["title"])
                if section == "featured":
                    feed_name = "Features"
                else:
                    feed_name = article["category"]
                if feed_name not in feeds:
                    feeds[feed_name] = []
                authors = []
                while len(authors) != len(article["authors"]):
                    for author in article["authors"]:
                        authors.append(author["name"])
                author_final = ""
                if len(authors) == 1:
                    author_final = authors[0]
                else:
                    author_final = authors[0]
                    authors.pop(0)
                    for a in authors:
                        author_final = author_final + ", " + a

                feeds[feed_name].append(
                    {
                        "title": article["title"],
                        "url": urljoin(
                            "https://www.scientificamerican.com/article/",
                            article["slug"],
                        ),
                        "description": article["summary"],
                        "date": article["release_date"],
                        "author": author_final,
                    }
                )

        return feeds.items()
