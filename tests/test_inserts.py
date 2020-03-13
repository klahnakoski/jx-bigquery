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

import tests
from jx_bigquery.bigquery import Dataset


class TestInerts(tests.TestBigQuery):

    def test_one_then_many_then_merge(self):
        dataset = Dataset("testing", kwargs=tests.config.destination)
        table1 = dataset.create_or_replace_table(table="table1", sharded=True)
        table1.add({"a": 1, "b": {"c": 1, "d": 1}})
        table1.add({"a": 1, "b": [{"c": 1, "d": 1}, {"c": 2, "d": 2}]})

        table1.merge_shards()
        result = table1.all_records()

        expected = [
            {"a": 1, "b": {"c": 1, "d": 1}},
            {"a": 1, "b": [{"c": 1, "d": 1}, {"c": 2, "d": 2}]}
        ]

        self.assertEqual(result, expected)
