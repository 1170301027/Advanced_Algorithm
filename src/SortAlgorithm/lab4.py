# coding=utf-8
import random 
import time
import sys
import threading
from threading import Thread 
#import matplotlib.pyplot as plt  

res1, res2 = [], []
class QuickSort():

    def insertSort(self, nums, left, right):
        for j in range(0, right - left + 1):
            for i in range(j, 0, -1):
                if nums[i] < nums[i - 1]:
                    nums[i], nums[i - 1] = nums[i - 1], nums[i]
                else:
                    break
        return

    def quickSort(self, nums, left, right):

        if left < right:
            #返回定位位置
            index = self.randomPartition(nums, left, right)
            low = index
            #从[low, index]元素都相等
            while low >= index and nums[low] == nums[index]:
                low -= 1
            self.quickSort(nums, left, low)
            self.quickSort(nums, index + 1, right)
    
    def randomPartition(self, nums, left, right):
        #随机定位一个基准数
        index = random.randint(left, right)
        nums[index], nums[right] = nums[right], nums[index]
        tmp = nums[right]
        index = left - 1
        for j in range(left, right):
            if nums[j] <=  tmp:
                index += 1
                nums[index], nums[j] = nums[j], nums[index]
        index += 1
        nums[index], nums[right] = nums[right], nums[index]
        return index

    #三路归并，将重复元素聚集到一起
    def quickSortPro(self, nums, left, right):
        if left >= right:
            return
        tmp = nums[left]
        i, j, k = left, right, left + 1
        while k <= j:
            if nums[k] < tmp:
                nums[k], nums[i] = nums[i], nums[k]
                i += 1
                k += 1
            elif nums[k] > tmp:
                nums[k], nums[j] = nums[j], nums[k]
                j -= 1
            else:
                k += 1
        self.quickSortPro(nums, left, i-1)
        self.quickSortPro(nums, j+1, right) 

class Test:
    def simpleTest(self):
        #生成10个随机小样本测试，小样本集大小在0-100之间，样本集中的数字范围在-1000到1000
        for i in range(10):
            length = random.randint(0,100)
            data = [random.randint(-1000, 1000) for j in range(length)]
            print("Before sort: ", data)
            s = QuickSort()
            s.quickSortPro(data,0,len(data)-1)
            print("After sort: ", data)
    
    def test(self, size, rate):
        #rate的取值从0, 0.1, 0.2, 到1
        length = int( size * rate /10)
        print(length)
        #先随机生成一个数，在data里重复length次
        tmp = random.randint(0, 1000000)
        data = [tmp]*length
        for i in range(size-length):
            num = random.randint(0, 1000000)
            if num != tmp:
                data.append(num)
            else:
                i-=1
        #打乱数组
        random.shuffle(data)

        copy_data = data[:]
        #print("随机生成的数据: ", data)
        s = QuickSort()
        time1 = time.time()
        s.quickSort(data,0,len(data)-1)
        time2 = time.time()
        res1.append((time2 - time1)*1000)

        time1 = time.time()
        #s.quickSortPro(copy_data,0, len(copy_data)-1)
        time2 = time.time()
        res2.append((time2 - time1)*1000)
        print(res1, res2)
        #print("排序后的数据: ", data)
'''
def draw():
    x = [0,1,2,3,4,5,6,7,8,9,10]
    y1 = [111.09495162963867, 7516.344785690308, 30641.21913909912, 67350.28600692749, 119142.25220680237, 190336.45391464233, 276526.93796157837, 389595.5948829651, 503566.6780471802, 606724.0269184113, 758451.5299797058] 
    y2 = 402.02903747558594, 348.88696670532227, 300.3721237182617, 270.6429958343506, 221.89593315124512, 189.37015533447266, 154.1748046875, 125.46205520629883, 76.95698738098145, 41.3057804107666, 10.420083999633789]
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.title('结果')
    plt.xlabel("数据量/个") #xlabel、ylabel：分别设置X、Y轴的标题文字。
    plt.ylabel("算法运行时间/ms")
    
    plt.plot(x, y1,  color='red', label='快排')
    plt.plot(x, y2,  color='blue', label='改进后')
    plt.legend() 
    plt.show()
'''

def main():
    t = Test()
    #t.simpleTest()

    for i in range(0,11):
       t.test(100000,i)
    print(res1, res2)

if __name__ == "__main__":
    #draw()
    sys.setrecursionlimit(2097152)    # adjust numbers
    threading.stack_size(134217728)   # for your needs

    main_thread = threading.Thread(target=main)
    main_thread.start()
    main_thread.join()        