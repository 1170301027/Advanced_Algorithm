import random
import sys
import time

import numpy as np


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
            A[i],A[j] = A[j],A[i]

        if p < r:
            q = rand_partition(A, p, r)
            self.quick_sort(A, p, q - 1)
            self.quick_sort(A, q + 1, r)

    def quicksort(self,array, left, right):
        if left >= right:
            return
        low = left
        high = right
        key = array[low]
        while left < right:
            while left < right and array[right] > key:
                right -= 1
            array[left] = array[right]
            while left < right and array[left] <= key:
                left += 1
            array[right] = array[left]
        array[right] = key
        self.quicksort(array, low, left - 1)
        self.quicksort(array, left + 1, high)


if __name__ == '__main__':
    def generate(count,limit = None):
        nums = []
        if limit == None: limit = count

        nums = random.sample(range(0, count), count - limit + 1)
        nums += [nums[random.randint(0, len(nums) - 1)]] * limit
        return nums

    def write_to_file(list,filepath = "a.csv"):
        with open(filepath,"w") as f:
            f.write(str(i[0]) + "," + str(i[1]) for i in list)


    Max = 1000000
    sys.setrecursionlimit(Max)
    qs = quickSort()
    n = 100000
    resultList=[]
    for i in range(1,12):
        repeat = int(n*10*0.01*i)
        nums = generate(n,repeat)
        start = time.time()
        print("zhixing ")
        qs.quick_sort(nums,0,len(nums) - 1)
        end = time.time()
        print(nums)
        timespan = end - start
        print("start: " + str(start) + ", end: "+ str(end) + ", timespan: " +str(timespan))
        resultList.append((i,timespan))
    write_to_file(resultList)