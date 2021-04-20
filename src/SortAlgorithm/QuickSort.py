import random
import sys
import time


# import matplotlib.pyplot as plt

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

    def quicksort(self, array, left, right):
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
        # qs.quick_sort(nums,0,len(nums) - 1)
        qs.quick_sort_three_way_division(nums, 0, len(nums) - 1)
        end = time.time()
        print(nums)
        timespan = (float)(end - start)
        # print("start: " + str(start) + ", end: "+ str(end) + ", timespan: " +str(timespan))
        resultList.append(timespan)
        print(resultList)
    # write_to_file(resultList)
    write_to_file(resultList, "b.csv")
