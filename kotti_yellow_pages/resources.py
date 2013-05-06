# -*- coding: utf-8 -*-

"""
Created on 2013-04-12
:author: Andreas Kaiser (disko)
"""

from kotti import Base
from kotti import DBSession
from kotti.resources import Content
from kotti.util import ViewLink
from phonenumbers import parse
from phonenumbers import format_number
from phonenumbers import PhoneNumberFormat
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from zope.interface import implements

from kotti_yellow_pages import _
from kotti_yellow_pages.interfaces import IYPBranchWorkflow
from kotti_yellow_pages.interfaces import IYPCompanyWorkflow
from kotti_yellow_pages.interfaces import IYellowPagesWorkflow


def format_phone(number, country, _format=PhoneNumberFormat.INTERNATIONAL):
    try:
        number = format_number(parse(number, country), _format)
    except:
        pass

    return number


class YellowPages(Content):
    """Yellow Pages content type"""

    __tablename__ = 'yp_pages'

    implements(IYellowPagesWorkflow)

    id = Column(
        Integer,
        ForeignKey('contents.id'),
        primary_key=True
    )

    type_info = Content.type_info.copy(
        name=u'YellowPages',
        title=_(u'Yellow Pages'),
        add_view=u'add_yellowpages',
        addable_to=['Document', ],
        edit_links=[
            # ViewLink('edit', title=_(u'Edit')),
            ViewLink('branches', title=_(u'Branches')),
            ViewLink('companies', title=_(u'Companies')),
            ViewLink('share', title=_(u'Share')),
        ],
    )

    def branches_with_permission(self, request, permission='view'):
        branches = [
            c for c in self.children_with_permission(request, permission)
            if isinstance(c, YPBranch)
        ]
        branches.sort(key=lambda c: c.title)
        return branches

    def companies_with_permission(self, request, permission='view'):
        companies = [
            c for c in self.children_with_permission(request, permission)
            if isinstance(c, YPCompany)
        ]
        companies.sort(key=lambda c: c.zipcode)
        return companies


class YPBranch(Content):
    """Yellow Pages Branch content type"""

    __tablename__ = 'yp_branches'

    implements(IYPBranchWorkflow)

    id = Column(
        Integer,
        ForeignKey('contents.id'),
        primary_key=True
    )

    @property
    def companies(self):
        """

        :result: List of companies
        :rtype: list of :class:`~kotti_yellow_pages.resources.YPCompany`
        """

        return [rel.company for rel in self.company_branches]

    type_info = Content.type_info.copy(
        name=u'YPBranch',
        title=_(u'Yellow Pages Branch'),
        add_view=u'add_yp_branch',
        addable_to=['YellowPages', ],
        edit_links=[
            ViewLink('edit', title=_(u'Edit')),
            ViewLink('share', title=_(u'Share')),
        ],
    )

    def __json__(self, request):
        return {
            'id': self.id,
            'title': self.title,
        }


class YPCompanyToBranch(Base):
    """ YPCompany to YPBranch mapping"""

    __tablename__ = 'yp_companies_to_branches'

    company_id = Column(Integer, ForeignKey("yp_companies.id"),
                        primary_key=True)
    branch_id = Column(Integer, ForeignKey("yp_branches.id"),
                       primary_key=True)

    branch = relationship('YPBranch', backref=backref('company_branches'))

    title = association_proxy('branch', 'title')

    @classmethod
    def _find_by_title(cls, title):
        """ Find a branch with the given title.

        :param title: Title of the branch to find.
        :type title: unicode

        :result:
        :rtype: :class:`~kotti_yellow_pages.resources.YPCompanyToBranch`
        """

        with DBSession.no_autoflush:
            branch = DBSession.query(YPBranch).filter_by(title=title).first()
        if branch is None:
            branch = YPBranch(title=title)

        return cls(branch=branch)


class YPCompany(Content):
    """Yellow Pages Company content type"""

    __tablename__ = 'yp_companies'

    implements(IYPCompanyWorkflow)

    id = Column(
        Integer,
        ForeignKey('contents.id'),
        primary_key=True
    )

    # Add additional columns here
    street = Column(Unicode, nullable=False)
    zipcode = Column(Unicode, nullable=False)
    city = Column(Unicode, nullable=False)
    country = Column(Unicode, nullable=False)

    _telephone = Column('telephone', Unicode, nullable=False)
    _facsimile = Column('facsimile', Unicode, nullable=True)
    _url = Column('url', Unicode, nullable=True)
    email = Column(Unicode, nullable=True)

    contact_person = Column(Unicode, nullable=True)

    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)

    @hybrid_property
    def telephone(self):
        return self._telephone

    @telephone.setter
    def telephone_setter(self, telephone):
        self._telephone = format_phone(telephone, self.country)

    @hybrid_property
    def facsimile(self):
        return self._facsimile

    @facsimile.setter
    def facsimile_setter(self, facsimile):
        self._facsimile = format_phone(facsimile, self.country)

    @hybrid_property
    def url(self):
        return self._url

    @url.setter
    def url_setter(self, url):
        if url:
            if not url.startswith(('http://', 'https://', )):
                url = 'http://' + url
            if not url.endswith('/'):
                url = url + '/'
        self._url = url

    _branches = relationship(
        YPCompanyToBranch,
        backref=backref('company'),
        cascade='all, delete-orphan',
    )

    branches = association_proxy(
        '_branches',
        'title',
        creator=YPCompanyToBranch._find_by_title)

    type_info = Content.type_info.copy(
        name=u'YPCompany',
        title=_(u'Yellow Pages Company'),
        add_view=u'add_yp_company',
        addable_to=['YellowPages', ],
        edit_links=[
            ViewLink('edit', title=_(u'Edit')),
            ViewLink('share', title=_(u'Share')),
        ],
    )

    def __init__(self, street=None, zipcode=None, city=None, country=None,
                 telephone=None, facsimile=None, contact_person=None, url=None,
                 email=None, lat=None, lng=None, branches=[],
                 **kwargs):

        super(YPCompany, self).__init__(**kwargs)

        self.street = street
        self.zipcode = zipcode
        self.city = city
        self.country = country
        self.telephone = telephone
        self.facsimile = facsimile
        self.contact_person = contact_person
        self.url = url
        self.email = email
        self.lat = lat
        self.lng = lng
        self.branches = branches

    def selectable_branches(self, request):

        if request.context == self:
            pages = self.parent
        elif isinstance(request.context, YellowPages):
            pages = request.context
        else:
            raise ValueError('Invalid context.  request.context must be an '
                             'instance of either YellowPages or YPCompany')
        branches = pages.branches_with_permission(request)

        return branches

    def __json__(self, request):

        post = request.POST

        if 'branches' in post:
            branches = [
                {
                    "title": b.title,
                    "selected": b.title in post.getall('branches')
                }
                for b in self.selectable_branches(request)]
        else:
            branches = [
                {"title": b.title, "selected": b.title in self.branches}
                for b in self.selectable_branches(request)]

        def get(key):
            if key in post:
                return post.get(key)
            else:
                return getattr(self, key)

        result = {
            'id': get('id'),
            'title': get('title'),
            'branches': branches,
            'contact_person': get('contact_person'),
            'telephone': get('telephone'),
            'tel_url': get('telephone'),
            'facsimile': get('facsimile'),
            'url': get('url'),
            'email': get('email'),
            'address': {
                'street': get('street'),
                'city': get('city'),
                'zipcode': get('zipcode'),
                'country': get('country'),
            },
            'location': {
                'lat': get('lat'),
                'lng': get('lng'),
            }
        }

        return result
