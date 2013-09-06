# -*- coding: utf-8 -*-

"""
Created on 2013-04-13
:author: Andreas Kaiser (disko)
"""

from logging import getLogger

from kotti.events import ObjectInsert
from kotti.events import subscribe
from kotti.security import get_principals
from kotti.security import has_permission
from kotti.security import map_principals_with_local_roles
from kotti.workflow import WorkflowTransition
from kotti.workflow import get_workflow
from pyramid.security import principals_allowed_by_permission
from pyramid.threadlocal import get_current_request

from kotti_yellow_pages import _
from kotti_yellow_pages.resources import YPCompany


log = getLogger(__name__)


@subscribe(ObjectInsert, YPCompany)
def on_company_insert(event):

    log.info("YPCompany insert")

    wf = get_workflow(event.object)

    if has_permission('state_change', event.object, event.request):
        wf.transition(event.object, event.request, 'created_to_public')
    elif has_permission('submit', event.object, event.request):
        wf.transition(event.object, event.request, 'created_to_pending')
    else:
        log.warn("Company created, but no transition allowed for current user.")


def get_recepients(context, permission="state_change"):
    """
    Get a list of principals that have the permission in context and a email.

    :param context: Object for that the permission is needed.
    :type context: :class:`kotti.resources.Node`

    :param permission:
    :type permission: str

    :result: List of principals.
    :rtype: set
    """

    principal_db = get_principals()

    recepients = []
    for p in principals_allowed_by_permission(context, permission):
        # set(['role:owner', 'role:editor'])
        for principal in principal_db.search(groups=u'*%s*' % p).all():
            recepients.append(principal)
        for principal in map_principals_with_local_roles(context):
            # [
            #   (
            #       <Principal u'disko'>,
            #       (
            #           [u'role:owner', u'group:admins', u'role:admin'],
            #           [u'role:owner', u'group:admins', u'role:admin']))]
            if p in principal[1][0] or p in principal[1][1]:
                recepients.append(principal[0])

    return set([r for r in recepients if r.email])


@subscribe(WorkflowTransition, YPCompany)
def on_company_transition(event):

    # wf = event.info.workflow
    context = event.object
    request = get_current_request()

    _from = event.info.transition['from_state']
    _to = event.info.transition['to_state']

    log.info("YPCompany transition (%s -> %s)" % (_from, _to))

    if _to == 'pending':
        # send email

        recepients = get_recepients(context)
        mailer = request.mailer
        message = mailer.new()
        message.to = ['%s <%s>' % (r.title, r.email) for r in recepients]
        message.subject = _(u'New company submitted and waiting for approval')
        message.plain = request.resource_url(context)
        message.send()

    elif (_from == 'pending') and (_to == 'public'):
        if context.email:
            mailer = request.mailer
            message = mailer.new()
            message.to = '%s <%s>' % (context.title, context.email)
            message.subject = _(u'Your company is now listed')
            message.plain = request.resource_url(context.parent)
            message.send()
