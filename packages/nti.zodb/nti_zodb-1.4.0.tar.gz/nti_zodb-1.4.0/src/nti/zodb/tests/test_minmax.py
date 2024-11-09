#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# pylint: disable=protected-access

import unittest
import pickle

from hamcrest import is_
from hamcrest import raises
from hamcrest import has_key
from hamcrest import calling
from hamcrest import less_than
from hamcrest import assert_that
from hamcrest import has_property
from hamcrest import greater_than
from hamcrest import same_instance
from hamcrest import less_than_or_equal_to

from nti.testing.matchers import validly_provides
from nti.testing.matchers import verifiably_provides

from nti.zodb import interfaces
from nti.zodb.minmax import Maximum
from nti.zodb.minmax import Minimum
from nti.zodb.minmax import MergingCounter
from nti.zodb.minmax import NumericMaximum
from nti.zodb.minmax import NumericMinimum
from nti.zodb.minmax import ConstantZeroValue
from nti.zodb.minmax import NumericPropertyDefaultingToZero
from nti.zodb.persistentproperty import PersistentPropertyHolder

from ZODB import DB


class TestModule(unittest.TestCase):
    def test_zope_imports_have_set(self):
        for t in Minimum, Maximum:
            v = t(0)
            v.set(1)
            assert_that(v.value, is_(1))

class NumericValueMixin(object):

    def _makeOne(self, *args):
        raise NotImplementedError

    def test_numeric_value_interface(self):
        val = self._makeOne()
        assert_that(val, verifiably_provides(interfaces.INumericValue))

    def test_comparisons(self):
        mc1 = self._makeOne()
        mc2 = self._makeOne()

        assert_that(mc1, is_(mc2))

        try:
            mc2.increment()
        except NotImplementedError:
            self.skipTest("Does not support incrementing.")

        assert_that(mc1, is_(less_than(mc2)))
        assert_that(mc2, is_(greater_than(mc1)))

        mc1.increment()
        assert_that(mc1, is_(less_than_or_equal_to(mc2)))

        assert_that(hash(mc1), is_(mc1.value))

    def test_add(self):
        try:
            mc1 = self._makeOne(1)
        except NotImplementedError:
            self.skipTest("Does not support initial values")
        mc2 = self._makeOne(2)

        assert_that(mc1 + mc2, is_(self._makeOne(3)))

        assert_that(mc1 + 2, is_(3))

        mc1 += 2
        assert_that(mc1, is_(self._makeOne(3)))


class TestMergingCounter(NumericValueMixin,
                         unittest.TestCase):

    def _makeOne(self, *args):
        return MergingCounter(*args)

    def test_numeric_counter_interface(self):
        assert_that(self._makeOne(),
                    validly_provides(interfaces.INumericCounter))

    def test_merge_resolve(self):
        # (original state, currently committed, desired)
        mc = self._makeOne()
        assert_that(mc._p_resolveConflict(0, 0, 1), is_(1))
        # simultaneous increment adds
        assert_that(mc._p_resolveConflict(0, 1, 1), is_(2))
        # In the special case that both set it to zero, it becomes 0
        assert_that(mc._p_resolveConflict(10, 0, 0), is_(0))

    def test_str(self):

        mc = MergingCounter()
        assert_that(str(mc), is_("0"))
        assert_that(repr(mc), is_("MergingCounter(0)"))

        mc.set(1)
        assert_that(str(mc), is_("1"))
        assert_that(repr(mc), is_("MergingCounter(1)"))


class TestConstantZeroValue(NumericValueMixin,
                            unittest.TestCase):

    def _makeOne(self, *args):
        return ConstantZeroValue(*args)

    def test_zero(self):
        czv = ConstantZeroValue()
        assert_that(czv, is_(same_instance(ConstantZeroValue())))
        assert_that(czv, has_property('value', 0))

        # equality
        assert_that(czv, is_(czv))
        v = NumericMaximum()
        assert_that(czv, is_(v))
        assert_that(v, is_(czv))

        v.value = -1
        assert_that(v, is_(less_than(czv)))

        v.value = 1
        assert_that(v, is_(greater_than(czv)))

        czv.value = 1
        assert_that(czv, has_property('value', 0))

        czv.set(2)
        assert_that(czv, has_property('value', 0))

        assert_that(calling(pickle.dumps).with_args(czv),
                    raises(TypeError))
        assert_that(calling(czv._p_resolveConflict).with_args(None, None, None),
                    raises(NotImplementedError))


class TestNumericMinumum(NumericValueMixin,
                         unittest.TestCase):

    def _makeOne(self, *args):
        return NumericMinimum(*args)

    def test_min_resolve(self):
        assert_that(NumericMinimum()._p_resolveConflict(0, 0, 1), is_(0))
        assert_that(NumericMinimum()._p_resolveConflict(3, 4, 2), is_(2))

class TestNumericMaximum(NumericValueMixin,
                         unittest.TestCase):

    def _makeOne(self, *args):
        return NumericMaximum(*args)

    def test_max_resolve(self):
        assert_that(self._makeOne()._p_resolveConflict(0, 0, 1), is_(1))
        assert_that(self._makeOne()._p_resolveConflict(3, 4, 2), is_(4))



class WithProperty(PersistentPropertyHolder):

    a = NumericPropertyDefaultingToZero(
        'a',
        NumericMaximum,
        as_number=True)
    b = NumericPropertyDefaultingToZero('b', MergingCounter)

class NPProperty(object):
    a = NumericPropertyDefaultingToZero(
        'a',
        NumericMaximum,
        as_number=True)
    b = NumericPropertyDefaultingToZero('b', MergingCounter)


class TestPropertyNonPersistent(unittest.TestCase):

    def make_one(self):
        obj = NPProperty()
        return obj

    def test_all_works(self):
        obj = self.make_one()

        assert_that(obj.a, is_(0))

        del obj.a
        assert_that(obj.a, is_(0))

        obj.a = 0
        assert_that(obj.a, is_(0))
        self.assertNotIn('a', obj.__dict__)

        obj.a = 1
        assert_that(obj.a, is_(1))

        obj.a = 2
        assert_that(obj.a, is_(2))

        del obj.a
        assert_that(obj.a, is_(0))

        assert_that(obj.b, is_(type(ConstantZeroValue())))

        # No change
        obj.b.set(0)
        assert_that(obj.b, is_(type(ConstantZeroValue())))


class TestProperty(TestPropertyNonPersistent):

    def make_one(self):
        db = DB(None)
        conn = db.open()

        obj = WithProperty()
        conn.add(obj)
        return obj

    def test_get_klass(self):
        assert_that(WithProperty.a, is_(NumericPropertyDefaultingToZero))

    def test_zero_property_increment(self):
        obj = self.make_one()

        assert_that(obj._p_status, is_('saved'))

        # Just accessing them doesn't change the saved status
        assert_that(obj.a, is_(0))
        assert_that(obj._p_status, is_('saved'))

        assert_that(obj.b.value, is_(0))
        assert_that(obj._p_status, is_('saved'))

        assert_that(obj.__getstate__(), is_({}))

        # Only when we do something does the status change
        obj.b.increment()
        assert_that(obj._p_status, is_('changed'))
        assert_that(obj.b, is_(same_instance(obj.b)))
        assert_that(obj.__getstate__(), has_key('b'))
        assert_that(obj.b, is_(MergingCounter))

    def test_zero_property_set(self):
        obj = self.make_one()

        assert_that(obj._p_status, is_('saved'))

        # Just accessing them doesn't change the saved status
        assert_that(obj.a, is_(0))
        assert_that(obj._p_status, is_('saved'))

        assert_that(obj.b.value, is_(0))
        assert_that(obj._p_status, is_('saved'))

        assert_that(obj.__getstate__(), is_({}))

        # Only when we do something does the status change
        obj.b.set(3)
        assert_that(obj._p_status, is_('changed'))
        assert_that(obj.b, is_(same_instance(obj.b)))
        assert_that(obj.__getstate__(), has_key('b'))
        assert_that(obj.b.value, is_(3))

    def test_zero_property_value(self):
        obj = self.make_one()

        assert_that(obj._p_status, is_('saved'))

        # Just accessing them doesn't change the saved status
        assert_that(obj.a, is_(0))
        assert_that(obj._p_status, is_('saved'))

        assert_that(obj.b.value, is_(0))
        assert_that(obj._p_status, is_('saved'))

        assert_that(obj.__getstate__(), is_({}))

        # Only when we do something does the status change
        obj.a = 3
        assert_that(obj._p_status, is_('changed'))
        assert_that(obj.a, is_(same_instance(obj.a)))
        assert_that(obj.__getstate__(), has_key('a'))
        assert_that(obj.a, is_(3))
