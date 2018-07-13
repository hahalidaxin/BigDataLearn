import queue
import copy
import random
from collections import defaultdict
from collections import Counter
import sys
sys.path.append("../")
from ATC import GraphFunc
from ATC import ATindex
from ATC.Steiner import Steiner
from ATC import AttributeScoreFunc
import CommunitySearch as CS


INF = float('inf')
erlta = 3
szLimit = 20


def cedge(u,v):
    return min(u,v),max(u,v)


def getGraphWithAttrDist(graph,Wq,attrTE):
    delta = 3
    maxTe = max(attrTE[''].values())
    newG = defaultdict(list)
    for v in graph.keys():
        for u in graph[v][0]:
            if v>u: continue
            distuv = 1
            for w in Wq:
                if attrTE[w].get(cedge(u, v)) is None:
                    distuv += maxTe
                else:
                    distuv += maxTe - attrTE[w][cedge(u, v)]
            newG[v].append((u, distuv))
            newG[u].append((v, distuv))
    return dict(newG)


def ExtendtoGt(steinerT, origraph,Wq, TE):
    que = queue.Queue()
    flag = defaultdict(int)
    kt = float('inf')
    newG = {}
    for v in steinerT.keys():
        que.put(v)
        flag[v] = 1
        newG[v] = [copy.deepcopy(steinerT[v]), copy.deepcopy(origraph[v][1])]
        kt = min(kt,min(TE[cedge(u,v)] for u in steinerT[v]))
    Wq_extend = set(copy.deepcopy(Wq))
    while not que.empty():
        u = que.get()
        for v in graph[u][0]:
            if TE[cedge(u, v)] >= kt:
                if len(newG.keys()) >= szLimit:
                    return newG
                else:
                    # AttributeScore条件约束
                    if AttributeScoreFunc.thetaFuncforG(newG, list(Wq_extend & set(origraph[v][1]))) < AttributeScoreFunc.\
                            thetaFuncforG(newG, Wq_extend) / (2 * len(newG)): continue
                    if newG.get(v) is None:
                        newG[v] = [[],copy.deepcopy(origraph[v][1])]
                    if newG[v][0].count(u) == 0:
                        newG[v][0].append(u)
                        newG[u][0].append(v)
                    if flag[v] == 0:
                        Wq_extend = Wq_extend & set(graph[v][1])
                        flag[v] = 1
                        que.put(v)
    return newG


def MaintainKDTruss(k,d,graph,Q,Wq):
    Gt = copy.deepcopy(graph)
    while True:
        TE,supE = ATindex.StructuralTrussness(Gt)
        distG = GraphFunc.getDistG(Gt,Q)
        edgestodelete = {}
        for v in supE:
            if supE[v] < k-2:
                for u in Gt[v][0]:
                    edgestodelete[cedge(u,v)] = 1
        for e in distG.keys():
            if distG[e] > d:
                edgestodelete[e]=1
        if len(edgestodelete) == 0: return Gt
        Gt = GraphFunc.deleteEdges(Gt,edgestodelete)
        if len(Gt) == 0: break
    return Gt

def BULK(graph,Q,Wq,k,d):
    l = 0
    Gl = copy.deepcopy(graph)
    distG = GraphFunc.getDistG(graph,Q)
    if d is None: d=max(distG.values())
    S = [v for v in Gl.keys() if distG[v]<=d]
    for q in Q:
        if not q in S: return False
    Gl = GraphFunc.buildNewGraph(Gl, S)
    if k is None: k = max(ATindex.StructuralTrussness(Gl)[0].values())
    maxfunc, ansg = -INF, None
    while GraphFunc.connected(graph,Q):
        attriscore = AttributeScoreFunc.attributeScore(Gl, Wq)
        if maxfunc < attriscore: maxfunc, ansg = attriscore, copy.deepcopy(Gl)

        gain = AttributeScoreFunc.computeGainFunc(k,graph,Wq)
        mingain = INF
        for v in gain:
            if gain[v] < mingain and not v in Q : mingain = gain[v]
        if mingain == INF : break
        S = [v for v in gain.keys() if gain[v] == mingain and not v in Q]
        S = random.sample(S,max(1,int(len(S)*erlta/(erlta+1))))
        edgesToDelete = GraphFunc.getNeighborEdges(Gl,S)
        Gl = GraphFunc.deleteEdges(Gl,edgesToDelete)
        Gl = MaintainKDTruss(k,d,Gl,Q,Wq)

    return list(ansg.keys())

def locATC(graph,Q,Wq,k=None,d=None):
    global attrTE,attrSupE
    attrTE,attrSupE= ATindex.AttributedTrussness(graph,Wq)
    steiner = Steiner(getGraphWithAttrDist(graph,Wq,attrTE),Q)  # steiner G 's :{v->[u1,u2...]}
    Gt = ExtendtoGt(steiner.G,graph,Wq,attrTE[''])
    ansg = BULK(Gt,Q,Wq,k,d)


if __name__ == "__main__":
    '''
    graph = CS.tempt_nodes_information
    group = CS.graph_information['Groups']['circle0']
    Q = random.sample(group[0],min(5,len(group[0])))
    Wq = random.sample(group[1],min(3,len(group[1])))
    print(locATC(graph, Q, Wq))
    '''
    G = {'222': [['0', '186', '240'], [8, 51, 54, 56, 60, 66, 78, 93, 101, 127, 139, 172, 193, 215]], '0': [['183', '222', '54'], [10, 15, 40, 51, 53, 54, 55, 56, 70, 79, 105, 128, 130, 146, 148, 152, 157, 161, 164, 167, 169, 177, 193, 196, 206, 207, 209, 211, 213, 220]], '183': [['0', '133'], [8, 53, 54, 56, 66, 78, 91, 93, 128, 129, 142, 157, 170, 175, 212, 218]], '133': [['183'], [8, 51, 54, 56, 60, 66, 78, 128, 139]], '54': [['0'], [79, 93, 101, 128, 134]], '186': [['222'], [75, 78, 128]], '240': [['222'], [51, 54, 55, 69, 70, 78, 128]]}
    TE,supE = ATindex.StructuralTrussness(G)