#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Utilities for weak references to persistent objects.

"""

__docformat__ = "restructuredtext en"

from zope import interface
from nti.wref.interfaces import ICachingWeakRef

from zope import copy

from persistent.wref import WeakRef

@interface.implementer(ICachingWeakRef)
class CopyingWeakRef(WeakRef):
    """
    A weak ref that also stores a one-shot copy (using
    :func:`zope.copy.copy`) of its reference, as a fallback to return
    from :meth:`__call__` if the weak reference cannot be resolved.

    Use this if the object is expected to mutate after this reference
    is established and you normally want to have access to those
    changes, and you cannot tolerate the object going missing, but you
    also cannot keep a strong reference to the object. This may be
    particularly the case in cross-database refs.

    Implements :class:`nti.wref.interfaces.ICachingWeakRef`.
    """

    def __init__(self, ob):
        super().__init__(ob)
        self._copy = copy.copy(ob)

    def __call__(self, allow_cached=True):
        result = super().__call__()
        if result is None and allow_cached:
            result = self._copy
        return result
