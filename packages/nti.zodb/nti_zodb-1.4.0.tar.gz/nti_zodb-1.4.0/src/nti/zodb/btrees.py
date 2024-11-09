# -*- coding: utf-8 -*-
"""
Support for using :mod:`BTrees` with ZODB.

This module is primarily concerned with making BTrees even more
efficient, especially at large scale and high concurrency.

.. rubric:: family64LargeBuckets

This is a BTree family that's useful for high-concurrency or large
applications by increasing the size of individual buckets. This
reduces the number of ZODB fetches required, and also reduces the
amount of bucket splitting required on write-heavy workloads, thus
reducing unresolvable conflicts. For example, an ``OOBTree`` defaults
to a bucket size of 60, while this family uses 500. This can be used
anywhere BTrees are used, for example in containers.

:mod:`zope.index` provides a particularly motivating example.

Underlying the indices are the same BTree data structures as under any
:class:`zope.container.btree.BTreeContainer`. They're typically intid,
based, though, so instead of the default limit of 60 items in a bucket
that applies for an OO tree, they would have different limits. For the
64-bit IO tree, that limit is...also 60. (Any BTree with a n 'O' in
its name defaults to 60.)

Most indices maintain two BTrees::

    forward: OO = indexed value to sequence of intids
    backward: IO = intid to indexed value

The forward index values are usually either a ISet or ITreeSet;
attribute indices always use TreeSet, but keyword indices transition
between Set and TreeSet at a fixed threshold. Sets should basically
always be able to resolve conflicts (no splits to deal with) but will
conflict on every addition (and of course have unbounded growth in
pickle size). TreeSets may occasionally have un-resolvable conflicts,
but any given insert is less likely to conflict because they're spread
across buckets.

Just as for ``BTreeContainers``, using a BTree with increased bucket
size, applied to the forward, backward, and sequence values, can serve
to reduce conflicts. Since all the index constructors take a 'family'
argument that's used to determine the type of their forward, backward
and sequence attributes, supplying the ``family64LargeBuckets`` will
accomplish this.

Why wasn't this done by default? Most importantly, the ability to
customize those aspects of BTree sizes is a relatively recent addition
(within the last few years), well after zope.index and zope.catalog
were written.

Why use such small sizes for the defaults? My guess is that it's a
product of the time BTrees were designed: smaller disks, smaller
memories, slower networks -> optimize for space and transfer time with
smaller pickles.

However, there are some caveats.

First, the pickles for individual buckets will be larger by a factor
of 8 (for an OO object). While there will be 8x fewer ZODB fetches
required to traverse a complete tree, unpickling a single bucket could
be up to 8x slower. If you store large keys or values, that may be a
concern.

Conflict resolution in a bucket is ``O(n)``, so resolving conflicts
will take some time longer.

The ZODB cache is configured by number of objects, so if the total
number of BTree buckets goes down, then there's space for some more
objects. This is somewhat offset by the fact that fewer buckets means
less overhead and thus slightly less memory usage. We're talking about
a 8x reduction of buckets; exactly how much difference that makes
depends on what proportion of the cache is currently buckets.

The RelStorage cache is measured in bytes; overall pickle sizes should
also be about the same, just slightly smaller.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import sys

import BTrees
from BTrees.Interfaces import IBTreeFamily
from BTrees.Interfaces import IBTreeModule

from zope import interface

__all__ = (
    'MAX_LEAF_SIZE',
    'MAX_INTERNAL_SIZE',
    'family64LargeBuckets',
)

#: The value used for ``max_leaf_size`` in all
#: BTree classes available in :obj:`family64LargeBuckets`.
MAX_LEAF_SIZE = 500

#: The value used for ``max_internal_size`` in all
#: BTree classes available in :obj:`family64LargeBuckets`
MAX_INTERNAL_SIZE = MAX_LEAF_SIZE

# We use the same value to keep it simple and easier to predict.

def _make_large_module(existing_module, generic_prefix, real_prefix):
    new_module = type(existing_module)('nti.zodb.btrees.' + generic_prefix + 'BTree')
    provides = interface.providedBy(existing_module)
    interface.directlyProvides(new_module, provides)

    for tree_name in IBTreeModule:
        tree = getattr(existing_module, tree_name)
        new_tree = type(
            tree.__name__,
            (tree,),
            {
                '__slots__': (),
                'max_internal_size': MAX_INTERNAL_SIZE,
                'max_leaf_size': MAX_LEAF_SIZE,
                '__module__': new_module.__name__
            }
        )
        setattr(new_module, tree_name, new_tree)
        full_name = real_prefix + tree_name
        setattr(new_module, full_name, new_tree)

    for iface in provides:
        for name in iface:
            if not hasattr(new_module, name):
                setattr(new_module, name, getattr(existing_module, name))
    sys.modules[new_module.__name__] = new_module
    return new_module


@interface.implementer(IBTreeFamily)
class _Family64LargeBuckets(object):

    def __init__(self):
        self.maxint = BTrees.family64.maxint
        self.minint = BTrees.family64.minint
        self.maxuint = BTrees.family64.maxuint

        for name in IBTreeFamily:
            if hasattr(self, name):
                continue
            prefix = name.replace('I', 'L').replace('U', 'Q')
            mod = _make_large_module(
                getattr(BTrees.family64, name),
                name,
                prefix)
            mod.family = self
            setattr(self, name, mod)

    def __reduce__(self):
        return _family64LargeBuckets, ()


def _family64LargeBuckets():
    return family64LargeBuckets
_family64LargeBuckets.__safe_for_unpickling__ = True

#: A BTree family (:class:`BTrees.Interfaces.IBTreeFamily`)
#: where all modules have BTree and TreeSet objects that use
#: larger buckets than the default.
family64LargeBuckets = _Family64LargeBuckets()
