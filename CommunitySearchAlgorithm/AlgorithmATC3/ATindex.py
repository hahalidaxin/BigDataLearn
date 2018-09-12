import copy
import sys
sys.path.append(r"..\\")
from AlgorithmATC3 import GraphFunc

def cedge(u, v):
    return min(u, v), max(u, v)


def StructuralTrussness(graph):
    # 利用Improved Truss Decomposition算法 计算grapn中每条边的trussness
    supE = {}
    edgeExist = {}
    for u in graph.keys():
        for v in graph[u][0]:
            e = cedge(u, v)
            if edgeExist.get(e) is None:
                edgeExist[e] = 1
            #     if graph.get(v) is None:  # 使用defaultdict的后遗症
            #         supE[e] = 0
            #     else:
            #         supE[e] = len(set(graph[u][0]) & set(graph[v][0]))  # 这个地方可能会有点儿慢
    for u,v in edgeExist:
        if supE.get((u,v)) is None: supE[(u,v)]=0
        if len(graph[u][0]) > len(graph[u][0]):
            u, v = v, u
        for w in graph[u][0]:
            if edgeExist.get(cedge(u, w)) is not None and edgeExist.get(cedge(v, w)) is not None:
                supE[cedge(u, v)] = supE.get(cedge(u, v), 0)+1
                supE[cedge(u, w)] = supE.get(cedge(u, w), 0)+1
                supE[cedge(v, w)] = supE.get(cedge(v, w), 0)+1
    for e in edgeExist:
        supE[e] = int(supE[e]/3)
    # print('lenlen',len(edgeExist),len(supE))
    ansSupE = copy.deepcopy(supE)
    #print("ok1")
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
    TE = {}
    #print("ok2")
    while numEdge:
        while lowestSup < tmpNumEdge and supE[vert[lowestSup]] <= k - 2:
            u, v = e = vert[lowestSup]
            for w in graph[u][0]:
                e1 = cedge(v, w)
                e2 = cedge(u, w)
                if (edgeExist.get(e1) is not None and edgeExist[e1]==1) and \
                        (edgeExist.get(e2) is not None and edgeExist[e2]==1):
                    for ex in [e1, e2]:
                    # 维护vert 改变两条边在vert中的位置
                        pw = max(bin[supE[ex]], lowestSup + 1)
                        if pw==len(vert):
                            break
                        pu = pos[ex]
                        fe = vert[pw]
                        if fe != ex:
                            pos[ex] = pw
                            pos[fe] = pu
                            vert[pw] = ex
                            vert[pu] = fe
                        bin[supE[ex]] += 1
                        if bin.get(supE[ex] - 1) is None:
                            bin[supE[ex] - 1] = pos[ex]
                        supE[ex] -= 1
            TE[e] = k
            edgeExist[e] = 0
            numEdge -= 1
            lowestSup += 1
        k += 1
    return dict(TE), dict(ansSupE)


def AttributedTrussness(graph,Wq,attrTE_forall,attrSupE_forall):
    attrTE,attrSupE = {}, {}
    if attrTE_forall is None or len(attrTE_forall)==0:
        attrTE_forall,attrSupE_forall = StructuralTrussness(graph)
        # check
    for w in Wq:
        flag = [v for v in graph.keys() if w in graph[v][1]]
        subgraph = GraphFunc.buildNewGraph(graph, flag)
        attrTE[w], attrSupE[w] = StructuralTrussness(subgraph)
    return attrTE,attrSupE,attrTE_forall,attrSupE_forall