# -*- coding: utf-8 -*-

"""
Created on 2013-04-13
:author: Andreas Kaiser (disko)
"""

from logging import getLogger

from kotti.events import ObjectInsert
from kotti.events import subscribe
from kotti.security import has_permission
from kotti.workflow import WorkflowTransition
from kotti.workflow import get_workflow
from pyramid.httpexceptions import HTTPTemporaryRedirect

from kotti_yellow_pages import _
from kotti_yellow_pages.resources import YPCompany


log = getLogger(__name__)


@subscribe(ObjectInsert, YPCompany)
def on_company_insert(event):

    log.info("YPCompany insert")

    context = event.object
    request = event.request

    wf = get_workflow(context)
    transitions = wf.get_transitions(context, request)
    to_states = [t['to_state'] for t in transitions]

    if 'private' in to_states:
        wf.transition_to_state(context, request, 'private')
    elif 'pending' in to_states:
        wf.transition_to_state(context, request, 'pending')

    #import pdb; pdb.set_trace()
    if not has_permission('view', context, request):
        request.session.flash(
            _(u'You will be notified on approval or rejection of your entry.'),
            'info')
        raise HTTPTemporaryRedirect(request.resource_url(context.parent))
    #import pdb; pdb.set_trace()


@subscribe(WorkflowTransition, YPCompany)
def on_company_transition(event):
    log.info("YPCompany transition")
    print event.object
    print event.request

    wf = event.info.workflow
    _from = event.info.transition['from_state']
    _to = event.info.transition['to_state']

    log.info('Transition of %s from %s to %s' % (event.object, _from, _to))
    #import pdb; pdb.set_trace()
