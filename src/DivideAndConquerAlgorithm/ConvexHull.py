#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: lenovo
@file: ConvexHull.py
@time: 2021/4/12 18:26
"""
import random
from math import atan2
import matplotlib.pyplot as plt


class ConvexHull:
    """question convex hull about divide and conquer algorithm."""

    def __init__(self,):
        """Constructor for ConvexHell"""
        self.max = 9999
        self.base_point = (0, 0)

    # 枚举
    def based_enum(self,points:[]):
        '''
        Implement method based on enumerate.
        :param points: [(x,y),]
        :return: points contain vertexes of convex hull
        '''
        n = len(points)
        if n <= 3:
            return points
        base_point = points[0]
        # find the min_x point -> base_point
        for i in range(1, n):
            if base_point[0] > points[i][0]:
                base_point = points[i]
        extra = [base_point]  # extra set store all non_vertex
        # three levels circulation
        for i in range(n - 2):
            point_i = points[i]
            if point_i in extra:
                continue
            for j in range(i + 1, n - 1):
                point_j = points[j]
                if point_j in extra:
                    continue
                for k in range(j + 1, n):
                    point_k = points[k]
                    if point_k in extra:
                        continue
                    if self.isInTriangle(base_point,point_j,point_k,point_i):
                        extra.append(point_i)
                        break
                    if self.isInTriangle(base_point,point_i,point_k,point_j):
                        extra.append(point_j)
                        break
                    if self.isInTriangle(base_point,point_i,point_j,point_k):
                        extra.append(point_k)
                        break
                if point_i in extra:
                    break
        extra.remove(base_point)
        result = []
        for i in points:
            if i not in extra:
                result.append(i)
        # sort by polygon
        print(result)
        result = self.sort_points_polygon(result)
        return result

    def based_divide_conquer(self,points):
        '''
        Implement divide and conquer algorithm
        :param points: [(x,y),]
        :return: points contain vertexes of convex hull
        '''
        n = len(points)
        if n <= 3:
            return points
        # cal median
        min,max= self.max,0
        for i in points:
            if min > i[0]: min = i[0]
            if max < i[0]: max = i[0]
        x_median = (min + max) // 2
        # divide
        left,right = [],[]
        for i in points:
            if i[0] <= x_median: left.append(i)
            else: right.append(i)

        Ql = self.based_divide_conquer(left)
        Qr = self.based_divide_conquer(right)

        # merge
        if len(Qr) > 0:
            Qr_ymax, index = Qr[0], 0
            for i in range(len(Qr)):
                if Qr_ymax < Qr[i]:
                    Qr_ymax, index = Qr[i], i
                else:
                    break
            result = Ql + Qr[:index + 1] + Qr[len(Qr) - 1 :index:-1]
        else:
            result = Ql

        return self.graham_scan(result)

    def graham_scan(self,points:list):
        '''
        Implement graham scan algorithm
        :param points: [(x,y),]
        :return: points contain vertexes of convex hull
        '''
        if len(points) <= 3:
            return points
        # find the base_point of min_y and sort by angle other points to base_point.
        base_y = self.max
        index = 0 # base_point
        for i in range(0, len(points)):
            if base_y > points[i][1]:
                base_y = points[i][1]
                self.base_point = points[i]
                index = i
            if base_y == points[i][1] and self.base_point[0] > points[i][0]:
                self.base_point = points[i]
                index = i
        points[0], points[index] = points[index], points[0]
        print(self.base_point)
        self.quickSortbyAngle(points,1,len(points)-1)
        print("sort :")
        print(points)

        # stack to store vertexes of convex hull
        print("\nprint stack :")
        stack = []
        stack.append(points[0])
        stack.append(points[1])
        stack.append(points[2])
        for i in range(3,len(points)):
            print(stack)
            top = len(stack)-1
            flag = True
            while len(stack) > 2 and flag:
                flag = False
                top_point = stack[top]
                next_top_point = stack[top - 1]
                # non-left move
                if self.is_move_non_left(next_top_point,top_point,points[i]):
                    flag = True
                    del stack[top]
                    top -= 1
            stack.append(points[i])
        return stack

    # 辅助：判断非左移动
    def is_move_non_left(self, p0, p1, p2):
        '''judge non left move'''
        if (p1[0]-p0[0])*(p2[1]-p0[1]) - (p2[0]-p0[0]) * (p1[1]-p0[1]) >= 0:
            return False
        return True

    # 辅助：获取两点与x轴夹角
    def angle(self, p1, p2):
        '''cal pole angle between two points'''
        return atan2(p2[0]-p1[0],p2[1]-p1[1])

    # 辅助：获取两点之间距离
    def distance(self, p1, p2):
        '''cal distance between two points'''
        return (p1[0] - p2[0])*(p1[0] - p2[0]) + (p1[1] - p2[1])*(p1[1] - p2[1])

    # 辅助: 快排，按极角排序所有点
    def quickSortbyAngle(self,points:list,low,high):
        # O(nlogn)
        base = self.base_point
        if low < high:
            i = low - 1
            pivot = self.angle(base,points[high])
            dis = self.distance(base,points[high])

            for j in range(low, high):
                cur_angle = self.angle(base,points[j])
                if cur_angle > pivot:
                    i += 1
                    points[i], points[j] = points[j] ,points[i]
                if cur_angle == pivot and self.distance(base,points[j]) > dis:
                    i += 1
                    points[i], points[j] = points[j], points[i]
            points[i + 1], points[high] = points[high], points[i + 1]

            self.quickSortbyAngle(points,low, i)
            self.quickSortbyAngle(points,i + 2, high)

    # 辅助：向量叉乘
    def vector_x_multify(self,a,b,point_target):
        return (b[0] - a[0]) * (point_target[1] - a[1]) - (b[1] - a[1]) * (point_target[0] - a[0])

    # 辅助：判断target是否在一个三角形abc中
    def isInTriangle(self,a,b,c, point_target):
        # 共线
        # count the sign of Triangle
        signOfTrig = self.vector_x_multify(a,b,c)
        if not signOfTrig: return False
        # count the sign of p with a,b a,c and b,c
        signOfAB = self.vector_x_multify(a,b,point_target)
        if signOfAB * signOfTrig < 0: return False
        signOfCA = self.vector_x_multify(c,a,point_target)
        if signOfCA * signOfTrig < 0: return False
        signOfBC = self.vector_x_multify(b,c,point_target)
        if signOfBC * signOfTrig < 0: return False
        return True

    # 辅助: 按多边形排序顶点
    def sort_points_polygon(self,points):
        up,down = [],[]
        left, right = points[0],points[0]
        for point in points:
            if left[0] > point[0]:
                left = point
            if right[0] < point[0]:
                right = point
        flag = self.vector_x_multify(left,right, (100,0)) # down
        for point in points:
            if self.vector_x_multify(left,right,point) * flag < 0:
                up.append(point)
            if self.vector_x_multify(left,right,point) * flag > 0:
                down.append(point)
        print("before sort :")
        print(up)
        print(down)
        print("after sort :")
        up = sorted(up,key=lambda i: i[0],reverse=True)
        print(up)
        down = sorted(down,key=lambda i: i[0])
        # down.reverse()
        print(down)
        return [left]+down+[right]+up




if __name__ == '__main__':
    def generate_points(n,limit = 100):
        points = []
        for i in range(n):
            a = (random.randint(0, limit),random.randint(0,limit))
            points.append(a)
        return points

    def save(points, filepath = "a.csv"):
        with open(filepath, "w") as f:
            for i in range(len(points)):
                f.write(str(points[i][0]) + ","+ str(points[i][1])+"\n")

    def read(points:[],filepath = "a.csv"):
        for line in open(filepath):
            a = (int(line.split(",")[0]),int(line.split(",")[1]))
            points.append(a)

    def UI(points_total, points_vertex, limit = 100,):
        flt,ax = plt.subplots()
        axle_x, axle_y = [],[]
        for i in points_total :
            axle_x.append(i[0])
            axle_y.append(i[1])
        # total points show
        ax.plot(axle_x,axle_y,'o')
        ax.set_title("convex hull")
        # draw lines
        for i in range(len(points_vertex)):
            if i == len(points_vertex) - 1:
                x = [points_vertex[i][0],points_vertex[0][0]]
                y = [points_vertex[i][1],points_vertex[0][1]]
            else:
                x = [points_vertex[i][0], points_vertex[i + 1][0]]
                y = [points_vertex[i][1], points_vertex[i + 1][1]]
            # print(x,y)
            ax.plot(x, y)
        plt.show()

    def UI_only_points(points_total, points_vertex, limit = 100,):
        flt, ax = plt.subplots()
        axle_x, axle_y = [], []
        for i in points_total:
            axle_x.append(i[0])
            axle_y.append(i[1])
        # total points show
        ax.plot(axle_x, axle_y, 'o')
        ax.set_title("convex hull")
        # draw lines
        axle_x, axle_y = [], []
        for i in points_vertex:
            axle_x.append(i[0])
            axle_y.append(i[1])
        ax.plot(axle_x, axle_y, 'o','r')
        plt.show()

    def test_read_file():
        convex_hull = ConvexHull()
        points = [] # [(x,y),]
        for i in range(1,2):
            points.clear()
            read(points)

            # test graham scan algorithm
            # result = convex_hull.graham_scan(points)
            # UI(points,result)

            # test enumerate algorithm
            # result = convex_hull.based_enum(points)
            # UI_only_points(points, result)
            # UI(points, result)

            # test divide and conquer algorithm
            result = convex_hull.based_divide_conquer(points)
            UI(points,result)

            print(result)
            # save(result, "b.csv")

    def test_random():
        convex_hull = ConvexHull()
        points = []  # [(x,y),]
        base = 100
        for i in range(1, 2):
            n = i * base
            points.clear()
            points = generate_points(n)
            print(points)
            # save(points)

            # test graham scan algorithm
            # result = convex_hull.graham_scan(points)
            # UI(points,result)

            # test enumerate algorithm
            result = convex_hull.based_enum(points)
            UI_only_points(points, result)

            # test divide and conquer algorithm
            # result = convex_hull.based_divide_conquer(points)
            # UI(points,result)

            print(result)
            # save(result, "b.csv")

    # test_random()
    test_read_file()