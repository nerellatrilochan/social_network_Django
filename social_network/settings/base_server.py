import os


from social_network.settings.base import *
from social_network.settings.base_pg_db import *
from social_network.settings.base_swagger_utils import *
from social_network.settings.base_aws_s3 import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

LOG_DSU_OLD_VERSION_LOGS = False