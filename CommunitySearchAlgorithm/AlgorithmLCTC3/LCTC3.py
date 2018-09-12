import copy
import queue
from collections import Counter
import sys
import time
from . import SortAlgorithm
# import CommunitySearch as CS

INF = float('inf')


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
        self.minTruss = minTruss = {}

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
        print(" \t\t spfa time",time.time()-nowtime)
        nowtime = time.time()
        triList = []
        for u in graph:
            for v in graph[u]:
                if self.s.get(v) is None: continue
                if self.s[u] < self.s[v]:
                    deltadist = self.factor * (
                            self.maxTruss - min([self.minTruss[u], self.minTruss[v], self.TE[self.cedge(u, v)]]))
                    triList.append((self.s[u], self.s[v], self.distTruss[u] + self.distTruss[v] + deltadist, (u, v)))
        G1 = {}
        triList.sort()
        print(' \t\t sortime',time.time()-nowtime)
        mediumTurple = {}
        for i in range(len(triList)):
            su, sv, w, (u, v) = triList[i]
            if i == 0 or (su, sv) != triList[i - 1][0:2]:
                if G1.get(su) is None: G1[su]=[]
                if G1.get(sv) is None: G1[sv]=[]
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
        ansG = {}
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
                if ansG.get(u) is None: ansG[u] = []
                if ansG.get(v) is None: ansG[v] = []
                ansG[u].append((v, w))
                ansG[v].append((u, w))
        if len(graph) == 1: ansG[list(graph.keys())[0]] = []
        return ansG

    def EXPAND(self, graph):
        newG = {}
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
                    if newG.get(x) is None: newG[x] = []
                    if newG.get(father[x]) is None: newG[father[x]] = []
                    newG[x].append((father[x], tmpdist))
                    newG[father[x]].append((x, tmpdist))
                    x = father[x]
            tmpdist = 1 + self.factor * (self.maxTruss - self.TE[self.cedge(u, v)])
            if newG.get(u) is None: newG[u] = []
            if newG.get(v) is None: newG[v] = []
            newG[u].append((v, tmpdist))
            newG[v].append((u, tmpdist))
        if len(graph) == 1: newG[list(graph.keys())[0]] = []
        for v in newG:
            newG[v] = {}.fromkeys(newG[v]).keys()  # ȥ���ظ��ı�
        return newG

    def DELETELEAF(self, graph, Q):
        flag = {}
        for v in graph.keys():
            flag[v] = 0 if (graph[v].__len__() == 1 and not (v in Q)) else 1
        newG = {}
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


class LCTC3Search:
    def __init__(self, graph_information, tempt_nodes_information, ExperimentalDataList):
        self.graph_information = graph_information
        self.tempt_nodes_information = tempt_nodes_information
        self.ExperimentalDataList = ExperimentalDataList
        return

    def cedge(self, u, v):
        return min(u, v), max(u, v)

    def EDGETRUSS(self, graph):
        # ����Improved Truss Decomposition�㷨 ����grapn��ÿ���ߵ�trussness
        supE = {}
        edgeExist = {}
        nowtime = time.time()
        for u in graph:
            for v in graph[u]:
                e = self.cedge(u, v)
                if edgeExist.get(e) is None:
                    edgeExist[e] = 1
                    # supE[e] = len(set(graph[u])&set(graph[v]))
        cedge = self.cedge
        for u, v in edgeExist:
            if supE.get((u, v)) is None: supE[(u, v)] = 0
            if len(graph[u]) > len(graph[u]):
                u, v = v, u
            for w in graph[u]:
                if edgeExist.get(cedge(u, w)) is not None and edgeExist.get(cedge(v, w)) is not None:
                    supE[cedge(u, v)] = supE.get(cedge(u, v), 0) + 1
                    supE[cedge(u, w)] = supE.get(cedge(u, w), 0) + 1
                    supE[cedge(v, w)] = supE.get(cedge(v, w), 0) + 1
        for e in edgeExist:
            supE[e]=int(supE[e]/3)
        ansSupE = copy.copy(supE)
        # ����vert ����sup˳��洢���еı� ����bin��pos�Ǹ������� ʹ��update�����ܹ��ڳ���ʱ�������
        vert = SortAlgorithm.bulksort(list(supE.keys()),func = lambda x: supE[x])
        print(" \t\t intersection time", time.time() - nowtime)
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
        TE = {}
        while numEdge:
            while lowestSup < tmpNumEdge and supE[vert[lowestSup]] <= k - 2:
                u, v = e = vert[lowestSup]
                x = u if len(graph[u]) < len(graph[v]) else v
                for w in graph[x]:
                    e1 = self.cedge(v, w)
                    e2 = self.cedge(u, w)
                    if (edgeExist.get(e1) is not None and edgeExist[e1]==1) and (edgeExist.get(e2) is not None and edgeExist[e2]==1):
                        # ά��vert �ı���������vert�е�λ��
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
        print(" \t\t else time", time.time() - nowtime)
        return ansSupE, TE

    def BFSEXTENDG(self, graph, oriGraph, szLimit, TE):
        kt = INF
        for v in graph.keys():
            for u, w in graph[v]:
                if v < u: kt = min(kt, TE[self.cedge(v, u)])
        if len(graph) == 1: kt = 0
        que = queue.Queue()
        flag = {}
        for v in graph:
            flag[v]=0
        for v in graph.keys():
            que.put(v)
            flag[v] = 1
        flagedge = {}
        while not que.empty() and len(graph) < szLimit:
            u = que.get()
            for v in oriGraph[u]:
                if TE[self.cedge(u, v)] >= kt:
                    if len(graph) >= szLimit:
                        break
                    else:
                        if flagedge.get(self.cedge(u, v)) is None:
                            if graph.get(v) is None: graph[v] = []
                            if graph.get(u) is None: graph[u] = []
                            graph[v].append((u, 1))
                            graph[u].append((v, 1))
                            flagedge[self.cedge(u, v)] = 1
                        if flag.get(v) is None:
                            flag[v] = 1
                            que.put(v)
        vertices = list(flag.keys())
        for v in vertices:
            for u in oriGraph[v]:
                if (flag.get(u) is not None and flag[u]) and flagedge.get(self.cedge(u, v)) is None:
                    graph[v].append((u, 1))

    def FINDG0(self, graph, oriGraph, Q, szLimit, TE):
        # ����һ������k-truss��ʹ��k-truss����Q��k���
        # First ʹ��truss-decomposition�㷨�������бߵ�trussness
        # ������յ���graph��һ��steinertree
        nowtime = time.time()
        self.BFSEXTENDG(graph, oriGraph, szLimit, TE)
        newG = {v: [e[0] for e in graph[v]] for v in graph}
        print(' \t\t sort time', time.time() - nowtime)
        # �������� ���ʱ��̫�����Կ���ʹ��Ͱ����
        for v in graph:
            graph[v].sort(key=lambda x: -TE[self.cedge(x[0], v)])
        k = min(TE[self.cedge(u, graph[u][0][0])] for u in Q)
        S = {}
        V, Vedge = set(), set()
        S[k] = set(Q)
        G0 = {}
        indexte = {v: 0 for v in graph}
        cnt = 0
        # print("k of this time ",k)
        while self.connected(G0, Q) is False:
            cnt += 1
            queK = queue.Queue()
            if k not in S.keys():
                S[k] = set()
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
                            if G0.get(u) is None: G0[u] = []
                            if G0.get(v) is None: G0[v] = []
                            G0[u].append((v, 1))
                            G0[v].append((u, 1))
                        if not u in S[k]:
                            S[k].add(u)
                            queK.put(u)
                    indexte[v] += 1
                if not indexte[v] == len(graph[v]):
                    l = TE[self.cedge(v, graph[v][indexte[v]][0])]
                    if S.get(l) is None: S[l]=set()
                    S[l].add(v)
            k -= 1
        return G0

    def dfs(self, v, graph, color, flag):
        que = queue.Queue()
        que.put(v)
        flag[v] = color
        cnt=0
        while not que.empty():
            v = que.get()
            cnt+=1
            if graph.get(v) is None: continue
            for u, w in graph[v]:
                if flag.get(u) is None:
                    flag[u] = color
                    que.put(u)

    def connected(self, graph, Q):
        if len(graph) == 0: return False
        flag = {}
        color, count = 1, 0
        for v in Q:
            if flag.get(v) is None:
                count += 1
                if count >= 2: break
                self.dfs(v, graph, color, flag)
                color += 1
        if len(graph) == 0: return False
        return True if count == 1 else False

    def MAINTAINKTRUSS(self, graph, L, k, supE,Q):
        S = set()
        flag = {}
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
                    if supE[ex] < k - 2 and not ex in S and flag.get(ex) is None:
                        S.add(ex)
            flag[self.cedge(u, v)] = 1
        ansG = {}
        for v in graph.keys():
            if not v in L:
                ansG[v] = []
                for u, w in graph[v]:
                    if flag.get(self.cedge(u, v)) is None:
                        ansG[v].append((u, 1))
        return ansG

    def COMPUTEDIST(self, graph, Q):
        ansdistG = {}
        for v in graph.keys(): ansdistG[v] = -INF
        for q in Q:
            distG = {}
            flag = {}
            que = queue.Queue()
            distG[q] = 0
            flag[q] = 1
            que.put(q)
            while not que.empty():
                u = que.get()
                for v, w in graph[u]:
                    if flag.get(v) is None:
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
        ansG = {}
        K = min(TE.values())
        while self.connected(graph, Q):
            for q in Q:
                if not q in graph:
                    break
            distG = self.COMPUTEDIST(graph, Q)
            maxdistG = max(distG.values())
            if maxdistG == 0: break
            if maxdistG < d:
                d = maxdistG
                ansG = copy.deepcopy(graph)
            L = {x for x in distG.keys() if distG[x] >= d}
            graph = self.MAINTAINKTRUSS(graph, L, K, copy.copy(supE),Q)
        return ansG

    def prepareforq(self, Q, graph):
        flag = {v: 1 for v in Q if graph.get(v) is None}
        for v in flag: Q.remove(v)
        newG = {v: [(u, 1) for u in graph[v]] for v in graph}
        label = {}
        color = 1
        for v in Q:
            if label.get(v) is None:
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
        print(" \t\t prepare for q", time.time() - nowtime)
        nowtime = time.time()
        supE, TE = self.supE, self.TE
        steiner = STEINER(TE, graph, nowQ)
        print(" \t\t steiner time", time.time() - nowtime)
        nowtime = time.time()
        # print("len of steiner",len(steiner.G))
        if steiner.G is None or len(steiner.G) == 0: return list(Q)
        G0 = self.FINDG0(steiner.G, graph, nowQ, szLimit, TE)
        print(" \t\t findG0 time", time.time() - nowtime)
        nowtime = time.time()
        # print("len of G0",len(G0))
        ansG = self.BUILKDELETE(G0, nowQ, self.TE, self.supE)
        print(" \t\t BULK time", time.time() - nowtime)
        # print("len of ansg",len(ansG))
        ansg = list(set(list(ansG.keys())) | set(Q))
        return ansg

    ### STEP3 ������� ###
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
        bstarttime = time.time()
        self.supE, self.TE = self.EDGETRUSS(graph)
        bendtime = time.time()
        addedtime = bendtime - bstarttime
        print(' \t\t supE/TE built')
        for i in range(0, len(self.ExperimentalDataList)):
            print(" \t\t rk {} of {}".format(i, len(self.ExperimentalDataList)))
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
        build_duration = addedtime
        query_duration = duration - build_duration
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
            TimeEvaluation = query_duration * 1.0 / len(self.ExperimentalDataList) / averagelen
        return [resultS, resultP, resultR, duration, build_duration, query_duration, TimeEvaluation]


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
