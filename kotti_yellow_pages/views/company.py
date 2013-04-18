# -*- coding: utf-8 -*-

"""
Created on 2013-04-13
:author: Andreas Kaiser (disko)
"""

import colander
import deform
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from kotti.views.form import ObjectType
from pyramid.view import view_config
from pyramid.view import view_defaults

from kotti_yellow_pages import _
from kotti_yellow_pages.fanstatic import company
from kotti_yellow_pages.fanstatic import company_edit
from kotti_yellow_pages.resources import YPCompany
from kotti_yellow_pages.views import BaseView
from kotti_yellow_pages.views.branch import deferred_branches_widget


class Schema(colander.MappingSchema):
    """Schema for add / edit forms of Companies"""

    title = colander.SchemaNode(colander.String(), title=_("Company name"))
    street = colander.SchemaNode(colander.String(), title=_("Street"))
    zipcode = colander.SchemaNode(colander.String(), title=_("Zipcode"))
    city = colander.SchemaNode(colander.String(), title=_("City"))
    country = colander.SchemaNode(colander.String(), title=_("Country"))
    telephone = colander.SchemaNode(colander.String(), title=_("Telephone"))
    facsimile = colander.SchemaNode(colander.String(), title=_("Facsimile"))

    url = colander.SchemaNode(colander.String(),
                              title=_("Website URL"),
                              default=None,
                              missing=None,
                              validator=colander.url)
    email = colander.SchemaNode(colander.String(),
                                title=_("Email address"),
                                default=None,
                                missing=None,
                                validator=colander.Email())

    latitude = colander.SchemaNode(colander.Float(),
                                   title=_(u"Latitude"),
                                   widget=deform.widget.HiddenWidget())
    longitude = colander.SchemaNode(colander.Float(),
                                    title=_(u"Longitude"),
                                    widget=deform.widget.HiddenWidget())
    branches = colander.SchemaNode(ObjectType(),
                                   title=_('Branches'),
                                   widget=deferred_branches_widget,
                                   missing=[])


@view_config(name=YPCompany.type_info.add_view,
             permission='add_company',
             renderer='kotti_yellow_pages:templates/company_edit.pt')
class Add(AddFormView):

    schema_factory = Schema
    add = YPCompany
    item_type = _(u"Company")

    def __init__(self, context, request, **kwargs):

        super(Add, self).__init__(context, request, **kwargs)

        company_edit.need()


@view_config(name='edit',
             context=YPCompany,
             permission='edit',
             renderer='kotti_yellow_pages:templates/company_edit.pt')
class Edit(EditFormView):

    schema_factory = Schema

    def __init__(self, context, request, **kwargs):

        super(Edit, self).__init__(context, request, **kwargs)

        company_edit.need()


@view_defaults(context=YPCompany, permission='view')
class View(BaseView):
    """View(s) for YPCompany"""

    @view_config(name='view',
                 renderer='kotti_yellow_pages:templates/company.pt')
    def view(self):

        company.need()

        return {}
