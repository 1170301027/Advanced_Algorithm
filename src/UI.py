
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: lenovo
@file: UI.py
@time: 2021/4/14 10:54
"""

import matplotlib.pyplot as plt

import numpy as np

fig,ax=plt.subplots() #建立对象

ax.plot(10*np.random.randn(100),10*np.random.randn(100),'o')#设置对象

ax.set_title("simple scatter")

plt.show()