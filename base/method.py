# -*- coding: utf-8 -*-
# @Time    : 2020/4/8 7:45
# @Author  : Daisy
# @File    : method.py

import requests


class RequestMethod:
    def request(self, url, method='get', **kwargs):
        return requests.request(url=url, method=method, **kwargs)

    def get(self, url, **kwargs):
        return self.request(url=url, **kwargs)

    def post(self, url, **kwargs):
        return self.request(url=url, method='post', **kwargs)

    def put(self, url, **kwargs):
        return self.request(url=url, method='put', **kwargs)

    def delete(self, url, **kwargs):
        return self.request(url=url, method='delete', **kwargs)

