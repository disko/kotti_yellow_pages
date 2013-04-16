# -*- coding: utf-8 -*-

"""
Created on 2013-04-13
:author: Andreas Kaiser (disko)
"""


class BaseView(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request
