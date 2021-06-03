from __future__ import unicode_literals

import logging
import json


# 用户操作请求日志打印记录，用于Hadoop离线分析日志，可自定义日志信息
class ApiLoggingMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        self.apiLogger = logging.getLogger('api')

    def __call__(self, request):
        try:
            body = json.loads(request.body)
        except Exception as ex:
            body = dict()
        try:
            get_str = dict(request.GET)
        except Exception as ex:
            get_str = dict()
        body.update(dict(request.POST))
        response = self.get_response(request)
        # if request.method != 'GET':
        # if request.method == 'GET' or request.method == 'POST':
        if not request.path.startswith("/static/") and request.path != "/favicon.ico":
            self.apiLogger.info("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(
                request.COOKIES.get("uuid"), request.method, request.path, get_str, body,
                response.status_code, response.reason_phrase))
        return response
