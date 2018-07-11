from collections import defaultdict
from ATC import GraphFunc

def thetaFunc(H, w):
    cnt = 0
    for v in H.keys():
        if w in H[v][1]: cnt += 1
    return cnt / len(H)


def attributeScore( H, w):
    return thetaFunc(H, w) ** 2 * len(H)


def thetaFuncforG(G, Wq):
    invertedWq = defaultdict(list)
    ans = 0
    for v in G:
        for w in G[v][1]:
            invertedWq[w].append(v)
    for w in Wq:
        ans += len(invertedWq[w])/len(G)
    return ans


def computeGainFunc(k, graph, Wq):
    gain = {}
    fHWq = thetaFuncforG(graph,Wq)
    for v in graph.keys():
        flagset = [u for u in graph[v][0] if len(graph[u][0]) != k - 1]
        gain[v] = fHWq - thetaFuncforG(GraphFunc.buildNewGraph(graph, flagset), Wq)
    return gain