from pyramid.interfaces import ITranslationDirectories

from kotti_yellow_pages import includeme
from kotti_yellow_pages import kotti_configure


def test_kotti_configure():

    settings = {
        'kotti.available_types': '',
        'pyramid.includes': '',
    }

    kotti_configure(settings)

    assert settings['pyramid.includes'] == ' kotti_yellow_pages'

    assert 'kotti_yellow_pages.resources.YellowPages' in \
        settings['kotti.available_types']
    assert 'kotti_yellow_pages.resources.YPBranch' in \
        settings['kotti.available_types']
    assert 'kotti_yellow_pages.resources.YPCompany' in \
        settings['kotti.available_types']


def test_includeme(config):

    includeme(config)

    utils = config.registry.__dict__['_utility_registrations']
    k = (ITranslationDirectories, u'')

    # test if the translation dir is registered
    assert k in utils
    assert utils[k][0][0].find('kotti_yellow_pages/locale') > 0
