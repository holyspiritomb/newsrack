import os
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
# from calibre.web.feeds import Feed
from calibre.web.feeds.news import BasicNewsRecipe
from calibre.ebooks.BeautifulSoup import BeautifulSoup

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import WordPressNewsrackRecipe, format_title

# convenience switches for when I'm developing
if "runner" in os.environ["recipes_includes"]:
    _masthead_prefix = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos"
else:
    _masthead_prefix = f"file://{os.environ['HOME']}/git/newsrack/recipes_custom/logos"
_masthead = f"{_masthead_prefix}/TPWKY.jpg"

_name = "This Podcast Will Kill You"


class TPWKY(WordPressNewsrackRecipe, BasicNewsRecipe):
    title = _name
    language = 'en'
    encoding = "utf-8"
    description = u'Shownotes for This Podcast Will Kill You. https://thispodcastwillkillyou.com'
    __author__ = 'holyspiritomb'
    category = 'news, rss'
    oldest_article = 365
    max_articles_per_feed = 50
    remove_empty_feeds = True
    resolve_internal_links = False
    use_embedded_content = True
    masthead_url = _masthead
    # reverse_article_order = False

    # remove_tags =[]

    feeds = [
        ("Shownotes", "https://thispodcastwillkillyou.com/episodes/feed/")
    ]

    remove_attributes = ["height", "width", "style"]

    extra_css = '''
        img{max-width:98vw}
        #article_meta{text-transform:uppercase;font-size:0.7em;}
        p{font-size:1rem}
        #article_source{font-size:0.8rem;}
        '''

    def populate_article_metadata(self, article, soup: BeautifulSoup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)

        nyc = ZoneInfo("America/New_York")
        nyc_dt = datetime.astimezone(article.utctime, nyc)
        datestring = datetime.strftime(nyc_dt, "%b %-d, %Y, %-I:%M %p %Z")
        nyc_dt_now = datetime.astimezone(datetime.now(), nyc)
        curr_datestring = datetime.strftime(nyc_dt_now, "%b %-d, %Y at %-I:%M %p %Z")
        article.title = format_title(article.title, nyc_dt)

        header = soup.new_tag("div")
        header["id"] = "article_meta"
        datetag = soup.new_tag("span")
        datetag["id"] = "date"
        datetag.string = datestring
        head_src = soup.new_tag("a")
        head_src["href"] = article.url
        head_src.string = "Episode Page"
        pod_src = soup.new_tag("a")
        pod_src["href"] = "https://thispodcastwillkillyou.com/"
        ep_href = article.url
        pod_src.string = "Podcast"
        header.append(datetag)
        header.append(" | ")
        header.append(pod_src)
        header.append(" | ")
        header.append(head_src)
        headline = soup.find("h2")
        headline.insert_before(header)

        source_link_div = soup.new_tag("div")
        source_link_div["id"] = "article_source"
        source_link_div.append("This article was downloaded on ")
        source_link_div.append(curr_datestring)
        source_link_div.append(".")
        hr = soup.new_tag("hr")
        soup.append(hr)
        soup.append(source_link_div)

    def preprocess_raw_html(self, raw_html, url):
        soup = BeautifulSoup(raw_html)
        table = soup.find("figure", attrs={"class": "wp-block-table"})
        if table:
            history = soup.new_tag("ul")
            hist_heading = soup.new_tag("h3")
            hist_heading.string = "History"
            history.append(hist_heading)
            for tr in table.find_all("tr"):
                first_td = tr.find("td")
                if self.tag_to_string(first_td) == "History":
                    first_td.extract()
                    continue
                elif self.tag_to_string(first_td) == "":
                    first_td.extract()
                    continue
                first_td.name = "li"
                history.append(first_td)
            bio = soup.new_tag("ul")
            bio_heading = soup.new_tag("h3")
            bio_heading.string = "Biology"
            bio.append(bio_heading)
            for tr in table.find_all("tr"):
                sec_td = tr.find("td")
                if self.tag_to_string(sec_td) == "Biology":
                    tr.extract()
                    continue
                elif self.tag_to_string(sec_td) == "":
                    tr.extract()
                    continue
                sec_td.name = "li"
                bio.append(sec_td)
                tr.extract()
            # table.insert_before(hist_heading)
            table.insert_before(history)
            # table.insert_after(bio_heading)
            table.insert_after(bio)
            table.extract()
            for img in soup.find_all("img"):
                # the quarantini & placeborita recipe card images
                # replace them with links
                new_link_el = soup.new_tag("p")
                a = img.parent
                img_url = a["href"]
                new_link = soup.new_tag("a")
                new_link["href"] = img_url
                if "copy" in img_url:
                    new_link.append("Placeborita")
                elif "placeborita" in img_url:
                    new_link.append("Placeborita")
                elif "quarantini" in img_url:
                    new_link.append("Quarantini")
                else:
                    new_link.string = img_url
                new_link_el.append(new_link)
                img.insert_before(new_link_el)
                img.decompose()
        return str(soup)

    def preprocess_html(self, soup):
        # self.log.warn(soup)
        return soup
