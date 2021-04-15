# coding=utf-8
#import pulp
import random
import time
import matplotlib.pyplot as plt  
#生成实验数据
'''
class generate():
    def __init__(self):
        self.rawData = []
        self.data = []
    
    def generateData(self, size):
        #X是原始数据集，用set表示防止重复
        X = set(list(range(size)))
        self.rawData = X
        #S代表每次生成的数据集合, random.sample函数返回X中长为20的子序列
        S = [random.randint(0, size-1) for i in range(20)]
        S = set(S)
        self.data.append(list(S))
        #rest表示剩余集合,unionS表示子集覆盖集合
        rest, unionS = X - S, S
        while len(rest) >= 20:
            n = random.randint(1,20)
            x = random.randint(1,n)
            
            S = set(random.sample(rest, x))
            rest = rest - S #更新剩余集合
            S.update(random.sample(unionS, n-x)) 
            unionS.update(S) #更新已经被选择的数据集合
            self.data.append(list(S))

        #小于20时直接加入
        if len(rest) > 0:
            self.data.append(list(rest))
        #生成|F|-y个随机集合
        y = len(self.data)
        for i in range(size - y):
            n = random.randint(1,20)
            S = random.sample(X, n)    
            self.data.append(list(S))  
        for i in range(len(self.data)):
            self.data[i] = set(self.data[i])

class solution():
    #贪心策略实现近似算法
    def greedy(self, X, F):
        res = []
        while X:
            #贪心策略，每次选择最多的元素集合，以intersection() 方法用于返回两个或更多集合中都包含的元素，即交集。
            S = max(F, key=lambda x: len(X.intersection(x)))
            X -= S
            res.append(S)
        return res
    #线性规划实现近似算法
    def LP(self, X, F):
        X = list(X)
        A = []
        #写出限制条件矩阵
        for i in range(len(X)):
            row = []
            for j in range(len(F)):
                row.append(1 if X[i] in F[j] else 0)
            A.append(row)
        t = 1 / max([sum(r) for r in A])
        
        #构建线性方程
        prob = pulp.LpProblem("Linear minimize problem", pulp.LpMinimize)
        ingredient_vars = pulp.LpVariable.dicts("Ingr", X, 0, 1)
        
        prob += pulp.lpSum([1 * ingredient_vars[i] for i in X])
        for i in range(len(X)):
            prob += pulp.lpSum([A[i][j] * ingredient_vars[j] for j in range(len(F))]) >= 1
        prob.solve()

        prob = prob.variables()
        #按照目标方程排序
        prob = sorted(prob, key=lambda x: int(x.name[5:]))
        #按照阈值进行舍入
        C = [set(f) for i, f in enumerate(F) if prob[i].varValue > t]
        return C
'''
if __name__ == "__main__":

    time1 = []
    time2 = []
    x = [100, 1000, 5000]
    time1 = [59.79800224304199, 4426.928758621216, 263768.18799972534] 
    time2 = [0.8149147033691406, 88.83404731750488, 3195.448875427246] 
    
    plt.rcParams['font.sans-serif']=['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.title('结果')
    plt.xlabel("数据量/个") #xlabel、ylabel：分别设置X、Y轴的标题文字。
    plt.ylabel("算法运行时间/ms")
    
    plt.plot(x, time1,  color='red', label='贪心')
    plt.plot(x, time2,  color='blue', label='线性规划')
    plt.legend() 
    plt.show()
    
    '''

    datasize = [100, 1000, 5000]
    for item in datasize:
        g = generate()
        g.generateData(item)
        s = solution()
        time1 = time.time()
        s.LP(g.rawData, g.data)
        time2 = time.time()
        print((time2 - time1)*1000 )

        time1 = time.time()
        s.greedy(g.rawData, g.data)
        time2 = time.time()
        print((time2 - time1)*1000)

    '''
    #print (s.LP(g.rawData, g.data))