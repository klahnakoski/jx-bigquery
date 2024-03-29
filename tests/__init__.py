# encoding: utf-8
#
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http:# mozilla.org/MPL/2.0/.
#
# Contact: Kyle Lahnakoski (kyle@lahnakoski.com)
#
from __future__ import absolute_import, division, unicode_literals

from mo_future import NEXT, text
from mo_logs import constants, startup, Log
from mo_testing.fuzzytestcase import FuzzyTestCase
from mo_times import Timer

from jx_bigquery import bigquery
from jx_bigquery.bigquery import Dataset

TESTING_DATASET = "testing"


def table_name():
    i = 0
    while True:
        yield "table" + text(i)
        i = i + 1


table_name = NEXT(table_name())


def delete_dataset():
    client = bigquery.connect(config.destination.account_info)
    existing = bigquery.find_dataset(TESTING_DATASET, client)
    if existing:
        with Timer("delete dataset {{dataset}}", {"dataset": TESTING_DATASET}):
            client.delete_dataset(existing, delete_contents=True)


class TestBigQuery(FuzzyTestCase):
    @classmethod
    def setUpClass(cls):
        bigquery.DEBUG = True


config = startup.read_settings(filename="tests/config.json")
constants.set(config.constants)
Log.start(config.debug)

delete_dataset()
TestBigQuery.dataset = Dataset(TESTING_DATASET, kwargs=config.destination)
