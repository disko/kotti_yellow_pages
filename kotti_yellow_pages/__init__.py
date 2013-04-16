# -*- coding: utf-8 -*-

"""
Created on 2013-04-12
:author: Andreas Kaiser (disko)
"""

from pyramid.i18n import TranslationStringFactory

_ = TranslationStringFactory('kotti_yellow_pages')


def kotti_configure(settings):

    settings['pyramid.includes'] += ' kotti_yellow_pages'
    settings['kotti.available_types'] += \
        ' kotti_yellow_pages.resources.YellowPages'
    settings['kotti.available_types'] += \
        ' kotti_yellow_pages.resources.YPBranch'
    settings['kotti.available_types'] += \
        ' kotti_yellow_pages.resources.YPCompany'


def includeme(config):

    config.add_translation_dirs('kotti_yellow_pages:locale')
    config.scan()
