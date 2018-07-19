import queue
from collections import defaultdict
from ATC import GraphFunc

def cedge(u,v):
    return min(u,v),max(u,v)


class Steiner:
    def __init__(self, graph, Q):
        self.factor = 3
        self.INF = float('inf')
        self.G = self.CONSTRUCT(graph, Q)

    def SPFA(self, graph, Q):
        distG, inq, s = {}, {}, {}
        father = {}

        for v in graph.keys():
            distG[v] = self.INF

        que = queue.Queue()
        for q in Q:
            father[q] = q
            que.put(q)
            distG[q], inq[q] = 0, 1
            s[q] = q
        while not que.empty():
            u = que.get()
            inq[u] = 0
            for v, w in graph[u]:
                if distG[u] + w < distG[v]:
                    distG[v] = distG[u] + w
                    father[v] = u
                    if not v in inq or not inq[v]:
                        s[v] = s[u]
                        que.put(v)
                        inq[v] = 1
        return s, distG, father

    def find(self, x, fa):
        if x == fa[x]:
            return x
        else:
            fa[x] = self.find(fa[x], fa)
            return fa[x]

    def KRUSKAL(self, graph):
        edges, fa = [], {}
        ansG = defaultdict(list)
        for u in graph.keys():
            fa[u] = u
            for v, w in graph[u]:
                if u < v:  edges.append((u, v, w))
        edges = sorted(edges, key=lambda x: (x[2], x[0], x[1]))
        for u, v, w in edges:
            x, y = self.find(u, fa), self.find(v, fa)
            if x != y:
                fa[x] = y
                ansG[u].append((v, w))
                ansG[v].append((u, w))
        if len(graph) == 1: ansG[list(graph.keys())[0]] = []
        return ansG

    def EXPAND(self, graph, oriGraph):
        newG = defaultdict(list)
        distG = self.distG
        father = self.father
        distuv , oridistuv= {},{}
        for v in graph.keys():
            for u, w in graph[v]:
                distuv[cedge(u, v)] = w
        for v in oriGraph.keys():
            for u, w in oriGraph[v]:
                oridistuv[cedge(u,v)] = w

        flagedge = {}
        for v in self.s.keys():
            if oriGraph.get(v) is None: continue
            for u,w in oriGraph[v]:
                if self.s[u] < self.s[v] and not cedge(self.s[u],self.s[v]) in flagedge:
                    dist = distuv.get(cedge(self.s[u], self.s[v]))
                    if not dist is None and distG[v] + distG[u] + w == dist:
                        for x in [u, v]:
                            while x != father[x]:
                                newG[x].append((father[x], oridistuv[cedge(father[x],x)]))
                                newG[father[x]].append((x, oridistuv[cedge(father[x],x)]))
                                x = father[x]
                        newG[u].append((v, oridistuv[cedge(u,v)]))
                        newG[v].append((u, oridistuv[cedge(u,v)]))
                        flagedge[cedge(self.s[u], self.s[v])] = 1
        if len(graph) == 1: newG[list(graph.keys())[0]] = []
        for v in newG.keys():
            newG[v] = {}.fromkeys(newG[v]).keys()  # 去掉重复的边
        return newG

    def DELETELEAF(self, graph, Q):
        flag = {}
        for v in graph.keys():
            flag[v] = 0 if (len(graph[v]) == 1 and not (v in Q)) else 1
        newG = {}
        for v in graph.keys():
            if flag[v]:
                newG[v] = []
                for u, w in graph[v]:
                    if flag[u]:
                        newG[v].append(u)
        return newG

    def GETG1(self, graph, Q):
        self.s, self.distG, self.father = self.SPFA(graph, Q)
        distuv = {}
        for v in graph.keys():
            for u,w in graph[v]:
                distuv[cedge(u,v)]=w
        triList = []
        for u in graph.keys():
            if self.s.get(u) is None:
                continue
            for v,w in graph[u]:
                if self.s.get(v) is None: continue
                if self.s[u] < self.s[v]:
                    triList.append((self.s[u], self.s[v], self.distG[u] + self.distG[v] + distuv[cedge(u,v)]))
        G1 = defaultdict(list)
        triList = sorted(triList, key=lambda x: x)
        for i in range(triList.__len__()):
            u, v, w = triList[i]
            if (i == 0 or (u, v) != triList[i - 1][0:2]):
                G1[u].append((v, w))
                G1[v].append((u, w))
        if len(Q) == 1: G1[Q[0]] = []
        # flagset = [v for v in G1.keys() if not self.s.get(v) is None]
        return G1

    def CONSTRUCT(self, graph, Q):
        G1 = self.GETG1(graph, Q)
        # G2 = self.KRUSKAL(G1)
        if len(G1)==0: return []
        G3 = self.EXPAND(G1, graph)
        G4 = self.KRUSKAL(G3)
        G5 = self.DELETELEAF(G4, Q)
        flag = False
        for v in Q:
            if G5.get(v) is None:
                flag = True
                break
        if flag:
            return None
        else:
            return G5