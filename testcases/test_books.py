# _*_ coding: utf-8 _*_
# @Time    : 2020/4/9 7:10
# @Author  : Daisy
# @File    : test_books.py

import json
import pytest
from base.method import RequestMethod
from utils.operation_excel import OperationExcel
from common.public import write_id_to_file, read_id_from_file


class TestBooks:
    rqst = RequestMethod()
    excel = OperationExcel('books.xlsx')

    def assert_result(self, res, row):
        assert res.status_code == 200
        # 如果返回结果里有中文，那么就要的序列化的时候，注意参数ensure_ascii=False，否则可能断言错误
        # 下面的assert xxx in xxx, in的前面和后面都是str类型
        assert self.excel.get_expect(row=row) in json.dumps(res.json(), ensure_ascii=False)  # res.text的类型是str；res.json()的类型是dict

    # ###########################测试用例组织方式1：所有case都在一个函数中运行###########################
    # 只根据excel中行数的不同，进行数据的循环即可
    def test_books(self):
        for i in range(1, self.excel.get_rows):
            if self.excel.get_method(i) == 'get':
                if '{bookID}' in self.excel.get_url(i):
                    res = self.rqst.get(url=self.excel.get_url(i).replace('{bookID}', read_id_from_file()))
                else:
                    res = self.rqst.get(self.excel.get_url(i))
            elif self.excel.get_method(i) == 'post':
                res = self.rqst.post(url=self.excel.get_url(i), json=self.excel.get_param(i))
                write_id_to_file(res.json()[0]['datas']['id'])
            elif self.excel.get_method(i) == 'put':
                res = self.rqst.put(url=self.excel.get_url(i).replace('{bookID}', read_id_from_file()),
                              json=self.excel.get_param(i))
            else:
                res = self.rqst.delete(url=self.excel.get_url(i).replace('{bookID}', read_id_from_file()))
            print()
            print(res.json())
            print()
            self.assert_result(res, i)

    ############################测试用例组织方式2：一个case是一个函数，依次运行###########################
    def test_books_001(self):
        # print(self.file_obj.get_method(1), self.file_obj.get_url(1))
        res = self.rqst.get(url=self.excel.get_url(1))
        self.assert_result(res, row=1)

    def test_books_002(self):
        res = self.rqst.post(url=self.excel.get_url(row=2), json=self.excel.get_param(row=2))
        # print(res.json())
        self.assert_result(res, row=2)
        write_id_to_file(res.json()[0]['datas']['id'])

    def test_books_003(self):
        book_id = read_id_from_file()
        # print(self.excel.get_url(row=3).replace('{bookID}', book_id))
        res = self.rqst.get(url=self.excel.get_url(row=3).replace('{bookID}', book_id))
        # print(res.json())
        self.assert_result(res, row=3)

    def test_book_004(self):
        # print(self.excel.get_url(row=4).replace('{bookID}', read_id_from_file()))
        # print(self.excel.get_param(row=4))
        res = self.rqst.put(url=self.excel.get_url(row=4).replace('{bookID}', read_id_from_file()),
                            json=self.excel.get_param(row=4))
        # print(res.json())
        self.assert_result(res, row=4)

    def test_book_005(self):
        res = self.rqst.delete(url=self.excel.get_url(row=5).replace('{bookID}', read_id_from_file()))
        # print(res.json())
        self.assert_result(res, row=5)

    def test_books_006(self):
        res = self.rqst.get(url=self.excel.get_url(1))
        print(res.json())
        self.assert_result(res, row=1)
    ######################################测试用例组织方式2####################################


if __name__ == '__main__':
    pytest.main(['-s', '-v', 'test_books.py::TestBooks::test_books()'])
