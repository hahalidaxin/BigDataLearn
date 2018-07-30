import random
import copy
import queue
from collections import defaultdict
from collections import Counter
import sys
import time
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
        distG, inq, s = {}, {}, {}
        father = {}
        self.maxTruss = maxTruss = max(self.TE.values())
        self.minTruss = minTruss = defaultdict(int)

        for v in graph.keys():
            distG[v] = self.INF
            minTruss[v] = maxTruss

        que = queue.Queue()
        for q in Q:
            father[q] = q
            que.put(q)
            distG[q], inq[q] = 0, 1
            s[q] = q
        while not que.empty():
            u = que.get()
            inq[u] = 0
            if graph.get(u) is None: continue
            for v in graph[u]:
                tmpminTruss = min(self.TE[self.cedge(u, v)], minTruss[v])
                if distG[u] + self.factor * (maxTruss - tmpminTruss) < distG[v]:
                    distG[v] = distG[u] + 1
                    father[v] = u
                    s[v] = s[u]
                    minTruss[v] = tmpminTruss
                    if inq.get(v) is None or not inq[v]:
                        que.put(v)
                        inq[v] = 1
        return s, distG, father

    def find(self, x, fa):
        if (x == fa[x]):
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
                if (u < v):
                    edges.append((u, v, w))
        edges = sorted(edges, key=lambda x: (x[2], x[0], x[1]))
        for u, v, w in edges:
            x, y = self.find(u, fa), self.find(v, fa)
            if (x != y):
                fa[x] = y
                ansG[u].append((v, w))
                ansG[v].append((u, w))
        if len(graph) == 1: ansG[list(graph.keys())[0]] = []
        return ansG

    def EXPAND(self, graph, oriGraph):
        newG = defaultdict(list)
        distG = self.distG
        father = self.father
        distuv = {}
        for v in graph.keys():
            for u, w in graph[v]:
                distuv[self.cedge(u, v)] = w

        for v in self.s.keys():
            if oriGraph.get(v) is None: continue
            for u in oriGraph[v]:
                if (self.s[u] < self.s[v]):
                    dist = distuv.get(self.cedge(self.s[u], self.s[v]))
                    deltadist = self.factor * (
                            self.maxTruss - min([self.TE[self.cedge(u, v)], self.minTruss[u], self.minTruss[v]]))
                    if (not (dist is None) and distG[v] + distG[u] + deltadist == dist):
                        # v->s[v] u->s[u]
                        for x in [u, v]:
                            while (x != father[x]):
                                newG[x].append((father[x], 1))
                                newG[father[x]].append((x, 1))
                                x = father[x]
                        newG[u].append((v, 1))
                        newG[v].append((u, 1))
        if len(graph) == 1: newG[list(graph.keys())[0]] = []
        for v in newG.keys():
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

    def GETG1(self, graph, Q):
        self.s, self.distG, self.father = self.SPFA(graph, Q)
        triList = []
        for u in graph.keys():
            if self.s.get(u) is None:
                graph[u] = None  # 删除不能与Q中节点联通的节点
                continue
            for v in graph[u]:
                if (self.s.get(v) is None): continue
                if (self.s[u] < self.s[v]):
                    deltadist = self.factor * (
                            self.maxTruss - min([self.minTruss[u], self.minTruss[v], self.TE[self.cedge(u, v)]]))
                    triList.append((self.s[u], self.s[v], self.distG[u] + self.distG[v] + deltadist))
        G1 = defaultdict(list)
        triList = sorted(triList, key=lambda x: x)
        for i in range(triList.__len__()):
            u, v, w = triList[i]
            if (i == 0 or (u, v) != triList[i - 1][0:2]):
                G1[u].append((v, w))
                G1[v].append((u, w))
        if len(Q) == 1: G1[Q[0]] = []
        return G1

    def CONSTRUCT(self, graph, Q):
        G1 = self.GETG1(graph, Q)
        # G2 = self.KRUSKAL(G1)
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

class LCTCSearch:
    def __init__(self,graph_information,tempt_nodes_information,ExperimentalDataList):
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
        for u in graph.keys():
            for v in graph[u]:
                e = self.cedge(u, v)
                if 0 == edgeExist[e]:
                    edgeExist[e] = 1
                    if graph.get(v) is None:  # 使用defaultdict的后遗症
                        supE[e] = 0
                    else:
                        supE[e] = len(set(graph[u]) & set(graph[v]))  # 这个地方可能会有点儿慢
        ansSupE = copy.copy(supE)
        # 构造vert 按照sup顺序存储所有的边 其中bin与pos是辅助数组 使得update操作能够在常数时间内完成
        vert = sorted(supE.keys(), key=lambda x: supE[x])
        bin, pos = {}, {}
        last, numEdge = -1, vert.__len__()
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
                for w in graph[u]:
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
        return ansSupE, TE

    def BFSEXTENDG(self, graph, oriGraph, szLimit, TE, kt):
        que = queue.Queue()
        flag = defaultdict(int)
        for v in graph.keys():
            que.put(v)
            flag[v] = 1
        while not que.empty():
            u = que.get()
            for v in oriGraph[u]:
                if TE[self.cedge(u, v)] >= kt:
                    if len(graph.keys()) >= szLimit:
                        return
                    else:
                        if graph[v].count((u, 1)) == 0:
                            graph[v].append((u, 1))
                            graph[u].append((v, 1))
                        if (flag[v] == 0):
                            flag[v] = 1
                            que.put(v)

    def FINDG0(self, graph, oriGraph, Q, szLimit, TE):
        # 返回一个最大的k-truss，使得k-truss包含Q且k最大
        # First 使用truss-decomposition算法计算所有边的trussness
        # 这里接收到的graph是一棵steinertree

        kt = INF
        for v in graph.keys():
            for u, w in graph[v]:
                if (v < u): kt = min(kt, TE[self.cedge(v, u)])
        if len(graph) == 1: kt = 0
        self.BFSEXTENDG(graph, oriGraph, szLimit, TE, kt)

        for v in graph.keys():
            graph[v] = sorted(graph[v], key=lambda x: -TE[self.cedge(x[0], v)])
        k = INF
        for u in graph.keys():
            if len(graph[u]):
                k = min(k, TE[self.cedge(u, graph[u][0][0])])
        '''
        label = defaultdict(int)
        color=1
        for v in graph.keys():
            if not label[v]:
                dfs(v, graph, color, label)
                color += 1

        print("color of Q: ")
        for v in Q:
            print(v,label[v])
        '''
        S = defaultdict(set)
        V, Vedge = set(), set()
        S[k] = set(copy.copy(Q))
        G0 = defaultdict(list)
        while self.connected(G0, Q) is False:
            '''
            if k == 0:
                print("G0 is :", str(G0))
            '''
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
                for u, w in graph[v]:
                    if TE[self.cedge(u, v)] < k:
                        break
                    elif TE[self.cedge(u, v)] < kmax:
                        if not (self.cedge(u, v) in Vedge):
                            Vedge.add(self.cedge(u, v))
                            G0[u].append((v, 1))
                            G0[v].append((u, 1))
                        if not u in S[k]:
                            S[k].add(u)
                            queK.put(u)
                if len(graph[v]):
                    for i,(u,w) in enumerate(graph[v]):
                        if not self.cedge(u,v) in Vedge:
                            break
                    if i < len(graph[v]):
                        l = TE[self.cedge(v, graph[v][i][0])]
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
        while len(S):
            u, v = S.pop()
            Nuv = set(graph[u]) & set(graph[v])
            for w, wx in Nuv:
                e1, e2 = self.cedge(u, w), self.cedge(v, w)
                for ex in [e1, e2]:
                    supE[ex] -= 1
                    if supE[ex] < k - 2 and (not ex in S) and (not flag[ex]):
                        S.add(ex)
            flag[self.cedge(u, v)] = 1
        ansG = defaultdict(list)
        for v in graph.keys():
            if not (v in L):
                ansG[v] = []
                for u, w in graph[v]:
                    if not flag[self.cedge(u, v)]:
                        ansG[v].append((u, 1))
        return ansG

    def COMPUTEDIST(self, graph, Q):
        distG = {}
        flag = defaultdict(int)
        for v in graph.keys(): distG[v] = INF
        que = queue.Queue()
        for v in Q:
            distG[v] = 0
            flag[v] = 1
            que.put(v)
        while (not que.empty()):
            u = que.get()
            for v, w in graph[u]:
                if (distG[v] == INF and flag[v] == 0):
                    distG[v] = distG[u] + 1
                    flag[v] = 1
                    que.put(v)
        return distG

    def BUILKDELETE(self, graph, Q, supE, TE):
        d = INF
        ansG = defaultdict(list)
        K = INF
        for v in graph.keys():
            for u, w in graph[v]:
                K = min(K, TE[self.cedge(u, v)])
        while self.connected(graph, Q):
            distG = self.COMPUTEDIST(graph, Q)
            maxdistG = max(distG.values())
            if maxdistG == 0: break
            if maxdistG < d:
                d = maxdistG
                ansG = copy.copy(graph)
            L = {x for x in distG.keys() if distG[x] >= d}
            graph = self.MAINTAINKTRUSS(graph, L, K, copy.copy(supE))
        return ansG

    def prepareforq(self, Q, graph):
        flag = defaultdict(int)
        for v in Q:
            if graph.get(v) is None:
                flag[v] = 1
        for v in flag.keys():
            Q.remove(v)
        newG = defaultdict(list)
        for v in graph.keys():
            for u in graph[v]:
                newG[v].append((u, 1))
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
        nowQ = self.prepareforq(Q,graph)
        supE, TE = self.supE, self.TE
        steiner = STEINER(copy.copy(TE), copy.deepcopy(graph), nowQ)
        if steiner.G is None or len(steiner.G) == 0: return []
        G0 = self.FINDG0(steiner.G, copy.deepcopy(graph), nowQ, szLimit, copy.copy(TE))
        ansG = self.BUILKDELETE(G0, nowQ, supE, copy.copy(TE))
        ansg = list(ansG.keys())
        for q in Q:
            if not q in ansg:
                ansg.append(q)
        return ansg

    ### STEP3 结果评估 ###
    def F1Score(self,GMembers,SearchedMembers):
        samen = 0
        for i in GMembers:
            if i in SearchedMembers:
                samen = samen + 1
        precision = samen*1.0/len(SearchedMembers)
        recall = samen*1.0/len(GMembers)
        Fscore = 2*precision*recall/(precision+recall)
        return [precision,recall,Fscore]

    def main(self):
        starttime = time.time()
        results = {
                'allscore':0,
                'allprecision':0,
                'allrecall':0,
                'allmemberlen':0
            }
        graph = {v: self.tempt_nodes_information[v][0] for v in self.tempt_nodes_information}
        self.supE, self.TE = self.EDGETRUSS(graph)
        print('supE/TE built')
        for i in range(0,len(self.ExperimentalDataList)):
            print("rk {} of {}".format(i, len(self.ExperimentalDataList)))
            TestData = self.ExperimentalDataList[i]
            group_name = TestData[0]
            QVlist = TestData[1]
            QAlist = TestData[2]
            GMembers = self.graph_information['Groups'][group_name][0]
            SearchedMembers = self.LCTC_MAIN(graph,1000,QVlist)
            [precision,recall,score] = self.F1Score(GMembers,SearchedMembers)
            results['allscore'] = results['allscore'] + score
            results['allprecision'] = results['allprecision'] + precision
            results['allrecall'] = results['allrecall'] + recall
            results['allmemberlen'] = results['allmemberlen'] + len(GMembers)
        endtime = time.time()
        duration = endtime-starttime
        if len(self.ExperimentalDataList) == 0:
            resultS = -1
            resultP = -1
            resultR = -1
            averagelen = -1
            TimeEvaluation = -1
        else:
            resultS = results['allscore']*1.0/len(self.ExperimentalDataList)
            resultP = results['allprecision']*1.0/len(self.ExperimentalDataList)
            resultR = results['allrecall']*1.0/len(self.ExperimentalDataList)
            averagelen = results['allmemberlen']*1.0/len(self.ExperimentalDataList)
            TimeEvaluation = duration*1.0/len(self.ExperimentalDataList)/averagelen
        return [resultS,resultP,resultR,duration,TimeEvaluation]



'''
if __name__ == "__main__":
    # graph, szLimit, Q = readData()
    G = CS.tempt_nodes_information
    graph = {v: G[v][0] for v in G.keys()}
    x = 0
    group = CS.graph_information['Groups']['student']
    Q = ['http://www.cs.cornell.edu/info/people/nikos/nikos.html', 'http://www.cs.cornell.edu/info/people/ghias/home.html', 'http://www.cs.cornell.edu/info/people/yminsky/yminsky.html', 'http://www.cs.cornell.edu/info/people/whkao/whkao.html', 'http://cam.cornell.edu/ph/index.html']
    print(LCTC_MAIN(graph,1000,Q))
    # print(CS.graph_information)
'''

