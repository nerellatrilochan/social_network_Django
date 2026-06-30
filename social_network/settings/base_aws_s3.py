import os

# ********************** Static Files *************************
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

AWS_HEADERS = {  # see http://developer.yahoo.com/performance/rules.html#expires
    'Expires': 'Thu, 31 Dec 2099 20:00:00 GMT',
    'Cache-Control': 'max-age=94608000',
}

AWS_ACCOUNT_ID = os.environ.get("AWS_ACCOUNT_ID")
AWS_ACCESS_KEY_ID = os.environ.get("CUSTOM_AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("CUSTOM_AWS_SECRET_ACCESS_KEY")

AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME", "ap-south-1")
AWS_CLOUDFRONT_DOMAIN = os.environ.get("AWS_CLOUDFRONT_DOMAIN")
AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_S3_CUSTOM_DOMAIN = os.environ.get('AWS_S3_CUSTOM_DOMAIN', '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME)
AWS_S3_HOST = 's3-ap-south-1.amazonaws.com'

STORAGES = {
    "default": {
        "BACKEND": "social_network.common.aws.custom_storages.MediaStorage",
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "custom_domain": AWS_S3_CUSTOM_DOMAIN,
            "region_name": AWS_S3_REGION_NAME,
        },
    },
    "staticfiles": {  # Add this key for static files
        "BACKEND": "social_network.common.aws.custom_storages.StaticStorage",
        "OPTIONS": {
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "custom_domain": AWS_S3_CUSTOM_DOMAIN,
            "region_name": AWS_S3_REGION_NAME,
        },
    },
}

STATICFILES_LOCATION = '%s/static' % os.environ.get("STAGE")
MEDIAFILES_LOCATION = '%s/media' % os.environ.get("STAGE")

# For uploading all the staticfiles correctly (with public read access)
AWS_S3_OBJECT_PARAMETERS = {
    'ACL': 'public-read',
}

# Only for django-storages
AWS_DEFAULT_ACL = 'public-read'

STATIC_URL = '//%s/%s/' % (AWS_CLOUDFRONT_DOMAIN, STATICFILES_LOCATION)
MEDIA_URL = '//%s/%s/' % (AWS_CLOUDFRONT_DOMAIN, MEDIAFILES_LOCATION)

DEFAULT_CLOUDFRONT_PROTOCOL = os.environ.get(
    "DEFAULT_CLOUDFRONT_PROTOCOL", "https")
