# -*- coding: utf-8 -*-

"""
Created on 2013-04-13
:author: Andreas Kaiser (disko)
"""

import json

import colander
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from kotti.views.form import ObjectType
from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid_deform import FormView

from kotti_yellow_pages import _
from kotti_yellow_pages.fanstatic import company
from kotti_yellow_pages.fanstatic import company_edit
from kotti_yellow_pages.resources import YPCompany
from kotti_yellow_pages.views import BaseView
from kotti_yellow_pages.views.branch import deferred_branches_widget


class Schema(colander.MappingSchema):
    """Schema for add / edit forms of Companies"""

    title = colander.SchemaNode(
        colander.String(),
        title=_("Company name"),)
    street = colander.SchemaNode(
        colander.String(),
        title=_("Street"),)
    zipcode = colander.SchemaNode(
        colander.String(),
        title=_("Zipcode"),)
    city = colander.SchemaNode(
        colander.String(),
        title=_("City"),)
    country = colander.SchemaNode(
        colander.String(),
        title=_("Country"),
        default=None,
        missing=None)
    telephone = colander.SchemaNode(
        colander.String(),
        title=_("Telephone"))
    facsimile = colander.SchemaNode(
        colander.String(),
        title=_("Facsimile"),
        default=None,
        missing=None)

    url = colander.SchemaNode(
        colander.String(),
        title=_("Website URL"),
        default=None,
        missing=None,
        validator=colander.url)
    email = colander.SchemaNode(
        colander.String(),
        title=_("Email address"),
        default=None,
        missing=None,
        validator=colander.Email())

    contact_person = colander.SchemaNode(
        colander.String(),
        title=_("Contact person"),
        default=None,
        missing=None)

    lat = colander.SchemaNode(
        colander.Float(),
        title=_(u"Latitude"),)
        #widget=deform.widget.HiddenWidget())
    lng = colander.SchemaNode(
        colander.Float(),
        title=_(u"Longitude"),)
        #widget=deform.widget.HiddenWidget())
    branches = colander.SchemaNode(
        ObjectType(),
        title=_('Branches'),
        widget=deferred_branches_widget,
        missing=[])


class YPCompanyForm(FormView):

    @property
    def _default_json(self):
        raise NotImplementedError(
            'Classes that inherit from YPCompanyForm must provide their own '
            'implementation of the _default_json property')

    def add_json(self, form):
        self.request.company_json = json.dumps(self._default_json)

    def failure(self, e):
        result = super(YPCompanyForm, self).failure(e)

        # put all validation failure error messages in a JSON serializable dict
        company_errors = {}
        for err in e.error.children:
            k = err.node.name
            company_errors[k] = err.msg

        # update the default company JSOn with the values submitted by the user
        # company_json = self._default_json
        # for k in company_json.keys():
        #     if k == 'branches':
        #         for b in company_json[k]:
        #             b['selected'] = b['title'] in e.cstruct[k]
        #     elif k in ('address', 'location'):
        #         for k2 in company_json[k]:
        #             company_json[k][k2] = e.cstruct[k2] or ''
        #     else:
        #         company_json[k] = e.cstruct[k] or ''

        # self.request.company_json = json.dumps(company_json)
        self.request.company_errors = json.dumps(company_errors)

        return result


@view_config(name=YPCompany.type_info.add_view,
             permission='add_company',
             renderer='kotti_yellow_pages:templates/company_edit.pt')
class Add(AddFormView, YPCompanyForm):

    schema_factory = Schema
    add = YPCompany
    item_type = _(u"Company")

    def __init__(self, context, request, **kwargs):

        super(Add, self).__init__(context, request, **kwargs)

        company_edit.need()

    @property
    def _default_json(self):
        return YPCompany().__json__(self.request)

    def before(self, form):
        super(Add, self).before(form)
        self.add_json(form)


@view_config(name='edit',
             context=YPCompany,
             permission='edit',
             renderer='kotti_yellow_pages:templates/company_edit.pt')
class Edit(EditFormView, YPCompanyForm):
    """
    Edit form view for :class:`kotti_yellow_pages.resources.YPCompany`.

    """

    schema_factory = Schema

    def __init__(self, context, request, **kwargs):

        super(Edit, self).__init__(context, request, **kwargs)

        company_edit.need()

    @property
    def _default_json(self):
        return self.context.__json__(self.request)

    def before(self, form):
        super(Edit, self).before(form)
        self.add_json(form)

    @property
    def success_url(self):
        """ Redirect to the parent on success (i.e. the YellowPages instance)

        :result: parent's URL.
        :rtype: str
        """

        return self.request.resource_url(self.context.parent)


@view_defaults(context=YPCompany, permission='view')
class View(BaseView):
    """View(s) for YPCompany"""

    @view_config(name='view',
                 renderer='kotti_yellow_pages:templates/company.pt')
    def view(self):

        company.need()

        return {}
