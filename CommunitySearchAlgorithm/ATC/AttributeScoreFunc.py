
from ATC import GraphFunc

INF = float('inf')


def thetaFunc(H, w):
    cnt = sum(w in H[v][1] for v in H)
    return cnt / len(H)


def thetaFuncforWqSet(H,W):
    ans = 0
    for w in W:
        ans += thetaFunc(H,w)
    return ans


def attributeScore(H, W):
    ans = 0
    for w in W:
        ans += (thetaFunc(H, w) ** 2) * len(H)
    return ans


def computeGainFunc(k, graph, Wq):
    gain = {}
    fHWq = attributeScore(graph,Wq)
    for v in graph.keys():
        flagv = {}
        for u in graph[v][0]:
            if len(graph[u][0]) == k-1:
                flagv[u]=0
            else :
                flagv[u] = 1
        flagv[v] = 0
        flagset = []
        for u in graph.keys():
            if flagv.get(u) is None: flagset.append(u)
            elif flagv[u] == 1: flagset.append(u)
        newG = GraphFunc.buildNewGraph(graph, flagset)
        if len(newG) == 0:
            gain[v] = INF
        else:
            gain[v] = fHWq - attributeScore(GraphFunc.buildNewGraph(graph, flagset), Wq)
    return gain