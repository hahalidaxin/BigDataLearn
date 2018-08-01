import os
import sys
import copy
import queue
from collections import defaultdict
import random
import time


# 添加了anchor属性的并查集 # 算法中定义的第一个辅助类
class AFU:
    class node:
        def __init__(self, parent, anchor):
            self.parent, self.anchor = parent, anchor
            self.rank = 0

    def __init__(self):
        self.NS = defaultdict(self.node)

    def MAKESET(self, x):
        self.NS[x] = self.node(-1, x)

    def find(self, x):
        if x.parent == -1:
            return x
        else:
            return self.find(x.parent)

    def FIND(self, x):
        return self.find(self.NS[x])

    def UNION(self, x, y):
        xRoot = self.FIND(x)
        yRoot = self.FIND(y)
        if xRoot == yRoot: return
        if xRoot.rank < yRoot.rank:
            xRoot.parent = yRoot
        elif xRoot.rank > yRoot.rank:
            yRoot.parent = xRoot
        else:
            yRoot.parent = xRoot
            xRoot.rank += 1

    def UPDATEANCHOR(self, x, coreG, y):
        xRoot = self.find(x)
        if (coreG[xRoot.anchor] > coreG[y]):
            xRoot.anchor = y


# 算法中定义的第二个辅助类
class CL_TREE:
    class treenode:
        def __init__(self, coreNum, vertexSet, property):
            self.coreNum = coreNum
            self.vertexSet = vertexSet
            self.invertedList = defaultdict(set)  # property ->List of Vertex owing the property
            self.childList = []
            for v in vertexSet:
                for p in property[v]:
                    self.invertedList[p].add(v)

    def __init__(self, graph, property):
        self.root = self.BUILDINDEX(graph, property)

    # 构建CL-Tree
    @classmethod
    def dfs(cls, v, label, graph, rank):
        que = queue.Queue()
        que.put(v)
        label[v] = rank
        while not que.empty():
            v = que.get()
            for u in graph[v]:
                if not label[u]:
                    label[u] = rank
                    que.put(u)

    def ConnectedComponents(self, newG):
        label = defaultdict(int)
        rank = 1
        for v in newG.keys():
            if not label[v]:
                CL_TREE.dfs(v, label, newG, rank)
                rank += 1
        return label

    # 分解法求解coreG数组
    def CORES(self, graph):
        bin, deg, pos, vert = {}, {}, {}, {}
        md = 0
        for v in graph.keys():
            deg[v] = graph[v].__len__()
            if deg[v] > md: md = deg[v]
        for d in range(0, md + 1): bin[d] = 0
        for v in graph.keys(): bin[deg[v]] += 1
        start = 1
        for d in range(0, md + 1):
            num = bin[d]
            bin[d] = start
            start += num
        for v in graph.keys():
            pos[v] = bin[deg[v]]
            vert[pos[v]] = v
            bin[deg[v]] += 1
        for d in range(md, 0, -1):
            bin[d] = bin[d - 1]
        bin[0] = 1
        for i in range(1, len(vert) + 1):
            v = vert[i]
            for u in graph[v]:
                if deg[u] > deg[v]:
                    du = deg[u]
                    pu = pos[u]
                    pw = bin[du]
                    w = vert[pw]
                    if u != w:
                        pos[u] = pw
                        pos[w] = pu
                        vert[pu] = w
                        vert[pw] = u
                    bin[du] += 1
                    deg[u] -= 1
        return deg

    def buildSubgraph(self, graph, vertices):
        newG = defaultdict(list)
        flagv = {v: 1 for v in vertices}
        for v in vertices:
            newG[v] = [u for u in graph[v] if u in flagv]
        return newG

    def BUILDINDEX(self, graph, property):
        self.property = property
        afu = AFU()
        for v in graph.keys(): afu.MAKESET(v)
        coreG = self.coreG = self.CORES(graph)
        V = defaultdict(set)
        kmax = 0
        for v in graph.keys():
            V[coreG[v]].add(v)
            kmax = max(kmax, coreG[v])
        k, map, flag = kmax, {}, defaultdict(int)
        while k >= 0:
            tV = set()
            for v in V[k]:
                tV.add(afu.FIND(v))
                flag[v] = 1
            newG = self.buildSubgraph(graph, list(flag.keys()))
            label = self.ConnectedComponents(newG)
            compo = defaultdict(list)
            for v in label:
                if v in V[k]: compo[label[v]].append(v)
            for i in compo:
                Pi = self.treenode(k, set(compo[i]), property)
                for v in compo[i]:
                    map[v] = Pi
                    for u in graph[v]:
                        if coreG[u] >= coreG[v]:
                            afu.UNION(u, v)
                        if coreG[u] > coreG[v]:
                            uRoot = afu.FIND(u)
                            uAnchor = uRoot.anchor
                            pt = map.get(uAnchor)
                            if not pt is None:
                                Pi.childList.append(pt)
                        # 基于Vk的每个连通子集进行操作
                    vRoot = afu.FIND(v)
                    if coreG[vRoot.anchor] > coreG[v]:
                        afu.UPDATEANCHOR(vRoot, coreG, v)
            k -= 1
        minCore = min(coreG[v] for v in graph if (coreG[v]))
        root = self.treenode(0, {v for v in graph if not coreG[v]}, property)
        root.childList = list({map[afu.FIND(v).anchor] for v in graph if coreG[v] == minCore})
        return root

    def findR(self, root, q, end, top, ans):
        flag = defaultdict(int)
        self.tFindR(root, flag, q, end, top, ans)

    def tFindR(self, root, flag, q, end, top, ans):
        flag[root] = 1
        if q in root.vertexSet:
            ans[root.coreNum] = root
            return True
        for v in root.childList:
            if not flag[v]:
                resBool = self.tFindR(v, flag, q, end, top, ans)
                if (resBool and end <= root.coreNum <= top):
                    ans[root.coreNum] = root
                if (resBool): return True
        return False

    def tfindGst(self, rt, St, flag):
        flag[rt] = 1
        ff = 0
        s = set()
        for prop in St:
            if ff == 0:
                ff = 1
                s = rt.invertedList[prop]
            else:
                s = s & rt.invertedList[prop]
        self.ansGst |= s
        for v in rt.childList:
            if not flag[v]:
                self.tfindGst(v, St, flag)

    def findGSt(self, G, R, St, c, q):
        flag = defaultdict(int)
        self.ansGst = set()
        self.tfindGst(R[c], St, flag)
        newG = self.buildSubgraph(G, self.ansGst)
        label = defaultdict(int)
        color = 1
        for v in self.ansGst:
            if not label[v]:
                CL_TREE.dfs(v, label, newG, color)
                color += 1
        return [v for v in newG.keys() if label[v] == label[q]]


# 主算法定义类
class ACCSearch:
    def __init__(self, graph_information, tempt_nodes_information, ExperimentalDataList):
        self.graph_information = graph_information
        self.tempt_nodes_information = tempt_nodes_information
        self.ExperimentalDataList = ExperimentalDataList
        return

    # 分解法求解coreG数组
    def CORES(self, graph):
        bin, deg, pos, vert = {}, {}, {}, {}
        md = 0
        for v in graph.keys():
            deg[v] = graph[v].__len__()
            if (deg[v] > md): md = deg[v]
        for d in range(0, md + 1): bin[d] = 0
        for v in graph.keys(): bin[deg[v]] += 1
        start = 1
        for d in range(0, md + 1):
            num = bin[d]
            bin[d] = start
            start += num
        for v in graph.keys():
            pos[v] = bin[deg[v]]
            vert[pos[v]] = v
            bin[deg[v]] += 1
        for d in range(md, 0, -1):
            bin[d] = bin[d - 1]
        bin[0] = 1
        for i in range(1, len(vert) + 1):
            v = vert[i]
            for u in graph[v]:
                if deg[u] > deg[v]:
                    du = deg[u]
                    pu = pos[u]
                    pw = bin[du]
                    w = vert[pw]
                    if u != w:
                        pos[u] = pw
                        pos[w] = pu
                        vert[pu] = w
                        vert[pw] = u
                    bin[du] += 1
                    deg[u] -= 1
        return deg

    def buildSubgraph(self, graph, vertices):
        flagv = {v: 1 for v in vertices}
        newG = {}
        for v in vertices:
            newG[v] = [u for u in graph[v] if u in flagv]
        return newG

    def findcoreGkExist(self, graph, k, q):
        coreG = self.CORES(graph)
        flagv = defaultdict(int)
        newG = defaultdict(list)
        for v in graph.keys():
            if coreG[v] >= k: flagv[v] = 1
        for v in list(flagv.keys()):
            for u in graph[v]:
                if flagv[u] == 1:
                    newG[v].append(u)
        label = defaultdict(int)
        color, cnt = 1, 0
        for v in newG.keys():
            if not label[v]:
                CL_TREE.dfs(v, label, newG, color)
                color += 1
        ls = [v for v in newG.keys() if label[v] == label[q]]
        if len(ls) < k:
            return -1, []
        else:
            newG = self.buildSubgraph(newG, ls)
            coreGk = min(self.CORES(newG).values())
            return coreGk if coreGk >= k else -1, ls

    def test_s(self, s, posy):
        ls = list(s)
        for i in range(len(ls)):
            ts = set(ls[:i] + ls[i + 1:])
            if not ts in posy:
                return False
        return True

    # 主算法 Inc-S算法 递增序、空间友好的算法
    def INCS(self, G, Property, cltree, q, k, S):
        # x寻找一条路径，这条路径上包含有q节点，而且满足路径上节点的coreG位于[end,top]之间
        k = min(cltree.coreG[q], k)
        R = {}
        cltree.findR(cltree.root, q, k, cltree.coreG[q], R)
        l = 0
        FAI = []
        for p in S:
            stt = set()
            stt.add(p)
            if Property[q].count(p): FAI.append((stt, k))
        POSY = defaultdict(list)
        cMax = cltree.coreG[q]
        while True:
            l += 1
            for St, c in FAI:
                if c > cMax: c = cMax
                while (R.get(c) is None) and c <= cMax: c += 1
                if c > cMax or R.get(c) is None: continue

                GS = list(cltree.findGSt(G, R, St, c, q))
                newG = self.buildSubgraph(G, GS)
                m, n = 0, newG.keys().__len__()
                m = (sum(newG[v].__len__() for v in newG.keys())) / 2
                if not (m - n < ((k ** 2 - k) / 2 - 1)):
                    coreGk, ls = self.findcoreGkExist(newG, k, q)
                    if coreGk >= k: POSY[l].append((St, coreGk))

            if POSY[l].__len__():
                FAI = []
                posi = POSY[l]
                for i in range(posi.__len__()):
                    si, corei = posi[i]
                    for j in range(i + 1, posi.__len__()):
                        sj, corej = posi[j]
                        if len(si) == len(sj):
                            st = si | sj
                            if len(st) == len(si) + 1:
                                # 这里没有利用lemma1进行剪枝
                                tposy = [x[0] for x in posi]
                                if self.test_s(st, tposy):
                                    c = max(corei, corej)
                                    if not (st, c) in FAI:
                                        FAI.append((st, c))
            else:
                break
        if POSY.get(l - 1) is None: return []  # 没有找到符合要求的群组
        # print("l: ", l)
        # print("POSY: ", POSY[l-1])
        # 在这里进行了选择，永远选择第一个构造答案
        maxcoreg = 0, 0
        for i, (S, c) in enumerate(POSY[l - 1]):
            while c <= cMax and R.get(c) is None: c += 1
            if c <= cMax and not R.get(c) is None:
                ls = cltree.findGSt(G, R, S, c, q)
                coreg = min(self.CORES(self.buildSubgraph(G, ls)).values())
                if coreg > maxcoreg[0]:
                    maxcoreg = coreg, i
        S, c = POSY[l - 1][maxcoreg[1]]
        if c == 0:
            return []
        else:
            while c <= cMax and R.get(c) is None: c += 1
            if c <= cMax and not R.get(c) is None:
                return cltree.findGSt(G, R, S, c, q)
            else:
                return []

    def ACC_MAIN(self, graph, property, q, k, S):
        S = list(set(S) & set(property[q]))
        if len(S) == 0:
            S = set(random.sample(property[q], min(5, len(property[q]))))
        # print(property['193'])
        ans = self.INCS(graph, property, self.cltree, q, k, S)
        if not q in ans: ans.append(q)
        return ans

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
        graph = {v: self.tempt_nodes_information[v][0] for v in self.tempt_nodes_information.keys()}
        property = {v: self.tempt_nodes_information[v][1] for v in self.tempt_nodes_information.keys()}
        starttime = time.time()
        results = {
            'allscore': 0,
            'allprecision': 0,
            'allrecall': 0,
            'allmemberlen': 0
        }
        self.cltree = CL_TREE(graph, property)
        print('cltree built')
        for i in range(0, len(self.ExperimentalDataList)):
            print("rk {} of {}".format(i, len(self.ExperimentalDataList)))
            TestData = self.ExperimentalDataList[i]
            group_name = TestData[0]
            QVlist = TestData[1]
            QAlist = TestData[2]
            GMembers = self.graph_information['Groups'][group_name][0]
            attriNum = sum(len(property[v]) for v in property)
            SearchedMembers = self.ACC_MAIN(graph, property, QVlist[0], 6, QAlist)
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


''''
if __name__ == "__main__":
    G = CS.tempt_nodes_information
    graph = {v: G[v][0] for v in G.keys()}
    property = {v: G[v][1] for v in G.keys()}
    cltree = CL_TREE(graph, property)
    group = CS.graph_information['Groups']['circle0']
    print(ACC_MAIN(graph, property, '193', 6, [93]))
    '''
