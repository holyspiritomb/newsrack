#!/usr/bin/env python

import os
import sys
from collections import OrderedDict
from datetime import datetime
from calibre.web.feeds.news import BasicNewsRecipe

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title

_name = "Strange Horizons"


class StrangeHorizons(BasicNewsrackRecipe, BasicNewsRecipe):
    # Recipe metadata
    title = _name
    description = "A magazine of speculative fiction and related nonfiction. http://strangehorizons.com"
    publication_type = "magazine"
    language = "en"
    __author__ = "Peter Fidelman, based on work by Jim DeVona"
    __version__ = "2.0"
    conversion_options = {
        'tags' : 'Literature, Arts, Strange Horizons, Periodical',
        'authors' : 'newsrack',
    }

    # Cruft filters to apply to each article found by parse_index
    keep_only_tags = [dict(name="div", attrs={"class": "post"})]
    remove_attributes = ['style']
    remove_tags_after = [dict(name="br", attrs={"class": "clear_both"})]
    remove_tags = [
        dict(name="div", attrs={"class": "single-title-header row"}),
        dict(name="div", attrs={"class": "podcast-title"}),
        dict(name="button", attrs={"onclick": "showWarning_enUS()"}),
    ]

    # Styles to apply to each article
    no_stylesheets = True
    extra_css = """
    div.image-left { margin: 0.5em auto 1em auto; }
    div.image-right { margin: 0.5em auto 1em auto; }
    div.illustration { margin: 0.5em auto 1em auto; text-align: center; }
    p.image-caption { margin-top: 0.25em; margin-bottom: 1em; font-size: 75%; text-align: center; }
    h1 { font-size: 160%; }
    h2 { font-size: 110%; }
    h3 { font-size: 85%; }
    div#content-warning-enUS[style]{display:block !important;}
    h4 { font-size: 80%; }
    p { font-size: 90%; margin: 1em 1em 1em 15px; }
    p.author-bio { font-size: 75%; font-style: italic; margin: 1em 1em 1em 15px; }
    p.author-bio i, p.author-bio cite, p.author-bio .foreign { font-style: normal; }
    p.author-copyright { font-size: 75%; text-align: center; margin: 3em 1em 1em 15px; }
    p.content-date { font-weight: bold; }
    p.dedication { font-style: italic; }
    div.stanza { margin-bottom: 1em; }
    div.stanza p { margin: 0px 1em 0px 15px; font-size: 90%; }
    p.verse-line { margin-bottom: 0px; margin-top: 0px; }
    p.verse-line-indent-1 { margin-bottom: 0px; margin-top: 0px; text-indent: 2em; }
    p.verse-line-indent-2 { margin-bottom: 0px; margin-top: 0px; text-indent: 4em; }
    p.verse-stanza-break { margin-bottom: 0px; margin-top: 0px; }
    .foreign { font-style: italic; }
    .thought { font-style: italic; }
    .thought cite { font-style: normal; }
    .thought em { font-style: normal; }
    blockquote { font-size: 90%; font-style: italic; }
    blockquote cite { font-style: normal; }
    blockquote em { font-style: normal; }
    blockquote .foreign { font-style: normal; }
    blockquote .thought { font-style: normal; }
    .speaker { font-weight: bold; }
    pre { margin-left: 15px; }
    div.screenplay { font-family: monospace; }
    blockquote.screenplay-dialogue { font-style: normal; font-size: 100%; }
    .screenplay p.dialogue-first { margin-top: 0; }
    .screenplay p.speaker { margin-bottom: 0; text-align: center; font-weight: normal; }
    blockquote.typed-letter { font-style: normal; font-size: 100%; font-family: monospace; }
    .no-italics { font-style: normal; }
    """

    def get_date(self):
        frontSoup = self.index_to_soup("http://strangehorizons.com")
        dateDiv = frontSoup.find(
            "div", attrs={"class": "current-issue-widget issue-medium issue"}
        )
        url = dateDiv.a["href"]
        date = url.split('/')[-2]
        return date

    def parse_index(self):
        # Change this to control what issue to grab.  Must be of the format
        # D-month-YYYY; for example, "4-july-2005".  Alternately, use
        # self.get_date() to retrieve the latest issue.

        dateStr = self.get_date()
        issuedate = datetime.strptime(dateStr, '%d-%B-%Y')
        self.title = format_title(_name, issuedate)
        self.log(dateStr)

        issueUrl = "http://strangehorizons.com/issue/%s/" % dateStr
        soup = self.index_to_soup(issueUrl)

        sections = OrderedDict()

        #
        # Each div with class="article" is an article.
        #
        articles = soup.findAll(attrs={"class": "article"})

        for article in articles:
            #
            # What kind of article is this?
            #
            categoryDiv = article.find("div", {"class": "category"})
            categoryStr = self.tag_to_string(categoryDiv.a)
            self.log(categoryStr)

            #
            # Ignore podcasts, as they cannot be converted to text.
            #
            if categoryStr == "Podcasts":
                continue

            #
            # Reviews must be special-cased, as several reviews
            # may be packed into the same div.
            #
            if categoryStr == "Reviews":
                reviews = article.findAll(attrs={"class": "review"})
                for review in reviews:
                    titleDiv = review.find("div", {"class": "title"})
                    titleStr = self.tag_to_string(titleDiv.a).strip()
                    if not titleStr:
                        continue
                    self.log(titleStr)
                    url = titleDiv.a["href"]

                    authorDiv = review.find("div", {"class": "author"})
                    authorStr = self.tag_to_string(authorDiv.a).strip()

                    if categoryStr not in sections:
                        sections[categoryStr] = []
                    sections[categoryStr].append({
                        "title": titleStr,
                        "author": authorStr,
                        "url": url,
                        "description": "",
                        "date": dateStr,
                    })

            #
            # Assume anything else is an ordinary article.  Ought
            # to work for "Fiction", "Poetry", "Articles", etc.
            #
            else:
                titleDiv = article.find("div", {"class": "title"})
                url = titleDiv.a["href"]
                titleStr = self.tag_to_string(titleDiv.a).strip()

                authorDiv = article.find("div", {"class": "author"})
                authorStr = self.tag_to_string(authorDiv.a).strip()

                # The excerpt consistently starts with a
                # comment containing one number.  This comment
                # is not removed by tag_to_string so we must
                # remove it ourself.  We do this by removing
                # the first word of the excerpt.
                excerptDiv = article.find("div", {"class": "excerpt"})
                excerptStr = self.tag_to_string(excerptDiv).strip()
                excerptStr = " ".join(excerptStr.split(" ")[1:])

                if categoryStr not in sections:
                    sections[categoryStr] = []
                sections[categoryStr].append({
                    "title": titleStr,
                    "author": authorStr,
                    "url": url,
                    "description": excerptStr,
                    "date": dateStr,
                })
        return sections.items()


calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
