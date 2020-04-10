# _*_ coding: utf-8 _*_
# @Time    : 2020/4/9 19:54
# @Author  : Daisy
# @File    : test_login_books.py

import json
import pytest
from base.method import RequestMethod
from utils.operation_excel import OperationExcel, ExcelColumNameAll
from common.public import write_id_to_file, read_id_from_file

excel = OperationExcel(file_name='books_all.xlsx', file_dir='data')
rqst = RequestMethod()
print(excel.read_excel_data())


def get_dict(data, col_name):
    '''对请求参数/请求头为空进行处理，并把字符串转换成dict类型'''
    param = data[col_name]
    if len(param.strip()) == 0:
        pass
    else:
        return json.loads(param.strip())   # 反序列化，得到字典类型


def get_url(data, book_id):
    """如果要获取某本书籍信息，则需要替换bookID的值；否则获取全部书籍信息"""
    if book_id:
        url = data[ExcelColumNameAll.rqst_url].replace('{bookID}', book_id)
    else:
        url = data[ExcelColumNameAll.rqst_url]
    return url


def assert_result(res, data):
    assert data[ExcelColumNameAll.status_code] == res.status_code
    assert data[ExcelColumNameAll.expect_rslt] in json.dumps(res.json(), ensure_ascii=False)


@pytest.mark.parametrize('data', excel.run_list())
def test_login_book(data):
    # 1. 判断case存不存在前置条件，如果存在，则先执行前置条件
    pre_case = excel.exist_pre(data[ExcelColumNameAll.pre_condition].strip())  # pre_case是一个字典类型
    if pre_case:
        # 在此处，我们知道所有的case最多只有一个前置条件，且只有一个是login，
        # 所以这里直接使用post,如果不确定就要再封装一层
        res = rqst.post(url=pre_case[ExcelColumNameAll.rqst_url],
                        json=get_dict(pre_case, ExcelColumNameAll.rqst_param))
        access_token = res.json()['access_token']
        # print(access_token)

    if len(data[ExcelColumNameAll.rqst_header].strip()) == 0:
        headers = None
    else:
        headers = json.loads(data[ExcelColumNameAll.rqst_header].replace('{token}', access_token))

    # 判断是获取全部书籍信息，还是获取某一本书籍的信息
    book_id = None
    if '{bookID}' in data[ExcelColumNameAll.rqst_url]:
        book_id = read_id_from_file()

    # 2. 根据method不同，使用不同的请求方法发送请求
    if data[ExcelColumNameAll.rqst_method] == 'get':
        res = rqst.get(url=get_url(data, book_id), headers=headers)
    elif data[ExcelColumNameAll.rqst_method] == 'post':
        res = rqst.post(url=data[ExcelColumNameAll.rqst_url],
                        json=get_dict(data, ExcelColumNameAll.rqst_param),
                        headers=headers)
        # 添加书籍成功后，需要存储书籍的bookID，后面的case可能会用到
        if 'id' in res.text:
            write_id_to_file(res.json()[0]['datas']['id'])
    elif data[ExcelColumNameAll.rqst_method] == 'put':
        res = rqst.put(url=get_url(data, book_id),
                       json=get_dict(data, ExcelColumNameAll.rqst_param),
                       headers=headers)
    elif data[ExcelColumNameAll.rqst_method] == 'delete':
        res = rqst.delete(url=get_url(data, book_id), headers=headers)
    # print(res.json())

    # 3. 对返回信息进行断言
    assert_result(res, data)


if __name__ == '__main__':
    pytest.main(["-v", "test_login_books.py", "--alluredir", ".//report//result"])
    import subprocess
    subprocess.call("allure generate report/result/ -o report/html --clean", shell=True)
    subprocess.call("allure open -h 127.0.0.1 -p 8088 ./report/html", shell=True)
