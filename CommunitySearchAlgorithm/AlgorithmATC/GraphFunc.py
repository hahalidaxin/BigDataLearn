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


# G = {[(u1,w1),()...],[]}
def buildNewGraph2(graph,flagset):
    newG = {}
    for v in flagset:
        newG[v] = []
        for u, w in graph[v]:
            if u in flagset:
                newG[v].append((u, w))
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


def bfsMinDist(graph,Q):
    distG = {}
    que = queue.Queue()
    for q in Q:
        distG[q] = 0
        que.put(q)
    while not que.empty():
        u = que.get()
        for v in graph[u][0]:
            if not v in distG:
                distG[v] = distG[u] + 1
                que.put(v)
    return distG


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
            print("yes")
    return distG, s, father


#dfs遍历graph 区分联通块
def dfsWithLable(v, graph, flag, color):
    flag[v] = color
    if len(graph[v]) == 2 and type(graph[v])!=tuple and \
        type(graph[v][1])==list:
        for e in graph[v][0]:
            u = e if not type(e) == tuple else e[0]
            if not flag[u]:
                dfsWithLable(u, graph, flag, color)
    else:
        for e in graph[v]:
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
    distG = {v:-INF for v in graph.keys()}
    for q in Q:
        distG[q] = 0
        tmpdist = bfsMinDist(graph,[q])
        for v in distG.keys():
            if v in tmpdist:
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


def addNodewithG(graph, origraph, u):
    newG = copy.deepcopy(graph)
    newG[u] = [[], copy.deepcopy(origraph[u][1])]
    for v in origraph[u][0]:
        if v in newG and newG[v][0].count(u) == 0:
            newG[v][0].append(u)
            newG[u][0].append(v)
    return newG