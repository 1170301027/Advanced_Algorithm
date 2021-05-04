#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: lenovo
@file: A_star.py
@time: 2021/4/12 18:26
"""
from math import sqrt

from tkinter import *

tk = Tk()


class Point:
    def __init__(self, father, cur, g, h):
        """
        point information
        :param father: 父节点
        :param cur: (cur_x,cur_y)
        :param g: 从起始到n的实际代价
        :param h: 从n到目标节点的预估代价
        :param f: 实际代价
        """
        self.father = father  # 根据父节点找路径
        self.cur = cur  # current_position [x,y]
        self.g = g
        self.h = h
        self.f = self.g+self.h

    def __str__(self) -> str:
        if not self.father and not self.cur:
            return "cur:" + str(self.cur) + ",father:(" + str(self.father.cur[0]) + "," + str(self.father.cur[1]) + ") ,f:" + str(self.f) + ",h:" + str(self.h)

class Astar:
    def __init__(self, points):
        self.points = points  # 地图

    def cal_h(self, point_1, point_2):
        # 计算预估代价，启发函数 哈夫曼距离
        return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1])

    def next_step(self, cur_pos, target, open, close):
        # 获取当前坐标
        g = cur_pos.g
        cur = cur_pos.cur
        for i in range(max(cur[0] - 1, 0), min(len(self.points), cur[0] + 2)):  # 计算可走点坐标，点周围的八个坐标
            for j in range(max(cur[1] - 1, 0), min(len(self.points[0]), cur[1] + 2)):
                # 原节点不扩展
                if i == cur[0] and j == cur[1]:
                    continue
                # 遇到障碍物不可扩展 gray
                if self.points[i][j] == "g":
                    continue
                if (i, j) in close:
                    continue
                newg = g
                # 计算已经经过的代价
                # 对角线 v2
                if abs(i - cur[0]) == 1 and abs(j - cur[1]) == 1:
                    newg += sqrt(2)
                else:
                    newg += 1
                # 沙漠 yellow
                if self.points[i][j] == "y":
                    newg += 4
                # 河流 blue
                elif self.points[i][j] == "b":
                    newg += 2

                next_point = Point(cur_pos, (i, j), newg, self.cal_h(target, [i, j]))
                descend = open.get((i, j))  # 获取当前节点的后继节点
                if not descend:  # 若空，则设置为该遍历节点
                    open[(i, j)] = next_point
                elif descend.g > next_point.g:  # 若非空，则比较遍历节点与后继节点的实际代价
                    open.pop((i, j))
                    open[(i, j)] = next_point

    def selectBest(self, open, close):
        res, min_f = None, float('inf')  # infinity
        for point, info in open.items():
            if info.f < min_f:
                res, min_f = point, info.f
        close.add(res)
        return open.pop(res)

    def equalTo(self, cur, target):  # [x,y]
        if cur[0] == target[0] and cur[1] == target[1]:
            return True
        return False

    def one_way(self, start, target):
        open = {}  # 存储 {(x,y):Point(next_x,next_y)}
        open[(start[0], start[1])] = Point(None, start, 0, self.cal_h(target, start))
        close = set()
        while True:
            cur_point = self.selectBest(open, close)
            print(cur_point.cur)
            # 判断是否为目标节点
            if self.equalTo(cur_point.cur, target):
                path = []
                print(cur_point.g,cur_point.h,cur_point.f)
                # 回溯路径, 倒叙输出的
                while cur_point:
                    path.append((cur_point.cur[0], cur_point.cur[1]))
                    cur_point = cur_point.father
                # print(close)
                return path
            # 寻找下一个扩展节点
            self.next_step(cur_point, target, open, close)

    def two_way(self, start, target):

        def find(start_open, target_open):  # 判断是否找到双向的交点
            for key in start_open.keys():
                if key in target_open:
                    startCur, endCur = start_open[key], target_open[key]
                    return startCur, endCur
            return None, None

        start_open = {}
        start_open[(start[0], start[1])] = Point(None, start, 0, self.cal_h(start, target))
        start_close = set()

        target_open = {}
        target_open[(target[0], target[1])] = Point(None, target, 0, self.cal_h(start, target))
        target_close = set()

        while True:
            # start 出发
            cur_start = self.selectBest(start_open, start_close)
            cur1, cur2 = find(start_open, target_open)
            if cur1 and cur2:
                break
            self.next_step(cur_start, target, start_open, start_close)
            # target 出发
            cur_target = self.selectBest(target_open, target_close)
            print(cur_target.cur)
            cur1, cur2 = find(target_open, start_open)
            if cur1 and cur2:
                break
            self.next_step(cur_target, start, target_open, target_close)
        # 回溯路径, 倒叙输出的
        if cur1:print(cur1.g,cur1.h,cur1.f)
        if cur2: print(cur2.g, cur2.h, cur2.f)
        path1 = []
        while cur1:
            path1.append([cur1.cur[0], cur1.cur[1]])
            cur1 = cur1.father
        path2 = []
        while cur2:
            path2.append([cur2.cur[0], cur2.cur[1]])
            cur2 = cur2.father
        return path1, path2


if __name__ == "__main__":
    # 让res1和res2分别表示从start, target出发的路径，既可以画单向的，又可以画双向的
    def draw(points, res1, res2, width, height):
        # 进行初始着色
        for i in range(len(points)):
            for j in range(len(points[0])):
                if points[i][j] == "g":
                    Button(tk, bg="gray", width=width, height=height).grid(row=i, column=j, sticky=W + E + N + S)
                elif points[i][j] == "y":
                    Button(tk, bg="yellow", width=width, height=height).grid(row=i, column=j, sticky=W + E + N + S)
                elif points[i][j] == "b":
                    Button(tk, bg="blue", width=width, height=height).grid(row=i, column=j, sticky=W + E + N + S)
                else:
                    Button(tk, bg="white", width=width, height=height).grid(row=i, column=j, sticky=W + E + N + S)
        # 对以start为起点的路径进行着色
        for i in range(len(res1)):
            if i == len(res1) - 1:
                Button(tk, bg="Violet", width=width, height=height, text="Start").grid(row=res1[i][0],column=res1[i][1],
                                                                                       sticky=W + E + N + S)
            else:
                Button(tk, bg="Violet", width=width, height=height).grid(row=res1[i][0], column=res1[i][1],
                                                                         sticky=W + E + N + S)
        # 单向判断
        if len(res2) == 0:
            Button(tk, bg="Violet", width=width, height=height, text="Target").grid(row=res1[0][0], column=res1[0][1],
                                                                                    sticky=W + E + N + S)
            return
        for i in range(len(res2)):
            if i == len(res2) - 1:
                # print(res2[i][0], res2[i][1])
                Button(tk, bg="Green", width=width, height=height, text="Target").grid(row=res2[i][0],column=res2[i][1],
                                                                                       sticky=W + E + N + S)
            else:
                Button(tk, bg="Green", width=width, height=height).grid(row=res2[i][0], column=res2[i][1],
                                                                        sticky=W + E + N + S)


    # y代表yellow沙漠，b代表blue溪流，g代表gray灰色障碍物，w代表white普通格子
    problem1 = [["w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w"],
                ["w", "w", "w", "g", "w", "w", "w", "w", "w", "w", "w", "w"],
                ["w", "w", "w", "g", "w", "w", "w", "w", "w", "w", "w", "w"],
                ["w", "w", "w", "w", "g", "w", "w", "w", "w", "w", "w", "w"],
                ["w", "w", "w", "w", "g", "w", "w", "w", "w", "w", "w", "w"],
                ["w", "w", "w", "w", "g", "g", "w", "w", "w", "w", "w", "w"],
                ["w", "w", "w", "w", "w", "g", "w", "w", "w", "w", "w", "w"],
                ["w", "w", "w", "w", "w", "g", "w", "w", "w", "w", "w", "w"],
                ["w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w"]]

    problem2 = [
        ["w", "w", "w", "g", "w", "w", "w", "g", "w", "w", "w", "w", "g", "w", "w", "w", "w", "w", "w", "w", "w", "w",
         "w", "w", "y", "y", "y", "y", "y", "y", "y", "y", "y", "y", "y", "y", "y", "y", "y", "y"],
        ["w", "w", "w", "w", "w", "w", "w", "g", "w", "w", "w", "w", "g", "w", "w", "w", "w", "w", "w", "w", "w", "w",
         "w", "w", "w", "y", "y", "y", "y", "y", "y", "y", "y", "y", "b", "y", "y", "y", "y", "y"],
        ["g", "g", "g", "g", "g", "g", "w", "g", "g", "g", "g", "w", "g", "w", "w", "w", "w", "w", "w", "w", "w", "w",
         "w", "w", "w", "w", "y", "y", "y", "y", "y", "y", "y", "b", "y", "y", "y", "y", "y", "y"],
        ["w", "w", "w", "w", "w", "w", "w", "w", "g", "w", "w", "w", "g", "w", "w", "w", "w", "w", "w", "w", "w", "w",
         "w", "w", "w", "w", "y", "y", "y", "y", "y", "y", "b", "y", "y", "y", "y", "w", "w", "w"],
        ["w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "g", "w", "w", "w", "w", "w", "w", "w", "w", "w",
         "w", "w", "w", "w", "y", "y", "y", "y", "y", "y", "y", "b", "y", "y", "w", "w", "w", "w"],
        ["w", "w", "w", "w", "w", "w", "w", "g", "g", "w", "w", "w", "g", "w", "w", "w", "w", "w", "w", "w", "w", "w",
         "w", "w", "w", "w", "w", "y", "y", "y", "y", "y", "y", "b", "b", "w", "w", "w", "w", "w"],
        ["w", "w", "g", "g", "g", "g", "g", "g", "w", "w", "w", "w", "g", "w", "w", "w", "w", "w", "w", "w", "w", "w",
         "w", "w", "w", "w", "w", "y", "y", "y", "y", "y", "y", "b", "b", "w", "w", "w", "w", "w"],
        ["w", "w", "g", "w", "w", "g", "w", "g", "w", "w", "w", "w", "g", "w", "w", "w", "w", "w", "w", "w", "w", "w",
         "w", "w", "w", "w", "w", "w", "w", "y", "y", "y", "y", "b", "b", "b", "g", "w", "w", "w"],
        ["w", "w", "w", "w", "w", "g", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w",
         "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "b", "b", "b", "b", "w", "w", "w", "w"],
        ["w", "w", "w", "w", "w", "g", "w", "g", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w",
         "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "b", "b", "b", "w", "g", "w", "w", "w"],
        ["w", "w", "g", "w", "w", "g", "w", "g", "g", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "g", "g", "g",
         "w", "w", "w", "w", "w", "w", "g", "w", "w", "w", "b", "b", "w", "b", "b", "w", "w", "w"],
        ["w", "w", "g", "g", "g", "g", "w", "w", "g", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "g", "g", "g",
         "w", "w", "w", "w", "w", "w", "w", "w", "w", "g", "b", "w", "b", "b", "w", "w", "w", "w"],
        ["w", "w", "w", "g", "w", "w", "w", "w", "g", "w", "w", "w", "g", "w", "w", "w", "w", "w", "w", "g", "g", "g",
         "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "b", "b", "w", "w", "w", "w", "w"],
        ["w", "w", "w", "g", "w", "w", "w", "w", "g", "g", "w", "g", "g", "w", "w", "w", "w", "w", "w", "w", "w", "w",
         "w", "w", "w", "w", "w", "w", "w", "w", "w", "g", "b", "b", "b", "w", "w", "w", "w", "w"],
        ["w", "w", "w", "g", "w", "w", "w", "w", "g", "w", "w", "w", "g", "w", "w", "w", "w", "w", "w", "w", "w", "w",
         "w", "w", "w", "w", "w", "w", "w", "w", "w", "w", "b", "b", "b", "w", "w", "w", "w", "w"],
        ["w", "w", "w", "g", "g", "g", "g", "g", "g", "w", "w", "w", "g", "w", "w", "w", "w", "w", "w", "w", "w", "w",
         "w", "w", "g", "g", "w", "w", "w", "w", "w", "b", "b", "b", "w", "w", "w", "w", "w", "w"],
        ["w", "w", "w", "g", "w", "w", "w", "w", "w", "w", "w", "w", "g", "w", "w", "w", "w", "w", "w", "w", "w", "w",
         "w", "w", "g", "g", "w", "w", "w", "w", "w", "b", "b", "b", "w", "w", "w", "w", "w", "w"],
        ["w", "w", "w", "w", "w", "w", "w", "g", "w", "w", "w", "w", "g", "w", "w", "w", "w", "w", "w", "w", "w", "w",
         "w", "w", "w", "w", "w", "w", "w", "w", "b", "b", "b", "w", "w", "w", "w", "w", "w", "w"],
        ["w", "w", "w", "g", "w", "w", "w", "g", "w", "w", "w", "w", "g", "w", "w", "w", "w", "w", "w", "w", "w", "w",
         "w", "w", "w", "w", "w", "w", "w", "b", "b", "b", "w", "w", "w", "w", "w", "w", "w", "w"],
        ["w", "w", "w", "g", "w", "w", "w", "g", "w", "w", "w", "w", "g", "w", "w", "w", "w", "w", "w", "w", "w", "w",
         "w", "w", "w", "w", "w", "w", "b", "b", "b", "w", "w", "w", "w", "w", "w", "w", "w", "w"]]

    def  test1():
        # 左上角为 （0，0） 向下为x轴向右为y轴
        start1 = [4, 1]
        target1 = [5, 11]
        s = Astar(problem1)
        # path1, path2 = s.one_way(start1, target1), []
        path1, path2 = s.two_way(start1, target1)
        draw(problem1, path1, path2, width=7, height=2)

    def test2():
        start2 = [10, 4]
        target2 = [0, 35]

        s = Astar(problem2)
        # path1, path2 = s.one_way(target2, start2), []
        # path1, path2 = s.one_way(start2, target2), []
        path1, path2 = s.two_way(start2, target2)
        draw(problem2, path1, path2, width=3, height=1)
    # test1()
    test2()
    mainloop()
