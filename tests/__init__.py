
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

from mo_logs import constants, startup, Log
from mo_testing.fuzzytestcase import FuzzyTestCase


config = None


class TestBigQuery(FuzzyTestCase):

    @classmethod
    def setUpClass(cls):
        global config
        config = startup.read_settings(filename="tests/config.json")
        constants.set(config.constants)
        Log.start(config.debug)







