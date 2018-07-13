import copy
import queue
from collections import defaultdict


INF = float('inf')


def cedge(u,v):
    return min(u,v),max(u,v)


# flag -> a set indicates existence
def buildNewGraph(graph, flagv):
    newG = {}
    flag = defaultdict(int)
    for v in flagv: flag[v] = 1
    for v in flag.keys():
        newG[v] = [[], []]
        for u in graph[v][0]:
            if flag.get(u) is None or not flag[u]: continue
            newG[v][0].append(u)
        newG[v][1] = copy.deepcopy(graph[v][1])
    return newG


def deleteEdges(graph, edgestoDelete):
    newG = {}
    flagedges = defaultdict(int)
    for e in edgestoDelete:
        flagedges[e] = 1
    tmpset = []
    for v in graph.keys():
        newG[v]=[[],copy.deepcopy(graph[v][1])]
        for u in graph[v][0]:
            if flagedges[cedge(u,v)]==0:
                newG[v][0].append(u)
        if len(newG[v][0]) == 0: tmpset.append(v)
    for v in tmpset: del(newG[v])
    return newG


#以Q中的点为点集 跑SPFA算法
def SPFA(graph, Q):
    distG, inq, s = {}, {}, {}
    father = {}

    for v in graph.keys():
        distG[v] = INF

    que = queue.Queue()
    for q in Q:
        father[q] = q
        que.put(q)
        distG[q], inq[q] = 0, 1
        s[q] = q
    while not que.empty():
        u = que.get()
        inq[u] = 0
        try:
            for v, w in graph[u][0]:
                if distG[u] + w < distG[v]:
                    distG[v] = distG[u] + w
                    father[v] = u
                    s[v] = s[u]
                    que.put(v)
                    inq[v] = 1
        except:
            print("yesss")
    return distG, s, father


#dfs遍历graph 区分联通块
def dfsWithLable(v, graph, flag, color):
    flag[v] = color
    for e in graph[v][0]:
        u = e if not type(e) == tuple else e[0]
        if not flag[u]:
            dfsWithLable(u, graph, flag, color)


#判断Q点集在graph中是否依旧联通
def connected(graph, Q):
    if len(graph) == 0: return False
    flag = defaultdict(int)
    color = 0
    for v in Q:
        if graph.get(v) is None: return False
        if not flag[v]:
            color += 1
            if color >= 2: break
            dfsWithLable(v, graph, flag, color)
    return True if color == 1 else False


def getDistG(graph,Q):
    flagq = defaultdict(int)
    for q in Q: flagq[q] = 1
    distG = {v:-INF for v in graph.keys()}
    newG = {}
    for v in graph.keys():
        newG[v] = [[],copy.deepcopy(graph[v][1])]
        for u in graph[v][0]:
            newG[v][0].append((u,1))

    for q in Q:
        distG[q] = 0
        tmpdist,s,father = SPFA(newG,[q])
        for v in distG.keys():
            if not flagq[v]:
                distG[v] = max(distG[v],tmpdist[v])
    return distG


#获得graph中S点集的相邻点
def getNeighborEdges(graph,S):
    edges = []
    for v in S:
        try:
            for u in graph[v][0]:
                edges.append(cedge(u, v))
        except:
            print("yesss")
    return edges