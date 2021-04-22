#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: lenovo
@file: QuickSort.py
@time: 2021/4/12 18:27
"""
import random
import time

import matplotlib.pyplot as plt


class quickSort:
    """a class to implement quick sort algorithm."""

    def __init__(self, ):
        """Constructor for quickSort"""

    def quick_sort(self, A, p, r):
        def rand_partition(A, p, r):
            i = random.randint(p, r)
            swap(A, i, r)
            x = A[r]
            i = p - 1
            for j in range(p, r):
                if A[j] <= x:
                    i += 1
                    swap(A, i, j)
            swap(A, i + 1, r)
            return i + 1

        def swap(A, i, j):
            A[i], A[j] = A[j], A[i]

        if p < r:
            try:
                # print("p, r: ", p, r)
                q = rand_partition(A, p, r)
                self.quick_sort(A, p, q - 1)
                self.quick_sort(A, q + 1, r)
            except Exception as e:
                print(e)

    def quick_sort_three_way_division(self, A, l, r):
        def rand_partition(A, l, r):
            v = random.randint(l, r)  # pivot
            # v = l
            swap(A, v, r)  # r is index of pivot
            x = A[r]  # value
            # record less_than pivot and grater_than pivot
            # sort [l,r-1]
            lt = l
            gt = r - 1
            i = l
            while i < gt:
                if A[i] < x:  # less than , swap lt , i
                    swap(A, lt, i)
                    lt += 1
                    i += 1
                elif A[i] == x:  # equal to , next i
                    i += 1
                else:  # greater than, swap gt , i
                    swap(A, i, gt)
                    gt -= 1
            swap(A, gt, r)
            return lt, gt

        def swap(A, i, j):
            A[i], A[j] = A[j], A[i]

        if l < r:
            try:
                # print("l, r: ", l, r)
                q = rand_partition(A, l, r)
                lt, gt = q[0], q[1]
                self.quick_sort(A, l, lt)
                self.quick_sort(A, gt + 1, r)
            except Exception as e:
                print(e)


if __name__ == '__main__':
    def generate(count, limit=None):
        if limit == None: limit = count

        nums = random.sample(range(0, count), count - limit)
        nums += [nums[random.randint(0, len(nums) - 1)]] * limit
        return nums


    def write_to_file(list, filepath="a.csv"):
        with open(filepath, "w") as f:
            for i in list:
                f.write(str(i) + "\n")


    def read_from_file(filepath="b.csv"):
        result = []
        for line in open(filepath):
            result.append(float(line))
        return result


    # 结果记录，a 原始排序结果，b 三路排序结果，c 自己电脑三路快排的结果。
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.title('快排结果')
    plt.ylabel('运行时间/s')
    plt.xlabel('重复元素（i% * 100 * n） -> i/num')
    plt.plot(range(1, 10), read_from_file('a.csv'), color='red', label='origin')
    plt.plot(range(1, 10), read_from_file('b.csv'), color='blue', label='three ways')
    plt.legend()
    plt.show()

    Max = 1000000
    # sys.setrecursionlimit(Max)
    qs = quickSort()
    n = 100000
    resultList = []
    for i in range(1, 10):
        repeat = int(n * 10 * 0.01 * i)
        nums = generate(n, repeat)
        start = time.time()
        # print("zhixing ")
        qs.quick_sort(nums, 0, len(nums) - 1)
        # qs.quick_sort_three_way_division(nums, 0, len(nums) - 1)
        end = time.time()
        print(nums)
        timespan = (float)(end - start)
        # print("start: " + str(start) + ", end: "+ str(end) + ", timespan: " +str(timespan))
        resultList.append(timespan)
        print(resultList)

    write_to_file(resultList)

    # write_to_file(resultList, "b.csv")
