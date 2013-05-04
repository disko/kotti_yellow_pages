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

        self.request.company_errors = json.dumps(company_errors)

        return result


@view_config(name=YPCompany.type_info.add_view,
             permission='add_company',
             renderer='kotti_yellow_pages:templates/company_edit.pt')
class Add(AddFormView, YPCompanyForm):

    schema_factory = Schema
    add = YPCompany
    item_type = _(u"Company")
    success_message = _(
        u"Your company has been submitted, but won't be visible until it has " +
        u"been approved by an editor. If you provided an email address, you " +
        u"will be notified upon publishing.")

    def __init__(self, context, request, **kwargs):

        super(Add, self).__init__(context, request, **kwargs)

        company_edit.need()

    @property
    def success_url(self):
        """
        Redirect to the current context on success (i.e. the YellowPages
        instance)

        :result: YellowPages' URL.
        :rtype: str
        """

        return self.request.resource_url(self.context)

    @property
    def _default_json(self):
        """ JSON
        :result: JSON with default values of
                 :class:`kotti_yellow_pages.resources.YPCompany`
        :rtype: dict
        """

        return YPCompany().__json__(self.request)

    def before(self, form):
        """
        Add the JSON representation for a new
        :class:`kotti_yellow_pages.resources.YPCompany` instance to the request
        to be able to render our custom (non deform) form.

        :param form: Form instance of the view
        :type form: :class:`deform.form.Form`
        """

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
        """ Constructor

        :param context: Context item that is edited
        :type context: :class:`kotti_yellow_pages.resources.YPCompany`

        :param request: Current request
        :type request: :class:`pyramid.request.Request`

        :param **kwargs: arbitrary keyword arguments that are passed to the
                         superclass constructor.
        :type **kwargs: dict
        """

        super(Edit, self).__init__(context, request, **kwargs)

        company_edit.need()

    @property
    def _default_json(self):
        """ JSON serializable dict for the view.

        :result: JSON serializable dict of the context instance.
        :rtype: dict
        """

        return self.context.__json__(self.request)

    def before(self, form):
        """
        Add the JSON representation for a new
        :class:`kotti_yellow_pages.resources.YPCompany` instance to the request
        to be able to render our custom (non deform) form.

        :param form: Form instance of the view
        :type form: :class:`deform.form.Form`
        """

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
        """ Default view for companies.

        :result: Dict needed to render the view.
        :rtype: dict
        """

        company.need()

        return {}
