# -*- coding: utf-8 -*-
# @Time    : 2020/4/8 17:16
# @Author  : Daisy
# @File    : public.py

import os

base_url = os.path.dirname(os.path.dirname(__file__))
# print(base_url)   # 得到当前框架的根目录


def file_path(file_dir, file_name):
    return os.path.join(base_url, file_dir, file_name)


def write_id_to_file(content):
    file_paths = os.path.join(base_url, 'data', 'bookID.txt')
    with open(file_paths, 'w') as f:
        f.write(str(content))


def read_id_from_file():
    with open(os.path.join(base_url, 'data', 'bookID.txt'), 'r') as f:
        return f.read()



# print(file_path('data', 'login.yaml'))
