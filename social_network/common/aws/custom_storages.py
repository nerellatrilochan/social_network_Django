from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings


class StaticStorage(S3Boto3Storage):
    location = settings.STATICFILES_LOCATION

    def _get_security_token(self):
        # https://github.com/jschneier/django-storages/issues/606
        return None


class MediaStorage(S3Boto3Storage):
    location = settings.MEDIAFILES_LOCATION

    def _normalize_name(self, name):
        """
        Get rid of this crap:
        http://stackoverflow.com/questions/12535123/django-storages-and-amazon-s3-suspiciousoperation
        """
        return name

    def _get_security_token(self):
        # https://github.com/jschneier/django-storages/issues/606
        return None
