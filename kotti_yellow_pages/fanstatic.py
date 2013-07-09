# -*- coding: utf-8 -*-

"""
Created on 2013-04-13
:author: Andreas Kaiser (disko)
"""

from __future__ import absolute_import

from fanstatic import Group
from fanstatic import Library
from fanstatic import Resource
from js.jquery import jquery
from js.leaflet import leaflet
from js.spin import jquery_spin

library = Library('kotti_yellow_pages', 'static')

# For now we have to bundle our own angular.js because the version provided by
# js.angular does not depend on jquery.  This is correct but shows up a current
# limitation of fanstatic, which cannot declare "optional dependencies".
# See: https://groups.google.com/forum/#!msg/fanstatic/CGAtvaLBu7g/elwINFULqEUJ

angular = Resource(
    library,
    'vendor/js/angular.js',
    minified='vendor/js/angular.min.js',
    depends=[jquery, ])

angular_ui_css = Resource(
    library,
    'vendor/css/angular-ui.css',
    minified='vendor/css/angular-ui.min.css',
    depends=[angular, ])
angular_ui_js = Resource(
    library,
    'vendor/js/angular-ui.js',
    minified='vendor/js/angular-ui.min.js',
    depends=[angular, ])
angular_ui = Group([angular_ui_js, angular_ui_css])

angular_bootstrap = Resource(
    library,
    'vendor/js/angular-bootstrap.js',
    minified='vendor/js/angular-bootstrap.min.js',
    depends=[angular, ])

leaflet_awesome_markers_js = Resource(
    library,
    'vendor/js/leaflet.awesome-markers.js',
    minified='vendor/js/leaflet.awesome-markers.min.js',
    depends=[leaflet, ]
)
leaflet_awesome_markers_css = Resource(
    library,
    'vendor/css/leaflet.awesome-markers.css',
    minified='vendor/css/leaflet.awesome-markers.min.css',
    depends=[leaflet, ]
)
leaflet_awesome_markers = Group(
    [leaflet_awesome_markers_js, leaflet_awesome_markers_css])

kotti_yellow_pages = Resource(
    library,
    'js/kotti_yellow_pages.js',
    minified='js/kotti_yellow_pages.min.js',
    depends=[
        jquery,
        angular,
        angular_ui,
        leaflet,
        leaflet_awesome_markers,
    ]
)

pages_complex_js = Resource(
    library,
    'js/pages-complex.js',
    minified='js/pages-complex.min.js',
    depends=[kotti_yellow_pages, ]
)
pages_simple_js = Resource(
    library,
    'js/pages-simple.js',
    minified='js/pages-simple.min.js',
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
    depends=[kotti_yellow_pages, angular_bootstrap, jquery_spin, ]
)

css = Resource(
    library,
    'css/style.css',
    minified='css/style.min.css'
)


pages_complex = Group([pages_complex_js, css, ])
pages_simple = Group([pages_simple_js, css, ])
company = Group([company_js, css, ])
company_edit = Group([company_edit_js, css, ])
