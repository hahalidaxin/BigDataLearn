import copy
from collections import defaultdict

import sys
sys.path.append(r"..\\")
from ATC import GraphFunc

def cedge(u, v):
    return min(u, v), max(u, v)


def StructuralTrussness(graph):
    # 利用Improved Truss Decomposition算法 计算grapn中每条边的trussness
    supE = defaultdict(int)
    edgeExist = defaultdict(int)
    for u in graph.keys():
        for v in graph[u][0]:
            e = cedge(u, v)
            if 0 == edgeExist[e]:
                edgeExist[e] = 1
                if graph.get(v) is None:  # 使用defaultdict的后遗症
                    supE[e] = 0
                else:
                    supE[e] = len(set(graph[u][0]) & set(graph[v][0]))  # 这个地方可能会有点儿慢
    ansSupE = copy.deepcopy(supE)
    # 构造vert 按照sup顺序存储所有的边 其中bin与pos是辅助数组 使得update操作能够在常数时间内完成
    vert = sorted(supE.keys(), key=lambda x: supE[x])
    bin, pos = {}, {}
    last, numEdge = -1, vert.__len__()
    for i in range(numEdge):
        pos[vert[i]] = i
        if (supE[vert[i]] != last):
            bin[supE[vert[i]]] = i
            last = supE[vert[i]]
    k, lowestSup = 2, 0
    tmpNumEdge = numEdge
    TE = defaultdict(int)
    while (numEdge):
        while (lowestSup < tmpNumEdge and supE[vert[lowestSup]] <= k - 2):
            u, v = e = vert[lowestSup]
            for w in graph[u][0]:
                e1 = cedge(v, w)
                e2 = cedge(u, w)
                if (edgeExist[e1] and edgeExist[e2]):
                    # 维护vert 改变两条边在vert中的位置
                    for ex in [e1, e2]:
                        pw = max(bin[supE[ex]], lowestSup + 1)
                        pu = pos[ex]
                        fe = vert[pw]
                        if (fe != ex):
                            pos[ex] = pw
                            pos[fe] = pu
                            vert[pw] = ex
                            vert[pu] = fe
                        bin[supE[ex]] += 1
                        if (bin.get(supE[ex] - 1) is None):
                            bin[supE[ex] - 1] = pos[ex]
                        supE[ex] -= 1

            TE[e] = k
            edgeExist[e] = 0
            numEdge -= 1
            if (numEdge == 0): break
            lowestSup += 1
        k += 1
    return dict(TE), dict(ansSupE)

def AttributedTrussness(graph,Wq):
    attrTE = {}
    attrSupE = {}
    attrTE[''],attrSupE[''] = StructuralTrussness(graph)
    for w in Wq:
        flag = [v for v in graph.keys() if w in graph[v][1]]
        subgraph = GraphFunc.buildNewGraph(graph, flag)
        attrTE[w], attrSupE[w] = StructuralTrussness(subgraph)
    return attrTE, attrSupE