#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: lenovo
@file: File.py
@time: 2021/4/12 13:20
"""

def write_to_file(filename,content):
    with open(filename, 'a') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
        for i in range(0,len(content)):
            f.write(content[i])
            f.write("\n")