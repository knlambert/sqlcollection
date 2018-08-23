# coding utf-8
"""
Contains the Client class.
"""

import re
from .db import DB
from sqlalchemy import (
    create_engine,
    inspect
)


class Client(object):
    """
    Handles the connection to a database.
    """
    def __init__(self, url=None):
        """
        Construct the object.
        Args:
            url (unicode): The db connection string.
        """
        self._url = url

    def __getattr__(self, name):
        """
        Called when a user try to access to an attribute of the object.
        Used to catch the DB name.
        Args:
            name (unicode): The name of the db to fetch.

        Returns:
            The attribute attribute.
        """
        if name not in self.__dict__:
            setattr(self, name, DB(
                url=self.adapt_url(name)
            ))

        return self.__dict__[name]

    def get_engine(self):
        """
        Creates the SQLAlchemy Engine.
        Returns:
            (sqlalchemy.engine.Engine): The created Engine.
        """
        return create_engine(self._url)

    def adapt_url(self, schema_name):
        """
        Adapt the url to connect to the right database.
        Args:
            schema_name (unicode): The name of the DB to inject in the url.

        Returns:
            (unicode): The modified url.
        """
        url = self._url

        if u"cloudsql" in self._url:
            regex = u"(\S+)\/([^\/]+)(\?.+\/cloudsql\/.+)"
            m = re.search(regex, self._url)
            groups = list(m.groups())
            groups[1] = schema_name
            url = u"{}/{}{}".format(*groups)

        else:
            url = u"{}/{}".format(self._url.rstrip(u"/"), schema_name)
        return url

