# -*- coding: utf-8 -*-
# snapshottest: v1 - https://goo.gl/zC4yUc
from __future__ import unicode_literals

from snapshottest import Snapshot


snapshots = Snapshot()

snapshots['TestCase03GetUserProfileAPITestCase.test_case status_code'] = '200'

snapshots['TestCase03GetUserProfileAPITestCase.test_case body'] = {
    'accepted_tnc': True,
    'age': 20,
    'age_group': 'age_group1',
    'country_code': '91',
    'cover_page_url': 'name_1',
    'dob': '2020-12-28',
    'email': 'my_email_1',
    'gender': 'MALE',
    'i_want_to_receive_updates_directly_on_whatsapp': 'yes',
    'is_email_verified': False,
    'is_phone_number_verified': False,
    'language_preference': 'ENGLISH',
    'last_name': 'last_name_1',
    'name': 'name_1',
    'occupation': 'occupation_1',
    'phone_number': '98765431',
    'pincode': '534313',
    'profile_pic_url': 'my_profile_1',
    'state_of_residence': 'my_profile_1',
    'user_id': 'user_1'
}
