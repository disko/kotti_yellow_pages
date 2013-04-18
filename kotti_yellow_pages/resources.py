# -*- coding: utf-8 -*-

"""
Created on 2013-04-12
:author: Andreas Kaiser (disko)
"""

from kotti import Base
from kotti import DBSession
from kotti.resources import Content
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import backref
from sqlalchemy.orm import relationship
from zope.interface import implements

from kotti_yellow_pages import _
from kotti_yellow_pages.interfaces import IYPBranchWorkflow
from kotti_yellow_pages.interfaces import IYPCompanyWorkflow
from kotti_yellow_pages.interfaces import IYellowPagesWorkflow


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
        companies.sort(key=lambda c: c.title)
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
    street = Column(Unicode)
    zipcode = Column(Unicode)
    city = Column(Unicode)
    country = Column(Unicode)

    telephone = Column(Unicode)
    facsimile = Column(Unicode)
    url = Column(Unicode)
    email = Column(Unicode)

    latitude = Column(Float)
    longitude = Column(Float)

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
    )

    def __init__(self, street=None, zipcode=None, city=None, country=None,
                 telephone=None, facsimile=None, url=None, email=None,
                 latitude=None, longitude=None, branches=[], **kwargs):

        super(YPCompany, self).__init__(**kwargs)

        self.street = street
        self.zipcode = zipcode
        self.city = city
        self.country = country
        self.telephone = telephone
        self.facsimile = facsimile
        self.url = url
        self.email = email
        self.latitude = latitude
        self.longitude = longitude
        self.branches = branches

    def __json__(self, request):
        return {
            'title': self.title,
            'name': self.title,
            'street': self.street,
            'zipcode': self.zipcode,
            'city': self.city,
            'country': self.country,
            'telephone': self.telephone,
            'facsimile': self.facsimile,
            'url': self.url,
            'email': self.email,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'branches': [b for b in self.branches],
        }
