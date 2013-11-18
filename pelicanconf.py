#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Chris Greenwood'
SITENAME = u'Chris Greenwood'
SITEURL = ''
ABOUT = 'blah blah blah'

USER_IMAGE = '/images/me2.jpeg'

THEME = 'custom_theme'

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2})-(?P<slug>.*)'

# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('Python.org', 'http://python.org/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

GITHUB_INTEGRATION_ENABLED = True
GITHUB_USERNAME = 'greenwoodcm'
GITHUB_URL = 'https://github.com/greenwoodcm'

#TWITTER_INTEGRATION_ENABLED = True
#TWITTER_USERNAME = 'chrismgreenwood'

DEFAULT_PAGINATION = 10

STATIC_PATHS = [
	'extra/favicon.png',
	'images'
]
EXTRA_PATH_METADATA = {
	'extra/favicon.png': {'path': 'favicon.ico'}
}

PLUGIN_PATH = 'pelican-plugins'
PLUGINS = ['assets']

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
