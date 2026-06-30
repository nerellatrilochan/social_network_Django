# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase05RefreshAuthTokensV1APITestCase.test_case status_code'] = '404'

snapshots['TestCase05RefreshAuthTokensV1APITestCase.test_case body'] = {
    'http_status_code': 404,
    'res_status': 'REFRESH_TOKEN_NOT_FOUND',
    'response': 'Refresh token not found'
}
