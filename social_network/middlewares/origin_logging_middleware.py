# ruff: noqa: SIM102, G002
# pylint: disable=C0411,W1201,R1702

import re

from django.conf import settings

import logging
logger = logging.getLogger('dsu.debug')


class OriginLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            if not settings.CORS_ORIGIN_ALLOW_ALL:
                origin = request.META.get('HTTP_ORIGIN')
                if origin and origin != 'null':
                    if settings.CORS_ORIGIN_REGEX_WHITELIST:
                        is_atleast_one_regex_matched = False
                        for cors_allowed_regex_origin in \
                                settings.CORS_ORIGIN_REGEX_WHITELIST:
                            if re.match(cors_allowed_regex_origin, origin):
                                is_atleast_one_regex_matched = True
                                break
                        if not is_atleast_one_regex_matched:
                            logger.warning('Unauthorized origin: %s' % origin)
        except Exception as e:
            logger.warning(e)

        response = self.get_response(request)
        return response
