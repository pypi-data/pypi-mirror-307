#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

# pylint: disable=protected-access
import unittest
from hamcrest import assert_that
from hamcrest import has_property
from hamcrest import has_length
from hamcrest import is_
from hamcrest import contains_exactly

from zope.testing.loggingsupport import InstalledHandler

from nti.zodb.activitylog import AbstractActivityMonitor as ActivityMonitor
from nti.zodb.activitylog import LogActivityMonitor
from nti.zodb.activitylog import LogActivityComponent
from nti.zodb.activitylog import StatsdActivityMonitor
from nti.zodb.activitylog import StatsdActivityComponent
from nti.zodb.activitylog import ActivityMonitorData
from nti.zodb.activitylog import ComponentActivityMonitor

AM_DATA = ActivityMonitorData(
    loads=1,
    stores=1,
    db_name='foo',
    pool_all_count=42,
    pool_idle_count=5
)

class TestAbstractActivityMonitor(unittest.TestCase):

    def test_delegate_properties(self):

        class Base(object):
            b = 1

        base = Base()
        mon = ActivityMonitor(base)

        assert_that(mon, has_property('b', 1))

    def test_closedConnection(self):
        from ZODB import DB
        from ZODB.DemoStorage import DemoStorage
        class Conn(DB.klass):
            loads = 1
            stores = 2

            def db(self):
                return db
            def getTransferCounts(self, clear=False):
                l, s = self.loads, self.stores
                if clear:
                    self.loads = self.stores = 0
                return l, s

        class MyDB(DB):
            klass = Conn

        db = MyDB(DemoStorage())
        database_name = 'DB'
        db.database_name = database_name
        self.addCleanup(db.close)

        db.klass = Conn

        called_component = []
        def component(data):
            called_component.append(1)
            assert_that(data.loads, is_(1))
            assert_that(data.stores, is_(2))
            assert_that(data.db_name, is_(database_name))
            assert_that(data.pool_all_count, is_(1))
            assert_that(data.pool_idle_count, is_(0))

        mon = ActivityMonitor(components=[component])
        conn = db.open()
        self.addCleanup(conn.close)

        mon.closedConnection(conn)

        assert_that(conn.loads, is_(0))
        assert_that(conn.stores, is_(0))
        assert_that(called_component, is_([1]))

class TestComponentActivityMonitor(unittest.TestCase):

    def test_get_loads_stores_with_base(self):
        class Base(object):
            closed = 0
            def closedConnection(self, _conn):
                self.closed += 1
                # Deliberately not calling anything on conn

        class Conn(object):
            database_name = 'DB'
            all = ()
            available = ()

            def db(self):
                return self

            @property
            def pool(self):
                return self

            loads = 1
            stores = 2

            def getTransferCounts(self, clear=False):
                l, s = self.loads, self.stores
                if clear:
                    self.loads = self.stores = 0
                return l, s

        base = Base()
        conn = Conn()
        mon = ComponentActivityMonitor(base)
        mon.closedConnection(conn)
        # transfer counts were cleared
        assert_that(conn, has_property('loads', 0))
        assert_that(conn, has_property('stores', 0))

        # Base was called once
        assert_that(base, has_property('closed', 1))


class TestLogActivityMonitor(unittest.TestCase):

    def setUp(self):
        super().setUp()
        self.handler = InstalledHandler('nti.zodb.activitylog')
        self.addCleanup(self.handler.uninstall)

    def _makeOne(self,
                 min_loads_and_stores=1000,
                 min_loads=1000,
                 min_stores=1000):
        mon = LogActivityMonitor()
        log = mon.components[0]
        log.min_loads_and_stores = min_loads_and_stores
        log.min_loads = min_loads
        log.min_stores = min_stores
        return log

    def _check_logs(self, log):
        log(AM_DATA)
        assert_that(self.handler.records, has_length(1))

    def test_combined_log_threshold_met(self):
        mon = self._makeOne(min_loads_and_stores=0)
        self._check_logs(mon)

    def test_combined_log_threshold_not_met(self):
        mon = self._makeOne(min_loads_and_stores=3)
        mon(AM_DATA)
        assert_that(self.handler.records, has_length(0))

    def test_load_threshold_met(self):
        mon = self._makeOne(min_loads=1)
        self._check_logs(mon)

    def test_store_threshold_met(self):
        mon = self._makeOne(min_loads=1)
        self._check_logs(mon)

    def test_all_thresholds_met(self):
        mon = self._makeOne(
            min_loads_and_stores=0,
            min_stores=0,
            min_loads=0)
        self._check_logs(mon)


class TestGetNonNegativeIntegerFromEnviron(unittest.TestCase):

    SETTING = 'NTI_ZODB_TESTING'

    def tearDown(self):
        import os
        try:
            del os.environ[self.SETTING]
        except KeyError:
            pass

    setUp = tearDown

    def _callFUT(self, default, env_value=None):
        from ..activitylog import _get_non_negative_integer_from_environ as FUT
        if env_value is not None:
            import os
            os.environ[self.SETTING] = env_value

        return FUT(self.SETTING, default)

    def test_no_value_return_default(self):
        assert_that(self._callFUT(self), is_(self))

    def test_negative_value_return_default(self):
        assert_that(self._callFUT(self, "-1"), is_(self))

    def test_malformed_value_return_default(self):
        assert_that(self._callFUT(self, "abc"), is_(self))

    def test_good_value(self):
        assert_that(self._callFUT(self, "42"), is_(42))


class TestStatsdLogActivityMonitor(unittest.TestCase):

    def test_closed_connection_no_client(self):
        mon = StatsdActivityMonitor()
        mon.statsd_client = lambda: None
        assert_that(mon.components[0], is_(StatsdActivityComponent))
        mon.components[0](AM_DATA)

    def test_closed_connection_with_client(self):
        glob_buf = []
        class MockClient(object):
            def gauge(self, key, value, buf):
                buf.append((key, value))
            def sendbuf(self, buf):
                glob_buf.extend(buf)

        mon = StatsdActivityComponent()
        mon.statsd_client = MockClient
        mon(AM_DATA)
        assert_that(glob_buf, is_([
            ('ZODB.DB.foo.loads', 1),
            ('ZODB.DB.foo.stores', 1),
            ('ZODB.DB.foo.total_connections', 42),
            ('ZODB.DB.foo.idle_connections', 5),
        ]))

class TestRegisterSubscriber(unittest.TestCase):

    def test_execute(self):
        from zope.processlifetime import DatabaseOpenedWithRoot
        from nti.zodb.activitylog import register_subscriber

        class DB(object):
            dam = None

            def __init__(self):
                self.databases = {'': self}
            def getActivityMonitor(self):
                return self.dam

            def setActivityMonitor(self, dam):
                self.dam = dam

        db = DB()
        db.setActivityMonitor(42)
        event = DatabaseOpenedWithRoot(db)

        register_subscriber(event)

        dam = db.getActivityMonitor()
        assert_that(dam, is_(ComponentActivityMonitor))
        assert_that(dam, has_property('base', is_(42)))
        assert_that(dam, has_property(
            'components',
            contains_exactly(is_(LogActivityComponent),
                             is_(StatsdActivityComponent))))
