# -*- coding: utf-8 -*-

"""
Created on 2013-04-13
:author: Andreas Kaiser (disko)
"""

from kotti.interfaces import IDefaultWorkflow


class IYellowPagesWorkflow(IDefaultWorkflow):
    """
    Marker interface for objects that implement the YellowPagesWorkflow. """


class IYPBranchWorkflow(IDefaultWorkflow):
    """
    Marker interface for objects that implement the YPBranchWorkflow. """


class IYPCompanyWorkflow(IDefaultWorkflow):
    """
    Marker interface for objects that implement the YPCompanyWorkflow. """
