import copy
import queue
from collections import defaultdict


INF = float('inf')


def cedge(u,v):
    return min(u,v),max(u,v)

# flag -> a set indicates existence
def buildNewGraph(graph,flagv):
    newG = {}
    flag = defaultdict(int)
    for v in flagv: flag[v] = 1
    for v in flag.keys():
        newG[v] = [[],[]]
        for u in graph[v][0]:
            if flag.get(u) is None or not flag[u]: continue
            newG[v][0].append(u)
        newG[v][1] = copy.deepcopy(graph[v][1])
    return newG


def deleteEdges(graph,edgestoDelete):
    newG = {}
    for v in graph.keys():
        newG[v]=[[],copy.deepcopy(graph[v][1])]
        for u in graph[v][0]:
            if not cedge(u,v) in edgestoDelete:
                newG[v][0].append(u)
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
        for v, w in graph[u][0]:
            if distG[u] + w < distG[v]:
                distG[v] = distG[u] + w
                father[v] = u
                s[v] = s[u]
                que.put(v)
                inq[v] = 1
    return distG, s, father


#dfs遍历graph 区分联通块
def dfsWithLable(v, graph, flag, color):
    flag[v] = color
    for u, w in graph[v]:
        if not flag[u]:
            dfsWithLable(u, graph, flag, color)


#判断Q点集在graph中是否依旧联通
def connected(graph, Q):
    if len(graph) == 0: return False
    flag = defaultdict(int)
    color = 0
    for v in Q:
        if not flag[v]:
            color += 1
            if color >= 2: break
            dfsWithLable(v, graph, flag, color)
    return True if color == 1 else False


def getDistG(graph,Q):
    distG = {v:-INF for v in graph.keys()}
    newG = {}
    for v in graph.keys():
        newG[v] = [[],copy.deepcopy(graph[v][1])]
        for u in graph[v][0]:
            newG[v][0].append((u,1))

    for q in Q:
        tmpdist,s,father = SPFA(newG,[q])
        for v in distG.keys():
            distG[v] = max(distG[v],tmpdist[v])
    return distG


#获得graph中S点集的相邻点
def getNeighborEdges(graph,S):
    edges = []
    for v in S:
        for u in graph[v]:
            if u < v:
                edges.append(cedge(u, v))
    return edges