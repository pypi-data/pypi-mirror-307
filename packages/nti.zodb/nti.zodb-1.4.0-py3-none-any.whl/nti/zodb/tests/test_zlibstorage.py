#!/usr/bin/env python
# -*- coding: utf-8 -*-


__docformat__ = "restructuredtext en"

# disable: accessing protected members, too many methods
# pylint: disable=W0212,R0904

from hamcrest import is_
from hamcrest import is_in
from hamcrest import assert_that
from hamcrest import has_property
from hamcrest import not_none

import unittest
from unittest import mock as fudge

from nti.zodb.zlibstorage import ZlibStorageClientStorageURIResolver
from nti.zodb.zlibstorage import ZlibStorageFileStorageURIResolver


class TestZlibStorage(unittest.TestCase):


    def test_resolve_zeo(self):
        with fudge.patch('ZEO.ClientStorage.ClientStorage') as mock_cs, \
             fudge.patch('zc.zlibstorage.ZlibStorage'), \
             fudge.patch('ZODB.DB') as mock_db:
            uri = ('zlibzeo:///dev/null/Users/jmadden/Projects/DsEnvs/AlphaExport/var/zeosocket'
                   '?connection_cache_size=25000'
                   '&cache_size=104857600&storage=1'
                   '&database_name=Users'
                   '&blob_dir=/Users/jmadden/Projects/DsEnvs/AlphaExport/data/data.fs.blobs'
                   '&shared_blob_dir=True')

            _, _, kw, factory = ZlibStorageClientStorageURIResolver()(uri)

            assert_that(kw, is_({
                'blob_dir': '/Users/jmadden/Projects/DsEnvs/AlphaExport/data/data.fs.blobs',
                'cache_size': 104857600,
                'shared_blob_dir': 1,
                'storage': '1'}))
            assert_that(factory, has_property('__name__', 'zlibfactory'))

            mock_cs.return_value = 1
            mock_db.return_value = 2

            assert_that(factory(), is_(2))


    def test_resolve_file(self):
        with fudge.patch('repoze.zodbconn.resolvers.FileStorage'), \
             fudge.patch('zc.zlibstorage.ZlibStorage') as fudge_zstor, \
             fudge.patch('repoze.zodbconn.resolvers.DB'):
            uri = ('zlibfile:///dev/null/Users/jmadden/Projects/DsEnvs/AlphaExport/var/zeosocket'
                   '?connection_cache_size=25000'
                   '&cache_size=104857600&storage=1'
                   '&database_name=Users'
                   '&blob_dir=/Users/jmadden/Projects/DsEnvs/AlphaExport/data/data.fs.blobs'
                   '&shared_blob_dir=True')

            _, _, kw, factory = ZlibStorageFileStorageURIResolver()(uri)

            assert_that(kw, is_({}))


            assert_that(factory, has_property('__name__', 'zlibfactory'))

            fudge_zstor.return_value = 1

            assert_that(factory(), is_(not_none()))

    def test_install(self):
        from repoze.zodbconn import resolvers
        from nti.zodb.zlibstorage import install_zlib_client_resolver

        before = resolvers.RESOLVERS.copy()
        install_zlib_client_resolver()
        try:
            assert_that('zlibfile', is_in(resolvers.RESOLVERS))
            assert_that('zlibzeo', is_in(resolvers.RESOLVERS))
        finally:
            resolvers.RESOLVERS = before
