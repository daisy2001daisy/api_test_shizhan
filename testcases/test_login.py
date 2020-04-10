# -*- coding: utf-8 -*-
# @Time    : 2020/4/8 18:23
# @Author  : Daisy
# @File    : test_login.py

import pytest
import json
from base.method import RequestMethod
from utils.operation_yaml import ReadYaml


class TestLogin():
    rqst = RequestMethod()

    @pytest.mark.parametrize('param', ReadYaml().read_list_content())  # 第1个参数注意：修饰下面参数，要加''引号
    def test_login(self, param):
        # print(param)
        if param['method'] == 'get':
            rsps = self.rqst.get(param['url'])
        elif param['method'] == 'post':
            rsps = self.rqst.post(param['url'], json=param['data'])
            assert param['expect'] in json.dumps(rsps.json(), ensure_ascii=False)    # expect: wuya，这时返回的是str类型的
                                                                                     # expect: {"username": "wuya"}，这样返回的是dict类型的
        # print(type(param['expect']))
        # print(json.dumps(rsps.json(), ensure_ascii=False))


if __name__ == '__main__':
    if __name__ == '__main__':
        pytest.main(['-s', '-v', 'test_login.py'])     # -s表示调试输出打印信息
