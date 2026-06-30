# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase03LoginWithCodeAPITestCase.test_case status_code'] = '403'

snapshots['TestCase03LoginWithCodeAPITestCase.test_case body'] = {
    'http_status_code': 403,
    'res_status': 'USER_ACCOUNT_IS_DEACTIVATED',
    'response': 'User Account is deactivated. Please contact support.'
}
