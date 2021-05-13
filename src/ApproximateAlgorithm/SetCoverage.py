#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: lenovo
@file: SetCoverage.py
@time: 2021/4/26 13:24
"""

import pulp
import random
import time
import matplotlib.pyplot as plt

'''
集合覆盖问题：
• 输入: 有限集 X, X 的子集合族 F, X=∪𝑆∈𝐹 S
• 输出: C⊆F, 满足
（1）X=∪𝑆∈𝐶 S
（2）C 是满足条件(1)的最小集族, 即|C|最小.
'''
# 生成实验数据
class generate():
    def __init__(self):
        self.X = [] # 有限集
        self.F = [] # 子集合族

    def generateData(self, size):
        X = set(list(range(size))) # 0~n-1
        self.X = X
        S = [random.randint(0, size - 1) for i in range(20)] # 随机选X中的 20 个点放入S0
        S = set(S)
        self.F.append(list(S))
        # union_s表示∪Sj,rest表示X-union_s
        union_s = S
        rest = X - union_s
        while len(rest) >= 20:
            n = random.randint(1, 20)
            x = random.randint(1, n)

            S = set(random.sample(rest, x))
            S.update(random.sample(union_s, n - x))
            union_s.update(S)  # 更新已经被选择的数据集合
            rest = X - union_s
            self.F.append(list(S))

        # 小于20时直接加入
        if len(rest) > 0:
            self.F.append(list(rest))
        # 生成|F|-y个随机集合
        y = len(self.F)
        for i in range(size - y):
            n = random.randint(1, 20)
            S = random.sample(X, n)
            self.F.append(list(S))
        for i in range(len(self.F)):
            self.F[i] = set(self.F[i])

class set_coverage:
    """Set coverage"""

    def __init__(self,):
        """Constructor for set_coverage"""

    def greedy(self, X, F) -> list:
        print(F)
        U = set(X)
        C = []
        while U:
            # 贪心策略:每次选择覆盖U中元素最多的集合加入到C中，
            S = max(F,key=(lambda x:len(U.intersection(x))))
            U -= S
            C.append(S)
        return C

    def liner_programming(self, X:list, F) -> list:
        # 加权集合覆盖：舍入
        # xs = {0,1}

        X = list(X)
        A = [] # 系数矩阵
        for i in range(len(X)):
            row = []
            for j in range(len(F)):
                if X[i] in F[j]:
                    row.append(1)
                else:
                    row.append(0)
            A.append(row)
        f = max([sum(r) for r in A]) # 统计X的元素在F中的最大频率
        t = 1 / f

        # 构建线性方程
        prob = pulp.LpProblem("Linear minimize problem", pulp.LpMinimize)
        ingredient_vars = pulp.LpVariable.dicts("Ingr", X, 0, 1)

        prob += pulp.lpSum([1 * ingredient_vars[i] for i in X])
        for i in range(len(X)):
            prob += pulp.lpSum([A[i][j] * ingredient_vars[j] for j in range(len(F))]) >= 1
        prob.solve()

        prob = prob.variables()
        # 按照目标方程排序
        prob = sorted(prob, key=lambda x: int(x.name[5:]))
        # 按照阈值进行舍入
        C = [set(f) for i, f in enumerate(F) if prob[i].varValue > t]
        return C


if __name__ == "__main__":

    time_lp = []
    time_greedy = []

    def write(time1:list, time2:list, filename='a.csv'):
        with open(filename, "w+") as f:
            for i in range(len(time1)):
                f.write(str(time1[i]) + ',' + str(time2[i]) + "\n")

    def read(time1, time2, filename='a.csv'):
        for line in open(filename,"r"):
            time1.append(float(line.split(",")[0]))
            time2.append(float(line.split(",")[1]))

    def draw(x,time1, time2):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.title('结果')
        plt.xlabel("数据量/个")  # xlabel、ylabel：分别设置X、Y轴的标题文字。
        plt.ylabel("算法运行时间/ms")

        plt.plot(x, time1, color='red', label='线性规划')
        plt.plot(x, time2, color='blue', label='贪心')
        plt.legend()
        plt.show()


    datasize = [100, 1000, 5000]
    # 读文件
    read(time_lp, time_greedy)
    draw(datasize, time_lp, time_greedy)
    time_lp.clear()
    time_greedy.clear()
    for i in datasize:
        g = generate()
        g.generateData(i)
        s = set_coverage()
        time1 = time.time()
        s.liner_programming(g.X, g.F)
        time2 = time.time()
        time_lp.append((time2 - time1)*1000)
        print("线性规划："+str(time_lp[-1]))

        time1 = time.time()
        s.greedy(g.X, g.F)
        time2 = time.time()
        time_greedy.append((time2 - time1) * 1000)
        print("贪心："+str(time_greedy[-1]))

    print(time_lp)
    print(time_greedy)

    write(time_lp, time_greedy)
    draw(datasize,time_lp, time_greedy)
    # print (s.LP(g.rawData, g.data))