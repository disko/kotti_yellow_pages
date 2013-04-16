# -*- coding: utf-8 -*-

"""
Created on 2013-04-12
:author: Andreas Kaiser (disko)
"""

from kotti import Base
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


class YPBranch(Content):
    """Yellow Pages Branch content type"""

    __tablename__ = 'yp_branches'

    implements(IYPBranchWorkflow)

    id = Column(
        Integer,
        ForeignKey('contents.id'),
        primary_key=True
    )

    companies = association_proxy('branch_companies', 'company')

    type_info = Content.type_info.copy(
        name=u'YPBranch',
        title=_(u'Yellow Pages Branch'),
        add_view=u'add_yp_branch',
        addable_to=['YellowPages', ],
    )


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

    branches = association_proxy('company_branches', 'branch')

    type_info = Content.type_info.copy(
        name=u'YPCompany',
        title=_(u'Yellow Pages Company'),
        add_view=u'add_yp_company',
        addable_to=['YellowPages', ],
    )

    def __init__(self, street=None, zipcode=None, country=None, state=None,
                 telephone=None, facsimile=None, url=None, email=None,
                 latitude=None, longitude=None, **kwargs):

        super(YPCompany, self).__init__(**kwargs)

        self.street = street
        self.zipcode = zipcode
        self.country = country
        self.state = state
        self.telephone = telephone
        self.facsimile = facsimile
        self.url = url
        self.email = email
        self.latitude = latitude
        self.longitude = longitude


class YPCompanyToBranch(Base):
    """ YPCompany to YPBranch mapping"""

    __tablename__ = 'yp_companies_to_branches'

    company_id = Column(Integer, ForeignKey("yp_companies.id"),
                        primary_key=True)
    branch_id = Column(Integer, ForeignKey("yp_branches.id"),
                       primary_key=True)

    company = relationship(YPCompany, backref=backref('company_branches'))
    branch = relationship(YPBranch, backref=backref('branch_companies'))
