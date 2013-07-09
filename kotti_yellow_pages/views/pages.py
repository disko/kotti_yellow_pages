# -*- coding: utf-8 -*-

"""
Created on 2013-04-13
:author: Andreas Kaiser (disko)
"""

import json

from kotti.views.edit.actions import contents
from kotti.views.edit.content import ContentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from pyramid.view import view_config
from pyramid.view import view_defaults

from kotti_yellow_pages import _
from kotti_yellow_pages.fanstatic import pages_complex
from kotti_yellow_pages.fanstatic import pages_simple
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

    @property
    def _branches(self):
        """ Branches as needed by views.

        :result: visible branches
        :rtype: list of dict
        """

        return [
            {
                "title": b.title,
                "visible": True,
                "companies": [],
            }
            for b in self.context.branches_with_permission(self.request)
        ]

    @property
    def _companies(self):
        """ Companies as needed by views.

        :result: visible companies
        :rtype: list of dict
        """

        return [
            c.__json__(self.request) for c in
            self.context.companies_with_permission(self.request)
        ]

    @view_config(name='advanced',
                 renderer='kotti_yellow_pages:templates/pages-complex.pt')
    def complex(self):
        """
        'Complex' view, showing everything with multiple filter / order options
        """

        pages_complex.need()

        return {
            'branches_json': json.dumps(self._branches),
            'companies_json': json.dumps(self._companies),
        }

    @view_config(name='view',
                 renderer='kotti_yellow_pages:templates/pages-simple.pt')
    def view(self):
        """
        'Simple' wizard style view, showing max 5 companies, always next to
        zipcode entered by the user.
        """

        pages_simple.need()

        return {
            'branches_json': json.dumps(self._branches),
            'companies_json': json.dumps(self._companies),
        }

    @view_config(name='branches', permission='edit',
                 renderer='kotti:templates/edit/contents.pt')
    def branches(self):
        """ Filtered contents view for editing """

        result = contents(self.context, self.request)
        result['children'] = [c for c in result['children']
                              if c.type == 'yp_branch']

        return result

    @view_config(name='companies', permission='edit',
                 renderer='kotti:templates/edit/contents.pt')
    def companies(self):
        """ Filtered contents view for editing """

        result = contents(self.context, self.request)
        result['children'] = [c for c in result['children']
                              if c.type == 'yp_company']

        return result
