# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase01LoginWithCodeAPITestCase.test_case status_code'] = '403'

snapshots['TestCase01LoginWithCodeAPITestCase.test_case body'] = {
    'http_status_code': 403,
    'res_status': 'INVALID_CREDENTIALS',
    'response': 'Invalid Credentials. Please enter valid credentials or contact support.'
}
