# -*- coding: utf-8 -*-

"""
Created on 2013-04-13
:author: Andreas Kaiser (disko)
"""

from colander import deferred
from deform.widget import CheckboxChoiceWidget
from kotti.views.edit.content import ContentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from pyramid.view import view_config

from kotti_yellow_pages import _
from kotti_yellow_pages.resources import YPBranch
from kotti_yellow_pages.resources import YPCompany


@deferred
def deferred_branches_widget(node, kw):
    yp = kw['request'].context
    if isinstance(yp, YPCompany):
        yp = yp.parent
    all_branches = YPBranch.query.filter(YPBranch.parent == yp).all()
    available_branches = [
        (topic.title.encode('utf-8'), topic.title.encode('utf-8'))
        for topic in all_branches]
    return CheckboxChoiceWidget(
        values=available_branches,
        template="kotti_yellow_pages:templates/checkbox_choice"
    )


class YPBranchSchema(ContentSchema):
    """Schema for add / edit forms of Branches"""


@view_config(name=YPBranch.type_info.add_view,
             permission='add_branch',
             renderer='kotti:templates/edit/node.pt')
class YPBranchAddForm(AddFormView):

    schema_factory = YPBranchSchema
    add = YPBranch
    item_type = _(u"Branch")


@view_config(name='edit',
             context=YPBranch,
             permission='edit',
             renderer='kotti:templates/edit/node.pt')
class YPBranchEditForm(EditFormView):

    schema_factory = YPBranchSchema
