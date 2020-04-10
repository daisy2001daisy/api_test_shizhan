# -*- coding: utf-8 -*-
# @Time    : 2020/4/9 6:56
# @Author  : Daisy
# @File    : operation_excel.py

import xlrd
import json
from common.public import file_path
from utils.operation_yaml import ReadYaml


# 为books.xlsx文件中的列名定义的类
class ExcelColumName:
    case_id = 0
    description = 1
    url = 2
    method = 3
    data = 4
    expect = 5

    @property
    def get_caseid(self):
        return self.case_id

    @property
    def get_description(self):
        return self.description

    @property
    def get_url(self):
        return self.url

    @property
    def get_method(self):
        return self.method

    @property
    def get_data(self):
        return self.data

    @property
    def get_expect(self):
        return self.expect


# 为文件books_all.xlsx中的列定义的类
class ExcelColumNameAll:
    case_id = '测试用例ID'
    module_name = '模块'
    api_name = '接口名称'
    pre_condition = '前置条件'
    rqst_url = '请求地址'
    rqst_method = '请求方法'
    rqst_param_type = '请求参数类型'
    rqst_param = '请求参数'
    expect_rslt = '期望结果'
    is_run = '是否运行'
    rqst_header = '请求头'
    status_code = '状态码'


class OperationExcel:
    def __init__(self, file_name, file_dir='data'):
        self.file_path = file_path(file_dir, file_name)

    def get_sheet(self):
        wk = xlrd.open_workbook(self.file_path)
        return wk.sheet_by_index(0)

    @property
    def get_colums(self):
        return self.get_sheet().ncols

    @property
    def get_rows(self):
        return self.get_sheet().nrows

    def get_value(self, row, col):
        return self.get_sheet().cell_value(row, col)

    def get_caseid(self, row):
        return self.get_value(row=row, col=ExcelColumName().get_caseid)  # 注意这里的ExcelColumName()要加括号，否则会报错

    def get_url(self, row):
        return self.get_value(row=row, col=ExcelColumName().get_url)

    def get_method(self, row):
        return self.get_value(row=row, col=ExcelColumName().get_method)

    def get_data(self, row):     # 取到excel表中的值
        return self.get_value(row=row, col=ExcelColumName().get_data)

    def get_param(self, row):        # 根据映射关系，再读取到excel映射的book.yaml文件中的值
        return ReadYaml().read_dict_content()[self.get_data(row)]    # 返回的是一个字典类型值

    def get_expect(self, row):
        return self.get_value(row=row, col=ExcelColumName().get_expect)

    def read_excel_data(self):
        '''
        把excel文件中的所有数据，按照字典的类型放在列表中返回
        :return
        '''
        st = self.get_sheet()
        case_lists = list()
        key = st.row_values(0)     # 读取第一行内容，作为字典的key
        for i in range(1, st.nrows):
            value = st.row_values(i)
            case_lists.append(dict(zip(key, value)))
        return case_lists

    def run_list(self):
        '''
        获取到可以运行的测试用例
        :return 返回一个要运行的case的列表
        '''
        run_list = []
        for item in self.read_excel_data():
            is_run = item[ExcelColumNameAll.is_run]
            if is_run == 'y':
                run_list.append(item)
        return run_list

    def exist_pre(self, pre):
        '''
        根据找到前置条件的名称，找到要执行的前置用例
        :pre 前置case的caseID字符串
        :return 一个包含case相关参数的字典
        '''
        for item in self.read_excel_data():
            if item[ExcelColumNameAll.case_id] == pre:
                return item

if __name__ == '__main__':
    # exl = OperationExcel('books.xlsx')
    # print(exl.get_param(2))
    exl = OperationExcel('books_all.xlsx')
    exl.run_list()
