# -*- coding: utf-8 -*-
"""

    MongoDB result store backend.

"""
from __future__ import absolute_import

from datetime import datetime
from kombu.utils import cached_property
from django.conf import settings
try:
    import pymongo
except ImportError:  # pragma: no cover
    pymongo = None   # noqa

if pymongo:
    try:
        from bson.binary import Binary
    except ImportError:                     # pragma: no cover
        from pymongo.binary import Binary   # noqa
    from pymongo.errors import InvalidDocument  # noqa
else:                                       # pragma: no cover
    Binary = None                           # noqa
    InvalidDocument = None                  # noqa



from kombu.utils import cached_property


__all__ = ['MongoBackend']


class MongoBackend(object):
    host = 'localhost'
    port = 27017
    user = None
    password = None
    database_name = 'wordfeed'
    _words_collection = 'words'
    max_pool_size = 100
    options = None

    supports_autoexpire = False

    _connection = None

    def __init__(self,database_name=None, *args, **kwargs):
        """Initialize MongoDB backend instance.

        :raises qga.exceptions.ImproperlyConfigured: if
            module :mod:`pymongo` is not available.

        """
        if not pymongo:
            raise ImproperlyConfigured(
                'You need to install the pymongo library to use the '
                'MongoDB backend.')

        config = settings.MONGODB_BACKEND_SETTINGS
        if config is not None:
            if not isinstance(config, dict):
                raise ImproperlyConfigured(
                    'MongoDB backend settings should be grouped in a dict')
            config = dict(config)  # do not modify original
            self.host = config.pop('host', self.host)
            self.port = int(config.pop('port', self.port))
            self.user = config.pop('user', self.user)
            self.password = config.pop('password', self.password)
            self.database_name = config.pop('database', self.database_name)
            self._words_collection = config.pop(
                'words_collection', self._words_collection,
            )
            # Set option defaults
            self.options.setdefault('max_pool_size', self.max_pool_size)
            self.options.setdefault('auto_start_request', False)
            
        url = kwargs.get('url')
        if url:
            # Specifying backend as an URL
            self.host = url
        db_name = kwargs.get('database_name')
        if db_name:
            self.database_name = db_name
        if database_name:
            self.database_name = database_name

    def _get_connection(self):
        """Connect to the MongoDB server."""
        if self._connection is None:
            from pymongo import MongoClient
            url = self.host
            self._connection = MongoClient(host=url, **self.options)

        return self._connection

    def _get_database(self):
        conn = self._get_connection()
        db = conn[self.database_name]
        if self.user and self.password:
            if not db.authenticate(self.user,
                                   self.password):
                raise ImproperlyConfigured(
                    'Invalid MongoDB username or password.')
        return db

    @cached_property
    def database(self):
        """Get database from MongoDB connection and perform authentication
        if necessary."""
        return self._get_database()

    @cached_property
    def words_collection(self):
        """Get the metadata task collection."""
        collection = self.database[self._words_collection]

        # Ensure an index on TIME_STAMP is there, if not process the index
        # in the background. Once completed cleanup will be much faster
        collection.ensure_index('TIME_STAMP', background='true')
        return collection