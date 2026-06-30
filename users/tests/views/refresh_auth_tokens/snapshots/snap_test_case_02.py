# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase02RefreshAuthTokensV1APITestCase.test_case status_code'] = '400'

snapshots['TestCase02RefreshAuthTokensV1APITestCase.test_case body'] = {
    'http_status_code': 400,
    'res_status': 'REFRESH_TOKEN_EXPIRED',
    'response': 'Refresh Token Expired'
}
