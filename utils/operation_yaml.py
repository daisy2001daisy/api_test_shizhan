# -*- coding: utf-8 -*-
# @Time    : 2020/4/8 17:25
# @Author  : Daisy
# @File    : operation_yaml.py

import yaml
from common.public import file_path


class ReadYaml:
    def read_list_content(self, file_name, file_dir):
        with open(file_path(file_dir, file_name), 'r', encoding='utf-8') as f:    # login.yaml文件中有中文，那么这里必须要加上encoding='utf-8'
            return list(yaml.safe_load_all(f))    # safe_load_all(f)得到的是一个生成器，所以要转换成一个列表
                                                  # 每一个元素都是字典类型的

    # safe_load()只能在样本文件中只有一个值时(即没有---时)，才可以用，得到的是字典类型的
    def read_dict_content(self, file_name='book.yaml', file_dir='config'):
        with open(file_path(file_dir, file_name), 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)


if __name__ == '__main__':
    print(ReadYaml().read_dict_content())
