import os
import json
import sys
import re

from collections import OrderedDict
from datetime import date, datetime, timezone

from calibre.web.feeds.news import BasicNewsRecipe
# from calibre.utils.date import utcnow, strptime, strftime
from calibre import browser
from calibre.ebooks.BeautifulSoup import BeautifulSoup

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import format_title, parse_date, BasicNewsrackRecipe

# # convenience switches for when I'm developing
# if "runner" in os.environ["recipes_includes"]:
#     _masthead_prefix = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos"
#     _oldest_article = 60
# else:
#     _masthead_prefix = f"file://{os.environ['HOME']}/git/newsrack/recipes_custom/logos"
#     _oldest_article = 60
#
# _masthead = f"{_masthead_prefix}/jewish-currents.svg"

_name = "Jewish Currents"


class JewishCurrents(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    __author__ = "holyspiritomb"
    language = "en"
    publication_type = 'magazine'
    oldest_article = 60
    request_as_gbot = True
    masthead_url = "https://jewishcurrents.org/img/jewish-currents.svg"
    resolve_internal_links = True
    use_embedded_content = False
    remove_empty_feeds = True
    remove_javascript: False
    max_articles_per_feed = 30
    no_stylesheets = True
    auto_cleanup = False
    recursions = 0
    browser_type = "webengine"
    simultaneous_downloads = 2
    # delay = 5
    description = (
        '''Breaking news, analysis, art, and culture from a progressive Jewish perspective. https://jewishcurrents.org'''
    )
    conversion_options = {
        'tags' : 'Jewish Currents, Jewish, Politics, News',
        'authors' : 'newsrack',
    }
    keep_only_tags = [
        dict(name="div", attrs={"id": "content"})
    ]

    feeds = [
        ("Articles", "https://jewishcurrents.org/feed"),
    ]

    remove_tags = [
        dict(name="div", attrs={"id": "letters"}),
        dict(name="div", attrs={"class": "footblurb"}),
        dict(name="div", attrs={"class": "social"}),
        dict(attrs={"class": "hidden"}),
        dict(name="svg", attrs={"height": False}),
        dict(name="script", attrs={"type": False}),
        dict(name="script", attrs={"type": "text/javascript"}),
        dict(name="script", attrs={"src": True}),
        dict(name="iframe"),
        dict(name="footer"),
    ]

    remove_attributes = ["style"]

    extra_css = '''
        * {
            font-family: "InterVar", Lato, "Readex Pro Light", sans-serif;
        }
        img {
            max-width: 98vw;
            height: auto;
        }

        .image-caption p, img + div p {
            font-size: 0.8rem;
            font-style: italic;
            font-family: "InterVar", Lato, "Readex Pro Light", sans-serif;
        }
        .image-credit, .image-caption span.opacity-50, img + div + div{
            font-size: 0.7rem;
            font-style: italic;
            font-family: "InterVar", Lato, "Readex Pro Light", sans-serif;
        }

        .bodytext p:not(.pullquote) {
            font-size: 1rem;
            font-family: "InterVar", Lato, "Readex Pro Light", sans-serif;
        }

        p.pullquote {
            font-size: 1.3rem;
            font-family: serif;
            font-style: italic;
            font-weight: bold;
            text-align: center;
            padding-left: 10vw;
            padding-right: 10vw;
        }

        .bioblock p, .bioblock span, #downloaded_from, #footnotes span, #footnotes p {
            font-size: 0.8rem;
            font-family: "InterVar", Lato, "Readex Pro Light", sans-serif;
        }

        #category_date, #article_updated {
            font-size:0.8rem;
            text-transform: uppercase;
            font-family: "InterVar", Lato, "Readex Pro Light", sans-serif;
        }
        #article_updated {font-weight: bold}
        '''

    def google_cache_uri(self, uri):
        g_uri = f"https://webcache.googleusercontent.com/search?q=cache:{uri}"
        return g_uri

    def ungoogle_uri(self, uri: str):
        ungoogled_uri = uri.removeprefix("https://webcache.googleusercontent.com/search?q=cache:")
        return ungoogled_uri

    def populate_article_metadata(self, article, soup, _):
        toc_thumb = soup.find("img", attrs={"id": "toc_thumb"})
        if toc_thumb:
            thumb_src = toc_thumb["src"]
            self.add_toc_thumbnail(article, thumb_src)
        content = soup.find("div", attrs={"id": "content"})
        article_pubdate_str = content["data-pub"]
        article_mod_str = content["data-mod"]
        pub_dt = parse_date(article_pubdate_str)
        mod_dt = parse_date(article_mod_str)
        if pub_dt == mod_dt:
            article_dt = pub_dt
        else:
            article_dt = mod_dt
        subhead = soup.find(attrs={"id": "article_subhead"})
        if subhead:
            article.description = self.tag_to_string(subhead)
        if "googleusercontent" in article.url:
            article_url = self.ungoogle_uri(article.url)
        else:
            article_url = article.url
        date_el = soup.find(attrs={"id": "article_date"})
        if date_el:
            date_el.string = date.strftime(pub_dt, "%-d %b %Y, %-I:%M %p %Z")
            if pub_dt != mod_dt:
                mod_span = soup.new_tag("span")
                mod_span["id"] = "article_updated"
                mod_span.string = date.strftime(mod_dt, "Updated %-d %b %Y, %-I:%M %p %Z")
                date_el.parent.insert_after(mod_span)
            url_el = soup.new_tag("a")
            url_el.string = "View on Website"
            url_el["href"] = article.url
            date_el.parent.append(" | ")
            date_el.parent.append(url_el)
        bioblock = soup.findAll(attrs={"class": "bioblock"})[-1]
        source_div = soup.new_tag("div")
        source_div["id"] = "downloaded_from"
        article_link = soup.new_tag("a")
        article_link["href"] = article_url
        article_link.string = article_url
        current_dt = datetime.now(tz=timezone.utc)
        current_dt_str = date.strftime(current_dt, "%-d %B %Y, %-I:%M %p %Z")
        source_div.append("This article was downloaded from ")
        if "googleusercontent" in article.url:
            source_div.append("google's cached page for ")
        source_div.append(article_link)
        source_div.append(f" at {current_dt_str}")
        source_div.append(".")
        hr = soup.new_tag("hr")
        bioblock.insert_after(source_div)
        bioblock.insert_after(hr)
        article.utctime = article_dt
        article.date = article_dt
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)

    def preprocess_raw_html(self, raw_html, url):
        soup = BeautifulSoup(raw_html, from_encoding='utf-8')
        for div in soup.findAll("div", attrs={"class": "bodytext"}):
            div["class"] = ["bodytext"]
        for div in soup.findAll("div", attrs={"class": "typography"}):
            div["class"] = ["typography"]
        for div in soup.findAll("div", attrs={"class": "footnotes"}):
            div["class"] = ["footnotes"]
        footnotes = soup.findAll("div", attrs={"class": "footnotes"})
        if footnotes:
            footnotes_container = soup.new_tag("div")
            footnotes_container["id"] = "footnotes"
            footnotes_heading = soup.new_tag("h4")
            footnotes_heading["id"] = "footnotes_header"
            footnotes_heading.string = "Footnotes"
            footnotes_container.append(footnotes_heading)
            footnotes[0].insert_before(footnotes_container)
            footnotes_container = soup.find("div", attrs={"id": "footnotes"})
            for fn in footnotes:
                fn.extract()
                footnotes_container.append(fn)
            for div in footnotes_container.findAll("div", attrs={"id": False}):
                if "footnotes" not in div["class"]:
                    div.unwrap()
        json_info = soup.find("script", attrs={"type": "application/ld+json"})
        article_data = json.loads(json_info.string)
        article_url = article_data["@graph"][0]["mainEntityOfPage"]
        article_pubdate_str = article_data["@graph"][0]["datePublished"]
        article_mod_str = article_data["@graph"][0]["dateModified"]
        content = soup.find("div", attrs={"id": "content"})
        content["data-pub"] = article_pubdate_str
        content["data-mod"] = article_mod_str
        content["data-url"] = article_url
        json_info.extract()
        for js in soup.findAll("script"):
            js.decompose()
        headline = content.find("h1")
        headline["id"] = "article_headline"
        headline["class"] = ["headline"]
        lockup = content.find("div", attrs={"class": "lockup"})
        if lockup:
            lockup["class"] = ["lockup"]
            date_el = lockup.find("div", string=re.compile(r"[0-9]{4}$"))
            if date_el:
                date_el["id"] = "article_date"
            head_authors = lockup.findAll("a", href=re.compile("author"))
            for auth in head_authors:
                auth["class"] = "header-author"
            subhead = lockup.find("h2")
            if subhead:
                subhead["id"] = "article_subhead"
                subhead["class"] = "subhead"
            lockup.extract()
            content.insert(0, lockup)
        for bug_div in soup.findAll("div", attrs={"class": "bug"}):
            bug_div.unwrap()
        img_auth = content.findAll("img", attrs={"data-srcset": True})
        for img in img_auth:
            if "/imager/cloud/authors" in img["data-srcset"]:
                img.extract()
        date_spans = content.findAll("span", string=re.compile(r"^[A-Z][a-z]* [0-9]+\, [0-9]{4}$"), attrs={"id": False})
        if date_spans:
            for span in date_spans:
                parent_el = span.parent
                span.extract()
                parent_el.smooth()
                for thing in parent_el.contents:
                    if not thing.name:
                        if re.search(r"^\W*$", thing.string):
                            thing.extract()
                if len(parent_el.contents) == 0:
                    parent_el.extract()
        for div in soup.findAll("div", attrs={"id": False, "class": ""}):
            div.unwrap()
        return str(soup)

    def preprocess_html(self, soup):
        content = soup.find("div", attrs={"id": "content"})
        headline = content.find("h1", attrs={"id": "article_headline"})
        date_el = content.find("div", attrs={"id": "article_date"})
        if date_el:
            date_el.name = "span"
            date_el.extract()
        else:
            date_el = soup.new_tag("span")
            date_el["id"] = "article_date"
        tinyheader = soup.new_tag("div")
        tinyheader["id"] = "category_date"
        category_link = content.find("a", href=re.compile(r"jewishcurrents\.org\/category"))
        category_link["id"] = "article_category"
        if "Comic" in category_link.string:
            category_link.string = "Comic"
            category_link.extract()
            tinyheader.append(category_link)
            head_authors = headline.parent.findAll("a", href=re.compile(r"\/author"))
            for auth in head_authors:
                auth["class"] = "header-author"
            # old_date = headline.parent.find("span", string=re.compile(r"^[A-Z][a-z]* [0-9]+\, [0-9]{4}$"))
            # if old_date:
            #     self.log("found old date", old_date)
            #     old_date.extract()
        else:
            category_link.wrap(tinyheader)
        category_link.insert_after(date_el)
        category_link.insert_after(" | ")
        content.insert(0, tinyheader)
        toc_thumb = content.find("img")
        toc_thumb["id"] = "toc_thumb"
        imgcap = toc_thumb.find_next_sibling("div", class_="text-sm")
        if imgcap:
            imgcap["class"] = "image-caption"
        imgcred = toc_thumb.find_next_sibling("div", class_="text-xs")
        if imgcred:
            imgcred["class"] = "image-credit"
        for img in content.findAll("img", attrs={"height": True}):
            del img["height"]
        for img in content.findAll("img", attrs={"width": True}):
            del img["width"]
        bioblocks = soup.findAll(attrs={"class": "bioblock"})
        if bioblocks:
            for bioblock in bioblocks:
                bioblock["class"] = ["bioblock"]
                twitter_handles = bioblock.findAll("a", href=re.compile("twitter"))
                if twitter_handles:
                    for tw in twitter_handles:
                        br = soup.new_tag("br")
                        tw.insert_after(br)
        article_main = content.find("main")
        if article_main:
            hr = soup.new_tag("hr")
            article_main.insert_after(hr)
        pullquotes = content.findAll(class_="pullquote")
        for pq in pullquotes:
            pq["class"] = ["pullquote"]
            pull_par = pq.find("p")
            if pull_par:
                pull_par["class"] = "pullquote"
                pull_par.parent.unwrap()
        return soup
