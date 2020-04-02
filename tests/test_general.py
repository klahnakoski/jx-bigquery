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
from mo_future import text

import tests
from jx_bigquery.sql import ApiName


class TestGeneral(tests.TestBigQuery):
    def test_fix_bad_view(self):
        dataset = self.dataset

        # make sharded table
        table = dataset.create_or_replace_table(table=tests.table_name(), sharded=True)

        # drop table
        dataset.client.delete_table(
            text(dataset.full_name + ApiName(table.shard.table_id))
        )

        table.add(42)

        # make new table
        table2 = dataset.get_or_create_table(table=table.short_name, sharded=True)
        table2.merge_shards()
        # update view to new table
        result = jx.sort(table2.all_records())
        self.assertEqual(result, [42])
