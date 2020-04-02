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

import math
from collections import OrderedDict
from enum import Enum
from unittest import skipIf

from jx_base.expressions import NULL
from jx_python import jx
from mo_future import PY2
from mo_times import Date

import tests
from jx_bigquery.bigquery import Dataset


class TestInserts(tests.TestBigQuery):
    def test_primitives(self):
        dataset = self.dataset
        table = dataset.create_or_replace_table(table=tests.table_name(), sharded=True)
        table.add(42)
        table.add(None)
        table.add("test")
        table.add({})

        table.merge_shards()
        result = jx.sort(table.all_records(), ".")

        expected = [42, "test", NULL, NULL]

        self.assertEqual(result, expected)

    def test_array(self):
        dataset = self.dataset
        table = dataset.create_or_replace_table(table=tests.table_name(), sharded=True)
        table.add({"b": [1, 2, 3, 4, 5, 6]})
        table.merge_shards()
        result = jx.sort(table.all_records(), "a")

        expected = [{"b": [1, 2, 3, 4, 5, 6]}]
        self.assertEqual(result, expected)

    def test_one_then_many_then_merge(self):
        dataset = self.dataset
        table = dataset.create_or_replace_table(table=tests.table_name(), sharded=True)
        table.add({"a": 1, "b": {"c": 1, "d": 1}})
        table.add({"a": 2, "b": [{"c": 1, "d": 1}, {"c": 2, "d": 2}]})

        table.merge_shards()
        result = jx.sort(table.all_records(), "a")

        expected = [
            {"a": 1, "b": {"c": 1, "d": 1}},
            {"a": 2, "b": [{"c": 1, "d": 1}, {"c": 2, "d": 2}]},
        ]

        self.assertEqual(result, expected)

    def test_one_then_deep_arrays1(self):
        dataset = self.dataset
        table = dataset.create_or_replace_table(table=tests.table_name(), sharded=True)
        table.add({"a": 1, "b": {"c": [{"e": "e"}, {"e": 1}]}})
        table.add({"a": 2, "b": {"c": 1}})

        table.merge_shards()
        result = jx.sort(table.all_records(), "a")

        expected = [
            {"a": 1, "b": {"c": [{"e": "e"}, {"e": 1}]}},
            {"a": 2, "b": {"c": 1}},
        ]

        self.assertEqual(result, expected)

    def test_one_then_deep_arrays2(self):
        dataset = self.dataset
        table = dataset.create_or_replace_table(table=tests.table_name(), sharded=True)
        table.add({"a": 1, "b": {"c": [{"e": "e"}, {"e": 1}]}})
        table.add({"a": 2, "b": {"c": 1}})
        table.add({"a": 3, "b": [{"c": [{"e": 2}, {"e": 3}]}, {"c": 42}]})

        table.merge_shards()
        result = jx.sort(table.all_records(), "a")

        expected = [
            {"a": 1, "b": {"c": [{"e": "e"}, {"e": 1}]}},
            {"a": 2, "b": {"c": 1}},
            {"a": 3, "b": [{"c": [{"e": 2}, {"e": 3}]}, {"c": 42}]},
        ]

        self.assertEqual(result, expected)

    def test_inject_arrays(self):
        dataset = self.dataset
        table = dataset.create_or_replace_table(table=tests.table_name(), sharded=True)

        table.add({"a": 1, "b": {"c": {"e": 42}}})
        table.add({"a": 3, "b": [{"c": {"e": 2}}, {"c": {"e": 3}}]})

        table.merge_shards()
        result = jx.sort(table.all_records(), "a")

        expected = [
            {"a": 1, "b": {"c": {"e": 42}}},
            {"a": 3, "b": [{"c": {"e": 2}}, {"c": {"e": 3}}]},
        ]

        self.assertEqual(result, expected)

    def test_has_arrays(self):
        dataset = self.dataset
        table = dataset.create_or_replace_table(table=tests.table_name(), sharded=True)

        table.add({"a": 1, "b": {"c": {"e": 42}}})
        table.add({"a": 3, "b": [{"c": {"e": 2}}, {"c": {"e": 3}, "f": 42}]})

        table.merge_shards()
        result = jx.sort(table.all_records(), "a")

        expected = [
            {"a": 1, "b": {"c": {"e": 42}}},
            {"a": 3, "b": [{"c": {"e": 2}}, {"c": {"e": 3}}]},
        ]

        self.assertEqual(result, expected)

    def test_zero_array(self):
        dataset = self.dataset
        table = dataset.create_or_replace_table(table=tests.table_name(), sharded=True)

        table.add({"a": 3, "b": []})

        table.merge_shards()
        result = jx.sort(table.all_records(), "a")

        expected = [
            {"a": 3, "b": NULL},
        ]

        self.assertEqual(result, expected)

    def test_null(self):
        dataset = self.dataset
        table = dataset.create_or_replace_table(table=tests.table_name(), sharded=True)

        table.add({"a": 3, "b": None})

        table.merge_shards()
        result = jx.sort(table.all_records(), "a")

        expected = [
            {"a": 3, "b": NULL},
        ]

        self.assertEqual(result, expected)

    def test_infinity(self):
        dataset = self.dataset
        table = dataset.create_or_replace_table(table=tests.table_name(), sharded=True)

        table.add({"a": 3, "b": -math.inf})

        table.merge_shards()
        result = jx.sort(table.all_records(), "a")

        expected = [
            {"a": 3, "b": NULL},
        ]

        self.assertEqual(result, expected)

    @skipIf(PY2, "no enums for python 2")
    def test_enum(self):
        class Status(Enum):
            PASS = 0
            FAIL = 1
            INTERMITTENT = 2

        dataset = self.dataset
        table = dataset.create_or_replace_table(table=tests.table_name(), sharded=True)

        table.add({"a": Status.PASS})

        table.merge_shards()
        result = jx.sort(table.all_records(), "a")

        expected = [
            {"a": "PASS"},
        ]

        self.assertEqual(result, expected)

    def test_encoding_on_deep_arrays(self):
        dataset = self.dataset
        table = dataset.create_or_replace_table(table=tests.table_name(), sharded=True)
        table.add({"__a": 1, "__b": {"__c": [{"__e": "e"}, {"__e": 1}]}})
        table.add({"__a": 2, "__b": {"__c": 1}})
        table.add({"__a": 3, "__b": [{"__c": [{"__e": 2}, {"__e": 3}]}]})

        table.merge_shards()
        result = jx.sort(table.all_records(), "__a")

        expected = [
            {"__a": 1, "__b": {"__c": [{"__e": "e"}, {"__e": 1}]}},
            {"__a": 2, "__b": {"__c": 1}},
            {"__a": 3, "__b": {"__c": [{"__e": 2}, {"__e": 3}]}},
        ]

        self.assertEqual(result, expected)

    def test_top_level_field_order(self):
        dataset = self.dataset

        table = dataset.create_or_replace_table(
            table=tests.table_name(),
            sharded=True,
            schema={"push": {"id": {"_i_": "integer"}}, "etl": {"timestamp": {"_t_": "time"}}},
            # REVERSE ALPHABTICAL ORDER
            top_level_fields=OrderedDict([
                ("push", {"id": "_push_id"}),
                ("etl", {"timestamp": "_etl_timestamp"})
            ]),
        )
        today = Date.today()
        now = Date.now()
        table.add({"push": {"id": 1}, "etl": {"timestamp": today}, "a": 1})
        table.add({"push": {"id": 2}, "etl": {"timestamp": now}, "b": 2})

        table.merge_shards()
        result = jx.sort(table.all_records(), "push.id")

        expected = [
            {"push": {"id": 1}, "etl": {"timestamp": today}, "a": 1},
            {"push": {"id": 2}, "etl": {"timestamp": now}, "b": 2},
        ]

        self.assertAlmostEqual(result, expected, places=10)
