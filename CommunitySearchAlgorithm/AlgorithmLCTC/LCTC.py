import copy
import queue
from collections import defaultdict
from collections import Counter
import sys
import time
from . import SortAlgorithm
# import CommunitySearch as CS

INF = 9999999


class STEINER:
    def __init__(self, TE, graph, Q):
        self.factor = 3
        self.INF = INF
        self.TE = TE
        self.G = self.CONSTRUCT(graph, Q)

    def cedge(self, u, v):
        return min(u, v), max(u, v)

    def SPFA(self, graph, Q):
        distG, inq, s, distTruss = {}, {}, {}, {}
        father = {}
        self.maxTruss = maxTruss = max(self.TE.values())
        self.minTruss = minTruss = defaultdict(int)

        for v in graph.keys():
            distG[v] = self.INF
            distTruss[v] = self.INF
            minTruss[v] = maxTruss

        que = queue.Queue()
        for q in Q:
            father[q] = q
            que.put(q)
            distG[q], inq[q] = 0, 1
            distTruss[q] = 0
            s[q] = q
        while not que.empty():
            u = que.get()
            inq[u] = 0
            if graph.get(u) is None: continue
            for v in graph[u]:
                tmpminTruss = min(self.TE[self.cedge(u, v)], minTruss[u])
                tmpTruss = distG[u] + 1 + self.factor * (maxTruss - tmpminTruss)
                if tmpTruss < distTruss[v]:
                    distTruss[v] = tmpTruss
                    distG[v] = distG[u] + 1
                    minTruss[v] = tmpminTruss
                    father[v] = u
                    s[v] = s[u]
                    if inq.get(v) is None or not inq[v]:
                        que.put(v)
                        inq[v] = 1
        return s, distG, father, distTruss

    def GETG1(self, graph, Q):
        nowtime = time.time()
        self.s, self.distG, self.father, self.distTruss = self.SPFA(graph, Q)
        print("spfa time",time.time()-nowtime)
        nowtime = time.time()
        triList = []
        for u in graph:
            for v in graph[u]:
                if self.s.get(v) is None: continue
                if self.s[u] < self.s[v]:
                    deltadist = self.factor * (
                            self.maxTruss - min([self.minTruss[u], self.minTruss[v], self.TE[self.cedge(u, v)]]))
                    triList.append((self.s[u], self.s[v], self.distTruss[u] + self.distTruss[v] + deltadist, (u, v)))
        G1 = defaultdict(list)
        triList.sort()
        print('sortime',time.time()-nowtime)
        mediumTurple = {}
        for i in range(len(triList)):
            su, sv, w, (u, v) = triList[i]
            if i == 0 or (su, sv) != triList[i - 1][0:2]:
                G1[su].append((sv, w))
                G1[sv].append((su, w))
            mediumTurple[(su, sv)] = (u, v)
        if len(Q) == 1: G1[Q[0]] = []
        self.mediumTurple = mediumTurple
        return G1

    def find(self, x, fa):
        if x == fa[x]:
            return x
        else:
            fa[x] = self.find(fa[x], fa)
            return fa[x]

    def KRUSKAL(self, graph):
        edges, fa = [], {}
        ansG = defaultdict(list)
        for u in graph:
            fa[u] = u
            for v, w in graph[u]:
                if u < v:
                    edges.append((u, v, w))
        edges.sort(key=lambda x: (x[2], x[0], x[1]))
        for u, v, w in edges:
            x, y = self.find(u, fa), self.find(v, fa)
            if x != y:
                fa[x] = y
                ansG[u].append((v, w))
                ansG[v].append((u, w))
        if len(graph) == 1: ansG[list(graph.keys())[0]] = []
        return ansG

    def EXPAND(self, graph):
        newG = defaultdict(list)
        father = self.father
        mediumTurple = self.mediumTurple
        distuv = {}
        for v in graph:
            for u, w in graph[v]:
                distuv[self.cedge(u, v)] = w

        for su, sv in mediumTurple:
            u, v = mediumTurple[(su, sv)]
            for x in [u, v]:
                while x != father[x]:
                    tmpdist = 1 + self.factor * (self.maxTruss - self.TE[self.cedge(x, father[x])])
                    newG[x].append((father[x], tmpdist))
                    newG[father[x]].append((x, tmpdist))
                    x = father[x]
            tmpdist = 1 + self.factor * (self.maxTruss - self.TE[self.cedge(u, v)])
            newG[u].append((v, tmpdist))
            newG[v].append((u, tmpdist))
        if len(graph) == 1: newG[list(graph.keys())[0]] = []
        for v in newG:
            newG[v] = {}.fromkeys(newG[v]).keys()  # 去掉重复的边
        return newG

    def DELETELEAF(self, graph, Q):
        flag = {}
        for v in graph.keys():
            flag[v] = 0 if (graph[v].__len__() == 1 and not (v in Q)) else 1
        newG = defaultdict(list)
        for v in graph.keys():
            if flag[v]:
                newG[v] = []
                for u, w in graph[v]:
                    if flag[u]:
                        newG[v].append((u, 1))
        return newG

    def CONSTRUCT(self, graph, Q):
        nowtime = time.time()
        G1 = self.GETG1(graph, Q)
        nowtime = time.time()
        # G2 = self.KRUSKAL(G1)
        G3 = self.EXPAND(G1)
        nowtime = time.time()
        G4 = self.KRUSKAL(G3)
        nowtime = time.time()
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


class LCTCSearch:
    def __init__(self, graph_information, tempt_nodes_information, ExperimentalDataList):
        self.graph_information = graph_information
        self.tempt_nodes_information = tempt_nodes_information
        self.ExperimentalDataList = ExperimentalDataList
        return

    def cedge(self, u, v):
        return min(u, v), max(u, v)

    def EDGETRUSS(self, graph):
        # 利用Improved Truss Decomposition算法 计算grapn中每条边的trussness
        supE = defaultdict(int)
        edgeExist = defaultdict(int)
        nowtime = time.time()
        deg = {}
        for u in graph:
            deg[u] = len(graph[u])
            for v in graph[u]:
                e = self.cedge(u,v)
                if not edgeExist[e]:
                    edgeExist[e] = 1
                    supE[e] = len(set(graph[u])&set(graph[v]))
        '''
        for u in graph:
            deg[u] = len(graph[u])
            for v in graph[u]:
                e = self.cedge(u, v)
                edgeExist[e] = 1
        edgelist = list(edgeExist.keys())
        for e in edgelist:
            u,v = e
            x = u if deg[u]<deg[v] else v
            for w in graph[x]:
                if edgeExist[self.cedge(u,w)] and edgeExist[self.cedge(v,w)]:
                    supE[e] += 1
        '''
        ansSupE = copy.copy(supE)
        # 构造vert 按照sup顺序存储所有的边 其中bin与pos是辅助数组 使得update操作能够在常数时间内完成
        vert = SortAlgorithm.bulksort(list(supE.keys()),func = lambda x: supE[x])
        print("intersection time", time.time() - nowtime)
        nowtime = time.time()
        bin, pos = {}, {}
        last, numEdge = -1, len(vert)
        for i in range(numEdge):
            pos[vert[i]] = i
            if supE[vert[i]] != last:
                bin[supE[vert[i]]] = i
                last = supE[vert[i]]
        k, lowestSup = 2, 0
        tmpNumEdge = numEdge
        TE = defaultdict(int)
        while numEdge:
            while lowestSup < tmpNumEdge and supE[vert[lowestSup]] <= k - 2:
                u, v = e = vert[lowestSup]
                x = u if deg[u] < deg[v] else v
                for w in graph[x]:
                    e1 = self.cedge(v, w)
                    e2 = self.cedge(u, w)
                    if edgeExist[e1] and edgeExist[e2]:
                        # 维护vert 改变两条边在vert中的位置
                        for ex in [e1, e2]:
                            pw = max(bin[supE[ex]], lowestSup + 1)
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
                if numEdge == 0: break
                lowestSup += 1
            k += 1
        print("else time", time.time() - nowtime)
        return ansSupE, TE

    def BFSEXTENDG(self, graph, oriGraph, szLimit, TE):
        kt = INF
        for v in graph.keys():
            for u, w in graph[v]:
                if v < u: kt = min(kt, TE[self.cedge(v, u)])
        if len(graph) == 1: kt = 0
        que = queue.Queue()
        flag = defaultdict(int)
        for v in graph.keys():
            que.put(v)
            flag[v] = 1
        flagedge = defaultdict(int)
        while not que.empty() and len(graph) < szLimit:
            u = que.get()
            for v in oriGraph[u]:
                if TE[self.cedge(u, v)] >= kt:
                    if len(graph) >= szLimit:
                        break
                    else:
                        if not flagedge[self.cedge(u, v)]:
                            graph[v].append((u, 1))
                            graph[u].append((v, 1))
                            flagedge[self.cedge(u, v)] = 1
                        if flag[v] == 0:
                            flag[v] = 1
                            que.put(v)
        vertices = list(flag.keys())
        for v in vertices:
            for u in oriGraph[v]:
                if flag[u] and not flagedge[self.cedge(u, v)]:
                    graph[v].append((u, 1))

    def FINDG0(self, graph, oriGraph, Q, szLimit, TE):
        # 返回一个最大的k-truss，使得k-truss包含Q且k最大
        # First 使用truss-decomposition算法计算所有边的trussness
        # 这里接收到的graph是一棵steinertree
        nowtime = time.time()
        self.BFSEXTENDG(graph, oriGraph, szLimit, TE)
        newG = {v: [e[0] for e in graph[v]] for v in graph}
        print('sort time', time.time() - nowtime)
        # 对于排序 如果时间太长可以考虑使用桶排序
        for v in graph:
            graph[v].sort(key=lambda x: -TE[self.cedge(x[0], v)])
        k = min(TE[self.cedge(u, graph[u][0][0])] for u in Q)
        S = defaultdict(set)
        V, Vedge = set(), set()
        S[k] = set(Q)
        G0 = defaultdict(list)
        indexte = {v: 0 for v in graph}
        cnt = 0
        # print("k of this time ",k)
        while self.connected(G0, Q) is False:
            cnt += 1
            queK = queue.Queue()
            for v in S[k]: queK.put(v)
            while not queK.empty():
                v = queK.get()
                if v in V:
                    kmax = k + 1
                else:
                    kmax = INF
                    V.add(v)
                    if G0.get(v) is None:
                        G0[v] = []
                while indexte[v] < len(graph[v]) and \
                        TE[self.cedge(v, graph[v][indexte[v]][0])] >= k:
                    # print(TE[self.cedge(v, graph[v][indexte[v]][0])],k)
                    u, w = graph[v][indexte[v]]
                    if TE[self.cedge(u, v)] < kmax:
                        if not (self.cedge(u, v) in Vedge):
                            Vedge.add(self.cedge(u, v))
                            G0[u].append((v, 1))
                            G0[v].append((u, 1))
                        if not u in S[k]:
                            S[k].add(u)
                            queK.put(u)
                    indexte[v] += 1
                if not indexte[v] == len(graph[v]):
                    l = TE[self.cedge(v, graph[v][indexte[v]][0])]
                    S[l].add(v)
            k -= 1
        return G0

    def dfs(self, v, graph, color, flag):
        que = queue.Queue()
        que.put(v)
        flag[v] = color
        while not que.empty():
            v = que.get()
            for u, w in graph[v]:
                if not flag[u]:
                    flag[u] = color
                    que.put(u)

    def connected(self, graph, Q):
        if len(graph) == 0: return False
        flag = defaultdict(int)
        color, count = 1, 0
        for v in Q:
            if not flag[v]:
                count += 1
                if count >= 2: break
                self.dfs(v, graph, color, flag)
                color += 1
        if len(graph) == 0: return False
        return True if count == 1 else False

    def MAINTAINKTRUSS(self, graph, L, k, supE):
        S = set()
        flag = defaultdict(int)
        for v in L:
            for u, w in graph[v]:
                S.add(self.cedge(u, v))
        Nuv_list = {}
        while len(S):
            u, v = S.pop()
            if Nuv_list.get(self.cedge(u, v)) is None:
                Nuv = Nuv_list[self.cedge(u, v)] = set(graph[u]) & set(graph[v])
            else:
                Nuv = Nuv_list[self.cedge(u, v)]
            for w, wx in Nuv:
                e1, e2 = self.cedge(u, w), self.cedge(v, w)
                for ex in [e1, e2]:
                    supE[ex] -= 1
                    if supE[ex] < k - 2 and not ex in S and not flag[ex]:
                        S.add(ex)
            flag[self.cedge(u, v)] = 1
        ansG = defaultdict(list)
        for v in graph.keys():
            if not v in L:
                ansG[v] = []
                for u, w in graph[v]:
                    if not flag[self.cedge(u, v)]:
                        ansG[v].append((u, 1))
        return ansG

    def COMPUTEDIST(self, graph, Q):
        ansdistG = {}
        for v in graph.keys(): ansdistG[v] = -INF
        for q in Q:
            distG = {}
            flag = defaultdict(int)
            que = queue.Queue()
            distG[q] = 0
            flag[q] = 1
            que.put(q)
            while not que.empty():
                u = que.get()
                for v, w in graph[u]:
                    if flag[v] == 0:
                        distG[v] = distG[u] + 1
                        flag[v] = 1
                        que.put(v)
            for v in distG:
                ansdistG[v] = max(distG[v], ansdistG[v])
        return ansdistG

    def BUILKDELETE(self, graph, Q, TE, supE):
        newG = {}
        for v in graph:
            newG[v] = []
            for u, w in graph[v]:
                newG[v].append(u)
        d = INF
        ansG = defaultdict(list)
        K = min(TE.values())
        while self.connected(graph, Q):
            distG = self.COMPUTEDIST(graph, Q)
            maxdistG = max(distG.values())
            if maxdistG == 0: break
            if maxdistG < d:
                d = maxdistG
                ansG = copy.deepcopy(graph)
            L = {x for x in distG.keys() if distG[x] >= d}
            graph = self.MAINTAINKTRUSS(graph, L, K, copy.copy(supE))
        return ansG

    def prepareforq(self, Q, graph):
        flag = {v: 1 for v in Q if graph.get(v) is None}
        for v in flag: Q.remove(v)
        newG = {v: [(u, 1) for u in graph[v]] for v in graph}
        label = defaultdict(int)
        color = 1
        for v in Q:
            if not label[v]:
                self.dfs(v, newG, color, label)
                color += 1
        maxlabel = Counter(label.values()).most_common(1)[0][0]
        newQ = [q for q in Q if label[q] == maxlabel]
        return newQ

    def LCTC_MAIN(self, graph, szLimit, Q):

        # print("len of graph",len(graph))
        # self.supE,self.TE = self.EDGETRUSS(graph)
        nowtime = time.time()
        nowQ = self.prepareforq(Q, graph)
        print("prepare for q", time.time() - nowtime)
        nowtime = time.time()
        supE, TE = self.supE, self.TE
        steiner = STEINER(TE, graph, nowQ)
        print("steiner time", time.time() - nowtime)
        nowtime = time.time()
        # print("len of steiner",len(steiner.G))
        if steiner.G is None or len(steiner.G) == 0: return list(Q)
        G0 = self.FINDG0(steiner.G, graph, nowQ, szLimit, TE)
        print("findG0 time", time.time() - nowtime)
        nowtime = time.time()
        # print("len of G0",len(G0))
        ansG = self.BUILKDELETE(G0, nowQ, self.TE, self.supE)
        print("BULK time", time.time() - nowtime)
        # print("len of ansg",len(ansG))
        ansg = list(set(list(ansG.keys())) | set(Q))
        return ansg

    ### STEP3 结果评估 ###
    def F1Score(self, GMembers, SearchedMembers):
        samen = 0
        for i in GMembers:
            if i in SearchedMembers:
                samen = samen + 1
        precision = samen * 1.0 / len(SearchedMembers)
        recall = samen * 1.0 / len(GMembers)
        Fscore = 2 * precision * recall / (precision + recall)
        return [precision, recall, Fscore]

    def main(self):
        starttime = time.time()
        results = {
            'allscore': 0,
            'allprecision': 0,
            'allrecall': 0,
            'allmemberlen': 0
        }
        graph = {v: self.tempt_nodes_information[v][0] for v in self.tempt_nodes_information}
        self.supE, self.TE = self.EDGETRUSS(graph)
        print('supE/TE built')
        for i in range(0, len(self.ExperimentalDataList)):
            print("rk {} of {}".format(i, len(self.ExperimentalDataList)))
            TestData = self.ExperimentalDataList[i]
            group_name = TestData[0]
            QVlist = TestData[1]
            QAlist = TestData[2]
            GMembers = self.graph_information['Groups'][group_name][0]
            SearchedMembers = self.LCTC_MAIN(graph, 1000, QVlist)
            [precision, recall, score] = self.F1Score(GMembers, SearchedMembers)
            results['allscore'] = results['allscore'] + score
            results['allprecision'] = results['allprecision'] + precision
            results['allrecall'] = results['allrecall'] + recall
            results['allmemberlen'] = results['allmemberlen'] + len(GMembers)
        endtime = time.time()
        duration = endtime - starttime
        if len(self.ExperimentalDataList) == 0:
            resultS = -1
            resultP = -1
            resultR = -1
            averagelen = -1
            TimeEvaluation = -1
        else:
            resultS = results['allscore'] * 1.0 / len(self.ExperimentalDataList)
            resultP = results['allprecision'] * 1.0 / len(self.ExperimentalDataList)
            resultR = results['allrecall'] * 1.0 / len(self.ExperimentalDataList)
            averagelen = results['allmemberlen'] * 1.0 / len(self.ExperimentalDataList)
            TimeEvaluation = duration * 1.0 / len(self.ExperimentalDataList) / averagelen
        return [resultS, resultP, resultR, duration, TimeEvaluation]


def readData():
    f = open("data.txt")
    graph = {}
    while True:
        line = f.readline()
        if len(line) == 0: break
        strs = line.strip().split()
        graph[strs[0]] = strs[1:]
    return graph


if __name__ == "__main__":
    # graph, szLimit, Q = readData()
    # G = CS.tempt_nodes_information
    # graph = {v: G[v][0] for v in G.keys()}
    # x = 0
    # group = CS.graph_information['Groups']['student']
    # Q = ['http://www.cs.cornell.edu/info/people/nikos/nikos.html', 'http://www.cs.cornell.edu/info/people/ghias/home.html', 'http://www.cs.cornell.edu/info/people/yminsky/yminsky.html', 'http://www.cs.cornell.edu/info/people/whkao/whkao.html', 'http://cam.cornell.edu/ph/index.html']
    graph = readData()
    lctc = LCTCSearch(1, 2, 3)
    print(LCTCSearch.LCTC_MAIN(lctc, graph, 1000, ['q1', 'q2', 'q3']))
    # print(CS.graph_information)
