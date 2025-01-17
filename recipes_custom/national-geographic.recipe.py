#!/usr/bin/env python
# vim:fileencoding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import json
from pprint import pformat
import os
import sys
from datetime import datetime, timezone

# custom include to share code between recipes
sys.path.append(os.environ["recipes_includes"])
from recipes_shared import BasicNewsrackRecipe, format_title
from calibre.web.feeds.news import BasicNewsRecipe
from calibre import prepare_string_for_xml as escape
from calibre.utils.iso8601 import parse_iso8601


def classes(classes):
    q = frozenset(classes.split(' '))
    return dict(attrs={
        'class': lambda x: x and frozenset(x.split()).intersection(q)})


def extract_json(raw):
    s = raw.find("window['__natgeo__']")
    script = raw[s:raw.find('</script>', s)]
    return json.loads(
        script[script.find('{'):].rstrip(';'))['page']['content']['article']


def parse_contributors(grp):
    for item in grp:
        line = '<p>' + escape(item['title']) + ' '
        for c in item['contributors']:
            line += escape(c['displayName'])
        yield line + '</p>'


def parse_lead_image(media):
    yield '<div><img src="{}" alt="{}"></div>'.format(
        escape(media['image']['src'], True), escape(media['image']['dsc'], True))
    yield '<p>' + escape(media['caption']) + '</p>'
    if 'credit' in media:
        yield '<p>' + escape(media['credit']) + '</p>'


def parse_body(item):
    c = item['cntnt']
    if item.get('type') == 'inline':
        if c.get('cmsType') == 'listicle':
            yield '<h3>' + escape(c['title']) + "</h3>"
            yield c['text']
        elif c.get('cmsType') == 'image':
            for line in parse_lead_image(c):
                yield line
    else:
        yield '<{tag}>{markup}</{tag}>'.format(
            tag=item['type'], markup=c['mrkup'])


def parse_article(edg):
    sc = edg['schma']
    yield '<h3>' + escape(edg['sctn']) + '</h3>'
    yield '<h1>' + escape(sc['sclTtl']) + '</h1>'
    yield '<div>' + escape(sc['sclDsc']) + '</div>'
    for line in parse_contributors(edg['cntrbGrp']):
        yield line
    ts = parse_iso8601(edg['mdDt'], as_utc=False).strftime('%B %d, %Y')
    yield '<p>Published: ' + escape(ts) + '</p>'
    if 'readTime' in edg:
        yield '<p>' + escape(edg['readTime']) + '</p>'
    if edg.get('ldMda', {}).get('cmsType') == 'image':
        for line in parse_lead_image(edg['ldMda']):
            yield line
    for item in edg['bdy']:
        for line in parse_body(item):
            yield line


def article_parse(data):
    yield "<html><body>"
    for frm in data['frms']:
        if not frm:
            continue
        for mod in frm.get('mods', ()):
            for edg in mod.get('edgs', ()):
                if edg.get('cmsType') == 'ArticleBodyTile':
                    for line in parse_article(edg):
                        yield line
    yield "</body></html>"


_name = "National Geographic Daily"


class NatGeo(BasicNewsRecipe, BasicNewsrackRecipe):
    title = _name
    description = 'Daily news articles from The National Geographic'
    language = 'en'
    encoding = 'utf8'
    publisher = 'nationalgeographic.com'
    publication_type = 'magazine'
    category = 'science, nat geo'
    __author__ = 'Kovid Goyal, holyspiritomb (adapted for newsrack)'
    description = 'Inspiring people to care about the planet since 1888'
    timefmt = ' [%a, %d %b, %Y]'
    no_stylesheets = True
    use_embedded_content = False
    remove_attributes = ['style']
    remove_javascript = False
    oldest_article = 2
    conversion_options = {
        'tags' : 'Science, History, Geography, Periodical, National Geographic',
    }

    def parse_index(self):
        soup = self.index_to_soup('https://www.nationalgeographic.com/latest-stories/')
        ans = {}
        for article in soup.findAll('article'):
            a = article.find('a')
            url = a['href']
            section = self.tag_to_string(article.find(**classes('SectionLabel')))
            title = self.tag_to_string(article.find(**classes('PromoTile__Title--truncated')))
            articles = ans.setdefault(section, [])
            articles.append({'title': title, 'url': url})
        self.log(pformat(ans))
        return list(ans.items())

    def populate_article_metadata(self, article, __, _):
        if (not self.pub_date) or article.utctime > self.pub_date:
            self.pub_date = article.utctime
            self.title = format_title(_name, article.utctime)

    def preprocess_raw_html(self, raw_html, url):
        data = extract_json(raw_html)
        return '\n'.join(article_parse(data))
