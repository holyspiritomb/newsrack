#!/usr/bin/env python
__license__ = 'GPL v3'
__copyright__ = '2008-2017, Darko Miletic <darko.miletic at gmail.com>'
'''
sciencedaily.com
'''

import os
import re
import sys

from calibre import browser
from calibre.web.feeds.news import BasicNewsRecipe, classes
from calibre.utils.date import utcnow, parse_date

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title


# convenience switches for when I'm developing
if "runner" in os.environ["recipes_includes"]:
    _masthead_prefix = "file:///home/runner/work/newsrack/newsrack/recipes_custom/logos"
    _max_per_feed = 15
    _oldest = 3
else:
    _masthead_prefix = f"file://{os.environ['HOME']}/git/newsrack/recipes_custom/logos"
    _max_per_feed = 1
    _oldest = 7
_masthead = f"{_masthead_prefix}/science-daily.png"


_name = "Science Daily"


class ScienceDaily(BasicNewsrackRecipe, BasicNewsRecipe):
    title = _name
    __author__ = u'Darko Miletic'
    description = ('''ScienceDaily is one of the Internet's most popular science news web sites. Since starting in 1995, the award-winning site has earned the loyalty of students, researchers, healthcare professionals, government agencies, educators and the general public around the world. Now with more than 6 million monthly visitors worldwide, ScienceDaily generates nearly 20 million page views a month and is steadily growing in its global audience. https://www.sciencedaily.com/''')
    conversion_options = {
        'tags' : 'Science, Science Daily, Periodical',
        'authors' : 'newsrack',
    }
    masthead_url = _masthead
    oldest_article = _oldest
    remove_empty_feeds = True
    max_articles_per_feed = _max_per_feed
    use_embedded_content = False
    language = 'en'
    encoding = 'utf-8'
    delay = 3
    publication_type = 'newspaper'
    auto_cleanup = False
    resolve_internal_links = False
    recursions = 0
    remove_tags = [
        classes("logo sharing hr-logo fullstory breaking-list sidebar"),
        dict(id='related_releases'),
        dict(id='related_topics'),
        dict(id='share_top'),
        dict(id='topnav'),
        dict(id='div-gpt-ad-story_bottom'),
        dict(id='div-gpt-ad-story_middle'),
        dict(id='div-gpt-ad-story_top'),
        dict(id='citation_mla'),
        dict(id='citation_chicago'),
        dict(name='ul', attrs={'role': 'tablist'}),
        dict(name='dt', attrs={'class': 'no-print'}),
        dict(name='dd', attrs={'class': 'no-print'}),
        dict(name='div', attrs={'class': 'mobile-top-rectangle'}),
        dict(name='div', attrs={'class': 'display-none'}),
        dict(name='div', attrs={'class': 'mobile-end-rectangle'}),
        dict(name='div', attrs={'class': 'mobile-bottom-rectangle'}),
        dict(name='div', attrs={'class': 'mobile-middle-rectangle'}),
        dict(name='ul', attrs={'class': 'topics'}),
    ]
    remove_tags_before = [
        dict(name='h1', attrs={'id': 'headline'}),

    ]
    remove_tags_after = [
        dict(name='div', attrs={'id': 'citations'}),

    ]
    filter_out = ["obesity", "wegovy", "weight loss"]

    extra_css = """
        dd,dt,
        #abstract,
        #date_posted,
        #source,
        #citations,
        #citation_apa,
        #journal_references,
        #metadata,
        #headersrc
        {
            font-size:0.8rem;
            line-height:normal;
        }
        h1#headline{
            font-size:1.75rem;
            text-align:left;
        }
        h2{
            text-align:left;
            font-size:1.5rem
        }
        p#first{
            font-size:1.25rem;
            text-align:left;
        }
        #text > p{
            font-size: 1rem;
            text-align:left;
        }
    """

    # Feed are found here: https://www.sciencedaily.com/newsfeeds.htm
    feeds = [
        # (u'Top News', u'https://www.sciencedaily.com/rss/top.xml'),
        # (u'Top Health', u'https://www.sciencedaily.com/rss/top/health.xml'),
        # (u'Top Technology', u'https://www.sciencedaily.com/rss/top/technology.xml'),
        # (u'Top Society', u'https://www.sciencedaily.com/rss/top/society.xml'),
        ("ADHD", "https://www.sciencedaily.com/rss/mind_brain/add_and_adhd.xml"),
        ("Alzheimer's", "https://www.sciencedaily.com/rss/mind_brain/alzheimer's.xml"),
        ("Autism", "https://www.sciencedaily.com/rss/mind_brain/autism.xml"),
        ("Behavior", "https://www.sciencedaily.com/rss/mind_brain/behavior.xml"),
        ("Computers and Math", "https://www.sciencedaily.com/rss/computers_math.xml"),
        ("Dyslexia", "https://www.sciencedaily.com/rss/mind_brain/dyslexia.xml"),
        ("Earth and Climate", "https://www.sciencedaily.com/rss/earth_climate.xml"),
        ("Eating Disorders", "https://www.sciencedaily.com/rss/health_medicine/eating_disorders.xml"),
        ("Education and Learning", "https://www.sciencedaily.com/rss/education_learning.xml"),
        ("Fossils and Ruins", "https://www.sciencedaily.com/rss/fossils_ruins.xml"),
        ("Gender Difference", "https://www.sciencedaily.com/rss/mind_brain/gender_difference.xml"),
        ("Health and Medicine", "https://www.sciencedaily.com/rss/health_medicine.xml"),
        ("IBS", "https://www.sciencedaily.com/rss/health_medicine/irritable_bowel_syndrome.xml"),
        ("Language Acquisition", "https://www.sciencedaily.com/rss/mind_brain/language_acquisition.xml"),
        ("Matter and Energy", "https://www.sciencedaily.com/rss/matter_energy.xml"),
        ("Mind and Brain", "https://www.sciencedaily.com/rss/mind_brain.xml"),
        ("Obstructive Sleep Apnea", "https://www.sciencedaily.com/rss/mind_brain/obstructive_sleep_apnea.xml"),
        ("Physics", "https://www.sciencedaily.com/rss/matter_energy/physics.xml"),
        ("Plants and Animals", "https://www.sciencedaily.com/rss/plants_animals.xml"),
        ("Psychiatry", "https://www.sciencedaily.com/rss/mind_brain/psychiatry.xml"),
        ("Psychology", "https://www.sciencedaily.com/rss/mind_brain/psychology.xml"),
        ("Racial Issues", "https://www.sciencedaily.com/rss/mind_brain/racial_issues.xml"),
        ("Schizophrenia", "https://www.sciencedaily.com/rss/mind_brain/schizophrenia.xml"),
        ("Severe Weather", "https://www.sciencedaily.com/rss/earth_climate/severe_weather.xml"),
        ("Sexual Health", "https://www.sciencedaily.com/rss/health_medicine/sexual_health.xml"),
        ("Sleep Disorders", "https://www.sciencedaily.com/rss/mind_brain/sleep_disorders.xml"),
        ("Society News", "https://www.sciencedaily.com/rss/science_society.xml"),
        ("Space and Time", "https://www.sciencedaily.com/rss/space_time.xml"),
        ("Sports Medicine", "https://www.sciencedaily.com/rss/health_medicine/sports_medicine.xml"),
        ("Technology News", "https://www.sciencedaily.com/rss/top/technology.xml"),
        ("Top Science News", "https://www.sciencedaily.com/rss/top/science.xml"),
        ("All News", "https://www.sciencedaily.com/rss/all.xml"),
    ]

    def parse_feeds(self):
        feeds = BasicNewsRecipe.parse_feeds(self)
        for feed in feeds:
            for article in feed.articles[:]:
                for word in self.filter_out:
                    if word.upper() in article.title.upper() or word.upper() in article.summary.upper():
                        self.log.warn(f"\t\tremoving \"{article.title}\" from _{feed.title}_ feed (keyword: {word})")
                        feed.articles.remove(article)
                        break
                    else:
                        continue
        # return feeds
        new_feeds = [f for f in feeds if len(f.articles[:]) > 0]
        return new_feeds

    def populate_article_metadata(self, article, soup, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)
            article.title = format_title(article.title, article.utctime)
        srclink = soup.find("a", attrs={"id": "meta_src"})
        if srclink:
            srclink["href"] = article.url

    def preprocess_html(self, soup):
        meta = soup.new_tag("div")
        meta["id"] = "metadata"
        date_posted = soup.find(attrs={"id": "date_posted"}).extract()
        dst = date_posted.string
        date_posted.string = "Date: {}".format(dst)
        art_source = soup.find(attrs={"id": "source"}).extract()
        art_source.string = "Source: {}".format(art_source.string)
        abstract = soup.find(attrs={"id": "abstract"}).extract()
        abstract.string = "Summary: {}".format(abstract.string)
        srclink = soup.new_tag("div")
        srclink["id"] = "headersrc"
        srclink.append("Article: ")
        srclink_a = soup.new_tag("a")
        srclink_a["id"] = "meta_src"
        srclink_a.append("View on ScienceDaily")
        srclink.append(srclink_a)
        for el in [date_posted, art_source, abstract]:
            el.name = "div"
        meta.append(date_posted)
        meta.append(art_source)
        meta.append(abstract)
        meta.append(srclink)
        hr = soup.new_tag("hr")
        subhead = soup.find(attrs={"id": "subtitle"})
        if subhead:
            subhead.insert_after(meta)
            subhead.insert_after(hr)
        else:
            soup.find("h1").insert_after(meta)
            soup.find("h1").insert_after(hr)
        soup.find("dl").extract()
        return soup

    def postprocess_html(self, soup, first_fetch):
        div = soup.find("div", attrs={"id": "citation_apa"})
        regex = re.compile("www.*?htm", re.DOTALL)
        if div:
            match = regex.search(self.tag_to_string(div))
            # pyright yells about the group method unless we ignore its type
            uri = match.group(0)  # type: ignore
            link = soup.new_tag("a")
            link["id"] = "article_url"
            link["href"] = 'https://{}'.format(uri)
            uri_sep = uri.split("/")
            link.append("https:/")
            for piece in uri_sep:
                wbr = soup.new_tag("wbr")
                link.append("/")
                link.append(wbr)
                link.append(piece)
            new_citation_content = div.contents[0:3]
            new_citation_content[-1] = new_citation_content[-1].split("www")[0]
            new_div = soup.new_tag("div")
            new_div["class"] = "tab_pane"
            div["id"] = "citation_apa_old"
            new_div["id"] = "citation_apa"
            new_div["role"] = "tabpanel"
            for thing in new_citation_content:
                new_div.append(thing)
            new_div.append(link)
            div.insert_after(new_div)
            div.extract()
        return soup

    def get_browser(self, *a, **kw):
        kw[
            "user_agent"
        ] = "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"
        br = BasicNewsRecipe.get_browser(self, *a, **kw)
        return br

    def clone_browser(self, *args, **kwargs):
        return self.get_browser()

    def open_novisit(self, *args, **kwargs):
        br = browser()
        return br.open_novisit(*args, **kwargs)

    open = open_novisit


calibre_most_common_ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36'
