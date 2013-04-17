# -*- coding: utf-8 -*-

"""
Created on 2013-04-13
:author: Andreas Kaiser (disko)
"""

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

        return {
            'companies': self.context.companies_with_permission(self.request),
        }

    @view_config(name='json', renderer='json')
    def json(self):

        companies = self.context.companies_with_permission(self.request)

        return {
            'companies': companies,
            'branches': self.context.branches_with_permission(self.request),
            'min_lat': min([c.latitude for c in companies]),
            'max_lat': max([c.latitude for c in companies]),
            'min_lng': min([c.longitude for c in companies]),
            'max_lng': max([c.longitude for c in companies]),
        }
