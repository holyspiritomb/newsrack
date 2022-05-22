# Original at https://github.com/kovidgoyal/calibre/blob/29cd8d64ea71595da8afdaec9b44e7100bff829a/recipes/nature.recipe

import re
from collections import defaultdict
from datetime import datetime, timezone
from calibre.web.feeds.news import BasicNewsRecipe

BASE = "https://www.nature.com"


def absurl(url):
    if url.startswith("/"):
        url = BASE + url
    elif url.startswith("http://"):
        url = "https" + url[4:]
    return url


def check_words(words):
    return lambda x: x and frozenset(words.split()).intersection(x.split())


def has_all_of(words):
    return lambda x: x and frozenset(words.split()).issubset(x.split())


class Nature(BasicNewsRecipe):
    title = "Nature"
    __author__ = "Jose Ortiz"
    description = (
        "Nature is a weekly international multidisciplinary scientific journal"
        " publishing peer-reviewed research in all fields of science and"
        " technology on the basis of its originality, importance,"
        " interdisciplinary interest, timeliness, accessibility, elegance and"
        " surprising conclusions.  Nauture also provides rapid, authoritative,"
        " insightful and arresting news and interpretation of topical and coming"
        " trends affecting science, scientists and the wider public."
    )
    language = "en"
    encoding = "UTF-8"
    masthead_url = "https://media.springernature.com/full/nature-cms/uploads/product/nature/header-86f1267ea01eccd46b530284be10585e.svg"

    no_javascript = True
    no_stylesheets = True
    compress_news_images = True
    scale_news_images = (800, 1200)
    # scale_news_images_to_device = False  # force img to be resized to scale_news_images
    timeout = 20
    timefmt = ""
    pub_date = None  # custom publication date

    keep_only_tags = [dict(name="article")]

    remove_tags = [
        dict(attrs={"class": ["u-hide-print", "hide-print", "c-latest-content__item"]}),
        dict(
            name="img",
            attrs={"class": ["visually-hidden"]},
        ),
    ]

    extra_css = """
    h1.c-article-magazine-title { font-size: 1.8rem; margin-bottom: 0.5rem; }
    h2.c-article-teaser-text { font-size: 1.2rem; font-style: italic; margin-bottom: 1rem; }
    div.c-article-identifiers .c-article-identifiers__item { display: inline-block; font-weight: bold; color: #444; }
    div.c-article-identifiers .c-article-identifiers__item time { font-weight: normal; }
    .c-article-author-list .c-author-list__item { font-weight: bold; color: #444; }
    .c-article-body { margin-top: 1rem; }
    p.figure__caption { font-size: 0.8rem; margin-top: 0.2rem; }
    .figure img { max-width: 100%; height: auto; }
    """

    def publication_date(self):
        return self.pub_date

    def populate_article_metadata(self, article, soup, _):
        article_identifiers = soup.find_all(
            attrs={"class": "c-article-identifiers__item"}
        )
        for i in article_identifiers:
            t = i.find(name="time")
            if not t:
                continue
            pub_date_utc = datetime.strptime(t.text, "%d %B %Y").replace(
                tzinfo=timezone.utc
            )
            article.utctime = pub_date_utc
            if not self.pub_date or pub_date_utc > self.pub_date:
                self.pub_date = pub_date_utc
                # self.title = f"Nature: {pub_date_utc:%-d %b, %Y}"

    def preprocess_html(self, soup):
        if soup.find(name="h2", id="access-options"):
            # paid access required
            self.abort_article("Subscription required")

        article_identifier = soup.find(
            name="ul", attrs={"class": "c-article-identifiers"}
        )
        if article_identifier:
            for li in article_identifier.find_all(name="li"):
                li.name = "div"
            article_identifier.name = "div"

        article_authors = soup.find(name="ul", attrs={"class": "c-article-author-list"})
        if article_authors:
            for li in article_authors.find_all(name="li") or []:
                li.name = "div"
                a = li.find(name="a")
                if a:
                    a.unwrap()
            article_authors.name = "div"

        subheadline = soup.find(name="div", attrs={"class": "c-article-teaser-text"})
        if subheadline:
            subheadline.name = "h2"

        for img in soup.findAll("img", {"data-src": True}):
            if img["data-src"].startswith("//"):
                img["src"] = "https:" + img["data-src"]
            else:
                img["src"] = img["data-src"]
        for div in soup.findAll(
            "div", {"data-component": check_words("article-container")}
        )[1:]:
            div.extract()
        return soup

    def parse_index(self):
        soup = self.index_to_soup(BASE + "/nature/current-issue")
        self.cover_url = (
            "https:"
            + soup.find("img", attrs={"data-test": check_words("issue-cover-image")})[
                "src"
            ]
        )
        try:
            self.cover_url = self.cover_url.replace(
                "w200", "w1000"
            )  # enlarge cover size resolution
        except:
            """
            failed, img src might have changed, use default width 200
            """
            pass

        title_div = soup.find(attrs={"data-container-type": "title"})
        if title_div:
            mobj = re.search(
                r"Volume \d+ Issue \d+, (?P<issue_date>\d+ [a-z]+ \d{4})",
                self.tag_to_string(title_div),
                re.IGNORECASE,
            )
            if mobj:
                issue_date = datetime.strptime(mobj.group("issue_date"), "%d %B %Y")
                self.title = f"Nature: {issue_date:%-d %b, %Y}"

        section_tags = soup.find(
            "div", {"data-container-type": check_words("issue-section-list")}
        )
        section_tags = section_tags.findAll(
            "div", {"class": check_words("article-section")}
        )

        sections = defaultdict(list)
        ordered_sec_titles = []
        index = []

        for sec in section_tags:
            sec_title = self.tag_to_string(sec.find("h2"))
            ordered_sec_titles.append(sec_title)
            for article in sec.findAll("article"):
                try:
                    url = absurl(
                        article.find("a", {"itemprop": check_words("url")})["href"]
                    )
                except TypeError:
                    continue
                title = self.tag_to_string(
                    article.find("h3", {"itemprop": has_all_of("name headline")})
                )
                date = (
                    " ["
                    + self.tag_to_string(
                        article.find("time", {"itemprop": check_words("datePublished")})
                    )
                    + "]"
                )
                author = self.tag_to_string(
                    article.find("li", {"itemprop": check_words("creator")})
                )
                description = (
                    self.tag_to_string(
                        article.find(attrs={"data-test": check_words("article.type")})
                    )
                    + " • "
                )
                description += self.tag_to_string(
                    article.find("div", attrs={"itemprop": check_words("description")})
                )
                sections[sec_title].append(
                    {
                        "title": title,
                        "url": url,
                        "description": description,
                        "date": date,
                        "author": author,
                    }
                )

        for k in ordered_sec_titles:
            index.append((k, sections[k]))
        return index
