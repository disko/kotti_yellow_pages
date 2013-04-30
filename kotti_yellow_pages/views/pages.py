# -*- coding: utf-8 -*-

"""
Created on 2013-04-13
:author: Andreas Kaiser (disko)
"""

import json

from kotti.views.edit.content import ContentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from pyramid.view import view_config
from pyramid.view import view_defaults

from kotti_yellow_pages import _
from kotti_yellow_pages.fanstatic import pages
from kotti_yellow_pages.resources import YellowPages
from kotti_yellow_pages.views import BaseView


class YellowPagesSchema(ContentSchema):
    """Schema for add / edit forms of YellowPages"""


@view_config(name=YellowPages.type_info.add_view,
             permission='add',
             renderer='kotti:templates/edit/node.pt')
class YellowPagesAddForm(AddFormView):

    schema_factory = YellowPagesSchema
    add = YellowPages
    item_type = _(u"Yellow Pages")


@view_config(name='edit',
             context=YellowPages,
             permission='edit',
             renderer='kotti:templates/edit/node.pt')
class YellowPagesEditForm(EditFormView):

    schema_factory = YellowPagesSchema


@view_defaults(context=YellowPages, permission='view')
class YellowPagesView(BaseView):
    """View(s) for YellowPages"""

    @view_config(name='view',
                 renderer='kotti_yellow_pages:templates/pages.pt')
    def view(self):

        pages.need()

        branches = [
            {
                "title": b.title,
                "visible": True,
                "companies": [
                    c.__json__(self.request) for c in
                    self.context.companies_with_permission(self.request)
                    if b.title in c.branches
                ]
            }
            for b in self.context.branches_with_permission(self.request)
        ]

        return {
            'branches_json': json.dumps(branches)
        }
