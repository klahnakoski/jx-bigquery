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

from jx_python import jx

import tests
from jx_bigquery.bigquery import Dataset


class TestInerts(tests.TestBigQuery):
    def test_one_then_many_then_merge(self):
        dataset = Dataset("testing", kwargs=tests.config.destination)
        table1 = dataset.create_or_replace_table(table="table1", sharded=True)
        table1.add({"a": 1, "b": {"c": 1, "d": 1}})
        table1.add({"a": 2, "b": [{"c": 1, "d": 1}, {"c": 2, "d": 2}]})

        table1.merge_shards()
        result = jx.sort(table1.all_records(), "a")

        expected = [
            {"a": 1, "b": {"c": 1, "d": 1}},
            {"a": 2, "b": [{"c": 1, "d": 1}, {"c": 2, "d": 2}]},
        ]

        self.assertEqual(result, expected)

    def test_one_then_deep_arrays1(self):
        dataset = Dataset("testing", kwargs=tests.config.destination)
        table2 = dataset.create_or_replace_table(table="table2", sharded=True)
        table2.add({"a": 1, "b": {"c": [{"e": "e"}, {"e": 1}]}})
        table2.add({"a": 2, "b": {"c": 1}})

        table2.merge_shards()
        result = jx.sort(table2.all_records(), "a")

        expected = [
            {"a": 1, "b": {"c": [{"e": "e"}, {"e": 1}]}},
            {"a": 2, "b": {"c": 1}},
        ]

        self.assertEqual(result, expected)

    def test_one_then_deep_arrays2(self):
        dataset = Dataset("testing", kwargs=tests.config.destination)
        table2 = dataset.create_or_replace_table(table="table2", sharded=True)
        table2.add({"a": 1, "b": {"c": [{"e": "e"}, {"e": 1}]}})
        table2.add({"a": 2, "b": {"c": 1}})
        table2.add({"a": 3, "b": [{"c": [{"e": 2}, {"e": 3}]}]})

        table2.merge_shards()
        result = jx.sort(table2.all_records(), "a")

        expected = [
            {"a": 1, "b": {"c": [{"e": "e"}, {"e": 1}]}},
            {"a": 2, "b": {"c": 1}},
            {"a": 3, "b": [{"c": [{"e": 2}, {"e": 3}]}]},
        ]

        self.assertEqual(result, expected)

    def test_encoding_on_deep_arrays(self):
        dataset = Dataset("testing", kwargs=tests.config.destination)
        table2 = dataset.create_or_replace_table(table="table2", sharded=True)
        table2.add({"__a": 1, "__b": {"__c": [{"__e": "e"}, {"__e": 1}]}})
        table2.add({"__a": 2, "__b": {"__c": 1}})
        table2.add({"__a": 3, "__b": [{"__c": [{"__e": 2}, {"__e": 3}]}]})

        table2.merge_shards()
        result = table2.all_records()

        expected = [
            {"__a": 1, "__b": {"__c": [{"__e": "e"}, {"__e": 1}]}},
            {"__a": 2, "__b": {"__c": 1}},
            {"__a": 3, "__b": [{"__c": [{"__e": 2}, {"__e": 3}]}]},
        ]

        self.assertEqual(result, expected)
