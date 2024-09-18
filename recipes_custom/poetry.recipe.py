# Copyright (c) 2022 https://github.com/ping/
#
# This software is released under the GNU General Public License v3.0
# https://opensource.org/licenses/GPL-3.0
import os
import os.path
import re
import sys
from collections import OrderedDict
from zoneinfo import ZoneInfo
from urllib.parse import urlparse
from calibre.utils.date import datetime

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe

from calibre.web.feeds.news import BasicNewsRecipe

_issue_url = ""
_name = "Poetry"


class Poetry(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    __author__ = "ping"
    description = (
        '''Founded in Chicago by Harriet Monroe in 1912, Poetry is the oldest monthly devoted to verse in the English-speaking world. https://www.poetryfoundation.org/poetrymagazine'''
    )
    conversion_options = {
        'tags' : 'Poetry, Poetry Magazine, Literature, Periodical',
        'authors' : 'newsrack',
    }
    publication_type = "magazine"
    language = "en"
    encoding = "utf-8"
    remove_javascript = True
    no_stylesheets = True
    auto_cleanup = False
    ignore_duplicate_articles = {"url"}
    compress_news_images = False
    scale_news_images = (800, 1200)
    simultaneous_downloads = 1

    remove_attributes = ["font"]
    keep_only_tags = [
        dict(name="article"),
    ]

    remove_tags = [
        dict(name="button"),
        dict(
            attrs={
                "class": [
                    "c-socialBlocks",
                    "c-index",
                    "o-stereo",
                    "u-hideAboveSmall",
                    "c-slideTrigger",
                    "js-slideshow",
                ]
            }
        ),
        dict(
            attrs={
                "data-dl_module_type": ["Appears In Magazine"]
            }
        ),
        dict(
            attrs={
                "data-dl_element_location": ["sidebar"]
            }
        )
    ]

    extra_css = """
    h1 { font-size: 1.8rem; margin-bottom: 0.5rem; }
    .leading-snug.text-xl { font-size: 1.2rem; font-style: italic; margin-bottom: 1rem; }
    div.type-kappa { font-weight: bold; color: #444; margin-bottom: 1.5rem; }
    div.rich-text.copy-large { margin-bottom: 2rem; }
    #article_date{font-size:0.8rem;text-transform:uppercase;}
    #article_source, .leading-[.7], .text-sm{font-size:0.8rem;}
    """

    def preprocess_html(self, soup):
        for img in soup.select("div.o-mediaEnclosure img"):
            if not img.get("srcset"):
                continue
            img["src"] = self.extract_from_img_srcset(img["srcset"], max_width=1000)
        return soup

    def populate_article_metadata(self, article, soup, _):
        nyc = ZoneInfo("America/New_York")
        nyc_dt = datetime.astimezone(datetime.now(), nyc)
        nyc_now_str = datetime.strftime(nyc_dt, "%b %-d, %Y at %-I:%M %p %Z")

        date_el = soup.new_tag("div")
        date_el["id"] = "article_date"
        nyc_article_dt = datetime.astimezone(article.utctime, nyc)
        datestamp = datetime.strftime(nyc_article_dt, "%b %-d, %Y, %-I:%M %p %Z")
        headlink = soup.new_tag("a")
        headlink["href"] = article.url
        headlink.string = "View on Website"
        date_el.string = f"{article.author} | {datestamp} | "
        date_el.append(headlink)
        if soup.find("span", attrs={"class": "leading-[.7]"}):
            hl = soup.find("span", attrs={"class": "leading-[.7]"})
            if hl.parent:
                headline = hl.parent
            else:
                headline = hl
        else:
            headline = soup.find("h1")
        headline.insert_before(date_el)

        source_link_div = soup.new_tag("div")
        source_link_div["id"] = "article_source"
        source_link = soup.new_tag("a")
        source_link["href"] = article.url
        source_link.string = article.url
        source_link_div.append("This article was downloaded from ")
        source_link_div.append(source_link)
        source_link_div.append(" at ")
        source_link_div.append(nyc_now_str)
        source_link_div.append(".")
        hr = soup.new_tag("hr")
        soup.append(hr)
        soup.append(source_link_div)

    def parse_index(self):
        # commented out bc this doesn't work when there's an issue spanning two months
        # nr_soup = self.index_to_soup("https://holyspiritomb.github.io/newsrack/")
        # nr_issue_date = nr_soup.find("li", id="poetry").find("span", class_="title").string[8:]
        if _issue_url:
            soup = self.index_to_soup(_issue_url)
        else:
            soup = self.index_to_soup("https://www.poetryfoundation.org/poetrymagazine")
            current_issue = soup.select("a[href*='issue']")
            # self.log(current_issue[0])
            if not current_issue:
                self.abort_recipe_processing("Unable to find latest issue")
            current_issue = current_issue[0]
            current_issue_link = "https://www.poetryfoundation.com" + current_issue["href"]
            soup = self.index_to_soup(current_issue_link)
        issue_edition = self.tag_to_string(soup.find("h1"))
        # Setting verbose will force a regeneration
        # if self.verbose is not True:
        #     if issue_edition == nr_issue_date:
        #         self.abort_recipe_processing("We have this issue already.")
        self.title = f"{_name}: {issue_edition}"
        try:
            self.pub_date = self.parse_date(issue_edition)
            # self.pub_date = datetime.strptime(issue_edition, "%B %Y").replace(
                # tzinfo=timezone.utc
            # )
        except ValueError:
            # 2-month issue e.g. "July/August 2021"
            mobj = re.match(
                r"(?P<mth>\w+)/\w+ (?P<yr>\d{4})", issue_edition, re.IGNORECASE
            )
            if not mobj:
                self.abort_recipe_processing("Unable to parse issue date")
            self.pub_date = self.parse_date(f'{mobj.group("mth")} {mobj.group("yr")}')
            # self.pub_date = datetime.strptime(
                # f'{mobj.group("mth")} {mobj.group("yr")}', "%B %Y"
            # ).replace(tzinfo=timezone.utc)

        # cover_image = soup.select("img[alt*='poetry cover']")
        cover_image = soup.select("meta[property='og:image']")[0]
        parsed_cover_url = urlparse(
            cover_image["content"].split("?")[0]
        )
        self.cover_url = f"{parsed_cover_url.scheme}://{parsed_cover_url.netloc}{parsed_cover_url.path}"
        # bod = soup.select("div#mainContent")[0]
        # self.log(bod.prettify())

        sectioned_feeds = OrderedDict()

        # tabs = soup.find_all("div", attrs={"class": "c-tier_tabbed"})
        tabs = soup.find_all("div", attrs={"class": "print:hidden"})
        for tab in tabs:
            tab_title = tab.find("span", attrs={"class": "md:leading-loose"})
            tab_content = tab.find("div")
            if not (tab_title and tab_content):
                continue
            tab_title = self.tag_to_string(tab_title)
            sectioned_feeds[tab_title] = []
            for li in tab_content.select("ul > li.col-span-full"):
                author = self.tag_to_string(
                    li.find("span", attrs={"class": "type-attribution"})
                )
                for link in li.find_all("a"):
                    self.log("Found article:", self.tag_to_string(link))
                    sectioned_feeds[tab_title].append(
                        {
                            "title": self.tag_to_string(link),
                            "url": "https://www.poetryfoundation.com" + link["href"],
                            "author": author,
                            "description": author,
                        }
                    )

        return sectioned_feeds.items()
