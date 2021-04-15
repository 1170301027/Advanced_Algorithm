#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: lenovo
@file: Astar.py
@time: 2021/4/12 18:26
"""
import matplotlib.pyplot as plt
from tkinter import *

tk = Tk()


class pointInfo:
    # prevPoints 为预先已经经过的节点，不能出现重复
    # f为实际代价
    # h为预估代价,采用哈夫曼距离
    def __init__(self, father, cur, f, h):
        self.father = father
        self.cur = cur
        self.f = f
        self.h = h


class Astar:
    def __init__(self, points):
        self.points = points

    def next_step(self, curinfo, f, end, open, close):
        # 获取当前坐标
        cur = curinfo.cur
        for i in range(max(cur[0] - 1, 0), min(len(self.points), cur[0] + 2)):
            for j in range(max(cur[1] - 1, 0), min(len(self.points[0]), cur[1] + 2)):
                # 原节点不扩展
                if i == cur[0] and j == cur[1]:
                    continue
                # 遇到障碍物不可扩展
                if self.points[i][j] == "g":
                    continue
                if (i, j) in close:
                    continue
                newf = f
                # 计算已经经过的代价
                if abs(i - cur[0]) == 1 and abs(j - cur[1]) == 1:
                    newf += 1.4142135623731
                else:
                    newf += 1
                if self.points[i][j] == "y":
                    newf += 4
                elif self.points[i][j] == "b":
                    newf += 2

                nextPoint = pointInfo(curinfo, (i, j), newf, abs(end[0] - i) + abs(end[1] - j))
                tmp = open.get((i, j))
                if not tmp:
                    open[(i, j)] = nextPoint
                elif tmp.f > nextPoint.f:
                    open.pop((i, j))
                    open[(i, j)] = nextPoint

    def selectBest(self, open, close):
        res, min_f = None, float('inf')
        for point, info in open.items():
            if info.f < min_f:
                res, min_f = point, info.f
        # 当前节点是某一条最优路径的节点，后续如果说扩展到此节点，那么代价一定比此时的大，所以无需扩展
        close.add(res)
        return open.pop(res)

    def singleway(self, start, end):
        open = {}
        open[(start[0], start[1])] = pointInfo(None, (start[0], start[1]), 0,
                                               abs(end[1] - start[1]) + abs(end[0] - start[1]))
        close = set()
        while True:
            curinfo = self.selectBest(open, close)
            # 到达节点
            if curinfo.cur[0] == end[0] and curinfo.cur[1] == end[1]:
                path = []
                # 不断向上迭代
                while curinfo:
                    path.append([curinfo.cur[0], curinfo.cur[1]])
                    curinfo = curinfo.father
                path.reverse()
                return path
            self.next_step(curinfo, curinfo.f, end, open, close)

    def Twoway(self, start, end):
        startOpen = {}
        startOpen[(start[0], start[1])] = pointInfo(None, (start[0], start[1]), 0,
                                                    abs(end[1] - start[1]) + abs(end[0] - start[1]))
        startClose = set()

        endOpen = {}
        endOpen[(end[0], end[1])] = pointInfo(None, (end[0], end[1]), 0,
                                              abs(end[1] - start[1]) + abs(end[0] - start[1]))
        endClose = set()
        # endCurInfo = endOpen[(end[0], end[1])]

        cur1, cur2 = None, None
        while True:
            startCur = self.selectBest(startOpen, startClose)
            self.next_step(startCur, startCur.f, end, startOpen, startClose)
            for key in startOpen.keys():
                if key in endOpen:
                    startCur, endCur = startOpen[key], endOpen[key]
                    # if startCur.f + endCur.f < g:
                    #    g = startCur.f + endCur.f
                    cur1, cur2 = startCur, endCur
                    break

            if cur1 and cur2:
                break

            endCur = self.selectBest(endOpen, endClose)
            self.next_step(endCur, endCur.f, start, endOpen, endClose)
            for key in endOpen.keys():
                if key in startOpen:
                    startCur, endCur = startOpen[key], endOpen[key]
                    # if startCur.f + endCur.f < g:
                    #    g = startCur.f + endCur.f
                    cur1, cur2 = startCur, endCur
                    break

            if cur1 and cur2:
                break

        res1 = []
        while cur1:
            res1.append([cur1.cur[0], cur1.cur[1]])
            cur1 = cur1.father
        res1.reverse()

        res2 = []
        while cur2:
            res2.append([cur2.cur[0], cur2.cur[1]])
            cur2 = cur2.father
        res2.reverse()
        return res1, res2

        '''
        startCurInfo, endCurInfo = None, None
        while True:
            startCurInfo = self.selectBest(startOpen, startClose)
            print(startCurInfo.cur)
            if startCurInfo and endCurInfo and  startCurInfo.cur == endCurInfo.cur:
                break
            self.next_step(startCurInfo, startCurInfo.f, end, startOpen, startClose)

            endCurInfo = self.selectBest(endOpen, endClose)
            print(endCurInfo.cur)
            if startCurInfo and endCurInfo and startCurInfo.cur == endCurInfo.cur:
                break
            self.next_step(endCurInfo, endCurInfo.f, start, endOpen, endClose)

        res1 = []
        while startCurInfo:
            res1.append([startCurInfo.cur[0], startCurInfo.cur[1]])
            startCurInfo = startCurInfo.father
        res1.reverse()

        res2 = []
        while endCurInfo:
            res2.append([endCurInfo.cur[0], endCurInfo.cur[1]])
            endCurInfo = endCurInfo.father
        res2.reverse()
        return res1, res2
        '''


# 为了实现函数复用，让res1和res2分别表示从start, end出发的路径，既可以画单向的，又可以画双向的
def draw(points, res1, res2, start, end, width, height):
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
    for i in range(len(res1) - 1):
        if i == 0:
            Button(tk, bg="Violet", width=width, height=height, text="Start").grid(row=res1[i][0], column=res1[i][1],
                                                                                   sticky=W + E + N + S)
        else:
            Button(tk, bg="Violet", width=width, height=height).grid(row=res1[i][0], column=res1[i][1],
                                                                     sticky=W + E + N + S)
    if len(res2) == 0:
        Button(tk, bg="Violet", width=width, height=height, text="End").grid(row=res1[-1][0], column=res1[-1][1],
                                                                             sticky=W + E + N + S)
        return
    for i in range(len(res2)):
        if i == 0:
            Button(tk, bg="SpringGreen", width=width, height=height, text="End").grid(row=res2[i][0], column=res2[i][1],
                                                                                      sticky=W + E + N + S)
        else:
            Button(tk, bg="SpringGreen", width=width, height=height).grid(row=res2[i][0], column=res2[i][1],
                                                                          sticky=W + E + N + S)


if __name__ == "__main__":
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

    start1 = [4, 0]
    end1 = [5, 11]

    start2 = [10, 4]
    end2 = [0, 35]

    s = Astar(problem1)
    path1, path2 = s.Twoway(start1, end1)
    draw(problem1, path1, path2, start1, end1, 7, 2)
    # s = Astar(problem2)
    # path1, path2 = s.Twoway(start2, end2)
    # path1 = s.singleway(start2, end2)
    # path2 = []
    # draw(problem2, path1, path2, start2, end2, 3, 1)
    # res1 = [[4, 0] ,[4, 1] ,[4, 2] ,[3, 3], [2, 4], [3, 5],[4, 6],[5, 7],[5, 8],[5, 9],[5, 10],[5, 11]]
    mainloop()
