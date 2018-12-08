from __future__ import with_statement
import sys
import unittest
import tempfile
import datetime
import pytz

import firebirdsql
from firebirdsql.tests.base import *
from firebirdsql.consts import *


class TestTimeZone(TestBase):
    def setUp(self):
        self.database=tempfile.mktemp()
        self.connection = firebirdsql.create_database(
                auth_plugin_name=self.auth_plugin_name,
                wire_crypt=self.wire_crypt,
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                page_size=self.page_size,
                tz_name='Asia/Tokyo')

    def test_time_zone(self):
        """
        For FB4
        """
        cur = self.connection.cursor()
        cur.execute('''
            CREATE TABLE tz_test (
                a INTEGER NOT NULL,
                b TIME WITH TIME ZONE DEFAULT '12:34:56',
                c TIMESTAMP WITH TIME ZONE DEFAULT '1967-08-11 23:45:01',
                PRIMARY KEY (a)
            )
        ''')
        cur.close()
        self.connection.commit()

        cur = self.connection.cursor()
        cur.execute("insert into tz_test (a) values (1)")

        tzinfo = pytz.timezone('Asia/Tokyo')
        cur.execute(
            "insert into tz_test (a, b, c) values (1, ?, ?)", [
                datetime.time(12, 34, 56, tzinfo=tzinfo),
                datetime.datetime(1967, 8, 11, 23, 45, 1, tzinfo=tzinfo)
            ]
        )

        cur = self.connection.cursor()
        cur.execute("select * from tz_test")
        for a, b, c in cur.fetchall():
            print(a, b, c)
            pass

        self.connection.close()

