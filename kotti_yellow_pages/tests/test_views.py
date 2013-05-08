from kotti.resources import get_root

from kotti_yellow_pages.resources import YellowPages
from kotti_yellow_pages.views.pages import YellowPagesView


def test_views(db_session, dummy_request):

    root = get_root()
    content = YellowPages()
    root['content'] = content

    view = YellowPagesView(root['content'], dummy_request)

    assert 'branches_json' in view.view()
    assert 'companies_json' in view.view()
