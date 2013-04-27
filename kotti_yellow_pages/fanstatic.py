# -*- coding: utf-8 -*-

"""
Created on 2013-04-13
:author: Andreas Kaiser (disko)
"""

from __future__ import absolute_import

from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource
from js.angular import angular
from js.jquery import jquery

library = Library('kotti_yellow_pages', 'static')

leaflet = Resource(
    library,
    'js/leaflet.css.bundle.js',
    minified='js/leaflet.css.bundle.min.js'
)

kotti_yellow_pages = Resource(
    library,
    'js/kotti_yellow_pages.js',
    minified='js/kotti_yellow_pages.min.js',
    depends=[angular, leaflet, jquery, ]
)

pages_js = Resource(
    library,
    'js/pages.js',
    minified='js/pages.min.js',
    depends=[kotti_yellow_pages, ]
)
company_js = Resource(
    library,
    'js/company.js',
    minified='js/company.min.js',
    depends=[kotti_yellow_pages, ]
)
company_edit_js = Resource(
    library,
    'js/company_edit.js',
    minified='js/company_edit.min.js',
    depends=[kotti_yellow_pages, ]
)

css = Resource(
    library,
    'css/style.css',
    minified='css/style.min.css'
)


pages = Group([pages_js, css, ])
company = Group([company_js, css, ])
company_edit = Group([company_edit_js, css, ])
