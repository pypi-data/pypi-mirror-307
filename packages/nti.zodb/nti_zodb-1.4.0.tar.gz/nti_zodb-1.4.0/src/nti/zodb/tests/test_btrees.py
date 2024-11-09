# -*- coding: utf-8 -*-
"""
Tests for btrees.py

"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904
import subprocess
import tempfile
import os
import sys
import operator
import unittest

from BTrees.Interfaces import IBTreeFamily
from BTrees.Interfaces import IBTreeModule

from hamcrest import assert_that
from hamcrest import is_
from hamcrest import same_instance
from hamcrest import has_property
from hamcrest import has_length
from hamcrest import not_none
from hamcrest import none

from nti.testing.matchers import verifiably_provides

from nti.zodb import btrees

class TestFamily(unittest.TestCase):

    def test_provides(self):
        assert_that(
            btrees.family64LargeBuckets,
            verifiably_provides(IBTreeFamily)
        )

    def test_pickle(self):
        from pickle import loads
        from pickle import dumps

        assert_that(
            loads(dumps(btrees.family64LargeBuckets)),
            is_(same_instance(btrees.family64LargeBuckets))
        )

    def test_module_provides(self):

        from BTrees import family64
        from zope.interface import providedBy

        for name in IBTreeFamily:
            if 'int' in name:
                continue
            module = getattr(btrees.family64LargeBuckets, name)
            assert_that(module, verifiably_provides(IBTreeModule))
            assert_that(module, verifiably_provides(*providedBy(
                getattr(family64, name)
            )))
            # That checks the un-adorned names like BTree; it doesn't
            # check that the prefix names are available.
            for attr_name in IBTreeModule:
                # The names are generic for 32-bit; the real named objects
                # are 64-bit
                prefix = name.replace('I', 'L').replace('U', 'Q')
                dec_attr_name = prefix + attr_name
                tree = getattr(module, attr_name)
                assert_that(module,
                            has_property(dec_attr_name,
                                         same_instance(tree)))

                assert_that(tree, has_property('max_leaf_size',
                                               btrees.MAX_LEAF_SIZE))
                assert_that(tree, has_property('max_internal_size',
                                               btrees.MAX_INTERNAL_SIZE))

class TestBTree(unittest.TestCase):

    def _check_bucket_sizes(self, mod_name, kind_name, populate):
        mod = getattr(btrees.family64LargeBuckets, mod_name)
        kind = getattr(mod, kind_name)
        btree = kind()
        # Putting exactly MAX_LEAF_SIZE keeps exactly one bucket.
        for x in range(btrees.MAX_LEAF_SIZE):
            populate(btree, x, x)

        assert_that(btree, has_property('_firstbucket', not_none()))
        bucket = btree._firstbucket
        assert_that(bucket, has_length(btrees.MAX_LEAF_SIZE))
        assert_that(bucket, has_property('_next'), none())

        # max_internal_size is interesting. Basically, all except the
        # last node in the linked list will have exactly have that
        # value; the last node can have up to max_internal_size -
        # max_internal_size/2 values. before it splits
        for x in range(btrees.MAX_LEAF_SIZE * 3 + (btrees.MAX_INTERNAL_SIZE // 2)):
            populate(btree, x, x)

        bucket = btree._firstbucket
        assert_that(bucket, has_length(btrees.MAX_INTERNAL_SIZE / 2)) # 1
        bucket = bucket._next
        assert_that(bucket, has_length(btrees.MAX_INTERNAL_SIZE / 2)) # 2
        bucket = bucket._next
        assert_that(bucket, has_length(btrees.MAX_INTERNAL_SIZE / 2)) # 3
        bucket = bucket._next
        assert_that(bucket, has_length(btrees.MAX_INTERNAL_SIZE / 2)) # 4
        bucket = bucket._next
        assert_that(bucket, has_length(btrees.MAX_INTERNAL_SIZE / 2)) # 5
        bucket = bucket._next
        assert_that(bucket, has_length(btrees.MAX_LEAF_SIZE)) # 6

        self._check_pickle(btree)

    def _check_pickle(self, obj):
        pickle_modules = []
        import pickle
        pickle_modules.append(pickle)
        try:
            import cPickle
        except ImportError:
            pass
        else:
            pickle_modules.append(cPickle)

        import zodbpickle.slowpickle
        pickle_modules.append(zodbpickle.slowpickle)
        try:
            import zodbpickle.fastpickle
        except ImportError:
            pass
        else:
            pickle_modules.append(zodbpickle.fastpickle)

        # in process tests first
        for pickle_module in pickle_modules:
            for proto in range(0, pickle_module.HIGHEST_PROTOCOL):
                obj_dump = pickle_module.dumps(obj, proto)
                copy = pickle_module.loads(obj_dump)
                copy_dump = pickle_module.dumps(copy, proto)
                assert_that(copy_dump, is_(obj_dump))
                if hasattr(copy, 'items'):
                    assert_that(dict(copy), is_(dict(obj)))
                else:
                    assert_that(list(copy), is_(list(obj)))

        # Next, make sure that a fresh process that has never imported
        # this module can unpickle them. This is important to test because
        # we dynamically create the classes and modules (and we treat btrees.py as if it
        # were a package instead of a module)
        obj_dump = pickle.dumps(obj)
        fd, fname = tempfile.mkstemp('.test_btrees')
        self.addCleanup(os.remove, fname)
        f = os.fdopen(fd, 'wb')
        f.write(obj_dump)
        f.close()
        subprocess.check_call(
            [sys.executable, '-c',
             'import pickle; f = open("%s", "rb"); x = pickle.load(f); f.close()' % (
                 fname
             )
            ]
        )

    _bt_pop = operator.setitem
    def _set_pop(self, treeset, x, _):
        treeset.add(x)


    for name in IBTreeFamily:
        if 'int' in name:
            continue
        tname = 'test_' + name + '_BTree'
        locals()[tname] = lambda self, kind=name: self._check_bucket_sizes(kind, 'BTree',
                                                                           self._bt_pop)

        tname = 'test_' + name + '_TreeSet'
        locals()[tname] = lambda self, kind=name: self._check_bucket_sizes(kind, 'TreeSet',
                                                                           self._set_pop)
