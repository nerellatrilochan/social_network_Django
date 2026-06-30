# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase04RefreshAuthTokensV1APITestCase.test_case status_code'] = '200'

snapshots['TestCase04RefreshAuthTokensV1APITestCase.test_case body'] = {
    'access_token': 'access_token',
    'expires_in': 10000,
    'refresh_token': 'refresh_token',
    'user_id': '1'
}
