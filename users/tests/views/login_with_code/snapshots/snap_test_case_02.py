# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase02LoginWithCodeAPITestCase.test_case status_code'] = '200'

snapshots['TestCase02LoginWithCodeAPITestCase.test_case body'] = {
    'access_token': 'access_token',
    'expires_in': 36000,
    'refresh_token': 'refresh_token'
}
