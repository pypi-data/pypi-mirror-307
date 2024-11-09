#!/usr/bin/env python
# -*- coding: utf-8 -*-

__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import assert_that

from nti.testing.matchers import is_true
from nti.testing.matchers import is_false
from nti.testing.matchers import validly_provides


import unittest
from unittest import mock as fudge

from nti.zodb import interfaces

from nti.zodb.tokenbucket import PersistentTokenBucket

from nti.zodb.tests import SharedConfiguringTestLayer


class TestTokenBucket(unittest.TestCase):

    layer = SharedConfiguringTestLayer

    def test_provides(self):
        bucket = PersistentTokenBucket(80, 1)
        assert_that(bucket, validly_provides(interfaces.ITokenBucket))

    @fudge.patch('nti.zodb.tokenbucket.time')
    def test_consume(self, fudge_time):

        fudge_time.is_callable()
        fudge_time.return_value = 0
        bucket = PersistentTokenBucket(2)

        assert_that(bucket, validly_provides(interfaces.ITokenBucket))

        # at time 0, the bucket has two tokens in it
        assert_that(bucket.consume(), is_true())
        assert_that(bucket.consume(), is_true())

        # Which are now gone
        assert_that(bucket.consume(), is_false())

        # If we strobe the clock forward, we can get another token, since
        # we are refilling at one per second
        fudge_time.return_value = 1

        assert_that(bucket.consume(), is_true())
        assert_that(bucket.consume(), is_false())

        # skip forward two seconds, and we can consume both tokens again
        fudge_time.return_value = 3
        assert_that(bucket.consume(2), is_true())
        assert_that(bucket.consume(), is_false())

        # cover
        assert_that(repr(bucket), is_('PersistentTokenBucket(2.0,1.0)'))

    @fudge.patch('nti.zodb.tokenbucket.sleep')
    @fudge.patch('nti.zodb.tokenbucket.time')
    def test_wait(self, fudge_time, fudge_sleep):
        fudge_time.return_value = 0
        bucket = PersistentTokenBucket(2)

        # at time 0, the bucket has two tokens in it
        assert_that(bucket.wait_for_token(), is_true())
        assert_that(bucket.wait_for_token(), is_true())

        # Which are now gone
        assert_that(bucket.consume(), is_false())

        def _sleep(how_long):
            # If we strobe the clock forward, we can get another token, since
            # we are refilling at one per second
            assert_that(how_long, is_(1.0))
            fudge_time.return_value = 1

        fudge_sleep.side_effect = _sleep
        # Sleep gets called, strobes the clock, and we move forward
        assert_that(bucket.wait_for_token(), is_true())
