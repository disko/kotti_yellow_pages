from kotti.resources import get_root
from kotti.testing import DummyRequest

from kotti_yellow_pages.resources import YellowPages


def test_yellowpages(db_session, config):
    config.include('kotti_yellow_pages')

    root = get_root()
    content = YellowPages()
    assert content.type_info.addable(root, DummyRequest()) is True
    root['content'] = content
