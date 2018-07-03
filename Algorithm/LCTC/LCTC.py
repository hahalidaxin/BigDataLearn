import os
import copy
import queue
from collections import defaultdict

INF = 9999999

def cedge(u,v):
    return (min(u,v),max(u,v))
def EDGETRUSS(graph):
    #利用Improved Truss Decomposition算法 计算grapn中每条边的trussness
    supE = defaultdict(int)
    edgeExist = defaultdict(int)
    for u in graph.keys():
        for v in graph[u]:
            e = cedge(u,v)
            if(edgeExist[e]==0):
                edgeExist[e]=1
                supE[e] = len(set(graph[u])&set(graph[v]))         #这个地方可能会有点儿慢
    ansSupE = copy.copy(supE)
    #构造vert 按照sup顺序存储所有的边 其中bin与pos是辅助数组 使得update操作能够在常数时间内完成
    vert = sorted(supE.keys(),key=lambda x:supE[x])
    bin,pos = {},{}
    last,numEdge=-1,vert.__len__()
    for i in range(numEdge):
        pos[vert[i]] = i
        if(supE[vert[i]] != last):
            bin[supE[vert[i]]]=i
            last=supE[vert[i]]
    k,lowestSup = 2,0
    tmpNumEdge = numEdge
    TE = defaultdict(int)
    while(numEdge):
        while(lowestSup<tmpNumEdge and supE[vert[lowestSup]]<=k-2):
            u,v = e = vert[lowestSup]
            for w in graph[u]:
                e1 = cedge(v,w)
                e2 = cedge(u,w)
                if(edgeExist[e1] and edgeExist[e2]):
                    #维护vert 改变两条边在vert中的位置
                    for ex in [e1,e2]:
                        pw = max(bin[supE[ex]],lowestSup+1)
                        pu = pos[ex]
                        fe = vert[pw]
                        if(fe!=ex):
                            pos[ex]=pw
                            pos[fe]=pu
                            vert[pw]=ex
                            vert[pu]=fe
                        bin[supE[ex]]+=1
                        if (bin.get(supE[ex]-1) is None):
                            bin[supE[ex]-1]=pos[ex]
                        supE[ex]-=1
            TE[e]=k
            edgeExist[e]=0
            numEdge-=1
            if(numEdge==0) : break
            lowestSup += 1
        k+=1
    return ansSupE,TE

class STEINER :
    def __init__(self,TE,graph,Q):
        self.factor = 3
        self.INF = INF
        self.TE = TE
        self.G = self.CONSTRUCT(graph,Q)

    def SPFA(self,graph,Q):
        distG,inq,s= {},{},{}
        father = {}
        self.maxTruss  = maxTruss = max(self.TE.values())
        self.minTruss = minTruss = {}

        for v in graph.keys():
            distG[v] = self.INF
            minTruss[v]=maxTruss

        que = queue.Queue()
        for q in Q:
            father[q]=q
            que.put(q)
            distG[q], inq[q] = 0,1
            s[q] = q
        while(not que.empty()):
            u = que.get()
            inq[u]=0
            for v in graph[u]:
                print(self.TE[cedge(u,v)],minTruss[v])
                tmpminTruss = min(self.TE[cedge(u,v)],minTruss[v])
                if(distG[u]+self.factor*(maxTruss-tmpminTruss)<distG[v]):                #此处有待修改
                    distG[v]=distG[u]+1
                    father[v]=u
                    s[v]=s[u]
                    minTruss=tmpminTruss
                    que.put(v)
                    inq[v]=1
        return s,distG,father
    def find(self,x,fa):
        if(x==fa[x]) :return x
        else :
            fa[x]=self.find(fa[x],fa)
            return fa[x]
    def KRUSKAL(self,graph):
        edges,fa=[],{}
        ansG = defaultdict(list)
        for u in graph.keys():
            fa[u]=u
            for v,w in graph[u]:
                if(u<v):
                    edges.append((u,v,w))
        edges = sorted(edges,key=lambda x:(x[2],x[0],x[1]))
        for u,v,w in edges:
            x , y = self.find(u,fa),self.find(v,fa)
            if(x!=y) :
                fa[x]=y
                ansG[u].append((v,w))
                ansG[v].append((u,w))
        return ansG

    def EXPAND(self,graph,oriGraph):
        newG = defaultdict(list)
        distG = self.distG
        father = self.father
        distuv = {}
        for v in graph.keys():
            for u,w in graph[v]:
                distuv[cedge(u,v)]=w
        for v in self.s.keys():
            for u in oriGraph[v]:
                if(self.s[u]<self.s[v]):
                    dist = distuv.get(cedge(self.s[u],self.s[v]))
                    deltadist = min([self.TE[cedge(u,v)],self.minTruss[u],self.minTruss[v]])
                    if(not(dist is None) and distG[v]+distG[u]+deltadist==dist):
                        #v->s[v] u->s[u]
                        for x in [u,v]:
                            while (x != father[x]):
                                newG[x].append((father[x], 1))
                                newG[father[x]].append((x, 1))
                                x = father[x]
                        newG[u].append((v,1))
                        newG[v].append((u,1))
        return newG
    def DELETELEAF(self,graph,Q):
        flag = {}
        for v in graph.keys():
            flag[v]=0 if (graph[v].__len__()==1 and not(v in Q)) else 1
        newG = defaultdict(list)
        for v in graph.keys():
            if(flag[v]):
                for u,w in graph[v]:
                    if(flag[u] and u<v):
                        newG[u].append((v,w))
                        newG[v].append((u,w))
        return newG
    def GETG1(self,graph,Q):
        self.s, self.distG, self.father = self.SPFA(graph, Q)
        triList = []
        for u in graph.keys():
            for v in graph[u]:
                if (self.s[u] < self.s[v]):
                    deltadist = self.factor * (
                            self.maxTruss - min([self.minTruss[u], self.minTruss[v], self.TE[cedge(u, v)]]))
                    triList.append((self.s[u], self.s[v], self.distG[u] + self.distG[v] + deltadist))
        G1 = defaultdict(list)
        triList = sorted(triList, key=lambda x: x)
        for i in range(triList.__len__()):
            u, v, w = triList[i]
            if (i == 0 or (u, v) != triList[i - 1][0:2]):
                G1[u].append((v, w))
                G1[v].append((u, w))
        return G1
    def CONSTRUCT(self,graph,Q):
        G1 = self.GETG1(graph,Q)
        G2 = self.KRUSKAL(G1)
        G3 = self.EXPAND(G2,graph)
        G4 = self.KRUSKAL(G3)
        G5 = self.DELETELEAF(G4,Q)
        return G5

def BFSEXTENDG(graph,oriGraph,szLimit,TE,kt):
    que = queue.Queue()
    flag = defaultdict(int)
    for v in graph.keys():
        que.put(v)
        flag[v]=1
    while(not que.empty()):
        u = que.get()
        for v in oriGraph[u]:
            if(TE[cedge(u,v)]>=kt):
                if(len(graph.keys())>=szLimit):
                    return
                else :
                    if(flag[v]==0):
                        graph[v].append((u,1))
                        graph[u].append((v,1))
                        flag[v]=1
                        que.put(v)


def FINDG0(graph,oriGraph,Q,szLimit,TE):
    #返回一个最大的k-truss，使得k-truss包含Q且k最大
    #First 使用truss-decomposition算法计算所有边的trussness
    # 这里接收到的graph是一棵steinertree

    kt = INF
    for v in graph.keys():
        for u,w in graph[v]:
            if(v<u): kt = min(kt,TE[cedge(v,u)])
    BFSEXTENDG(graph,oriGraph,szLimit,TE,kt)

    for v in graph.keys():
        graph[v] = sorted(graph[v],key=lambda x:-TE[cedge(x[0],v)])
    k = INF
    for u in graph.keys():
        k = min(k,TE[cedge(u,graph[u][0][0])])

    S=defaultdict(set)
    V,Vedge=set(),set()
    S[k]=copy.copy(Q)
    G0 = defaultdict(list)
    while(connected(G0,Q)==False):
        queK = queue.Queue()
        for  v in S[k]: queK.put(v)
        while(not (queK.empty())):
            v = queK.get()
            if (v in V): kmax = k+1
            else :
                kmax = INF
                V.add(v)
                if(G0.get(v)==None):
                    G0[v]=[]
            for u,w in graph[v]:
                if(TE[cedge(u,v)]<k):break;
                elif (TE[cedge(u,v)]<kmax) :
                    if(not (cedge(u,v) in Vedge)):
                        Vedge.add(cedge(u,v))
                        G0[u].append((v, 1))
                        G0[v].append((u, 1))
                    if not(u in S[k]):
                        S[k].add(u)
                        queK.put(u)
            l = TE[cedge(v,graph[v][0][0])]
            S[l].add(v)
        k-=1
    return G0

def dfs(v,graph,color,flag):
    flag[v] = color
    for u,w in graph[v]:
        if(not flag[u]):
            dfs(u,graph,color,flag)

def connected(graph,Q):
    flag = defaultdict(int)
    color,count = 1,0
    for v in Q:
        if(not flag[v]):
            count+=1
            if(count>=2) : break
            dfs(v,graph,color,flag)
            color += 1
    return True if count==1 else False

def MAINTAINKTRUSS(graph,L,supE,k):
    S = set()
    flag = defaultdict(int)
    for v in L:
        for u,w in graph[v]:
            S.add(cedge(u,v))
    while(S.__len__()):
        u,v = S.pop()
        Nuv = set(graph[u])&set(graph[v])
        for w in Nuv:
            e1,e2 = cedge(u,w),cedge(v,w)
            for ex in [e1,e2]:
                supE[ex]-=1
                if(supE[ex]<k-2): S = S.add(ex)
        flag[cedge(u,v)]=1
    ansG=defaultdict(list)
    for v in graph.keys():
        if(not (v in L)):
            ansG[v] = []
            for u,w in graph[v]:
                if(not flag[cedge(u,v)]):
                    ansG[v].append((u,1))
    return ansG
def COMPUTEDIST(graph,Q):
    distG = {}
    flag = defaultdict(int)
    for v in graph.keys(): distG[v]=INF
    que = queue.Queue()
    for v in Q:
        distG[v]=0
        flag[v]=1
        que.put(v)
    while(not que.empty()):
        u = que.get()
        for v,w in graph[u]:
            if(distG[v]==INF and flag[v]==0):
                distG[v]=distG[u]+1
                flag[v]=1
                que.put(v)
    return distG
def BUILKDELETE(graph,Q,supE):
    d = INF
    l = 0
    ansG = defaultdict(list)
    while(connected(graph,Q)):
        distG = COMPUTEDIST(graph,Q)
        maxdistG = max(distG.values())
        if(maxdistG<d):
            d=maxdistG
            ansG = copy.copy(graph)
        L = {x for x in distG.keys() if distG[x]>=d}
        graph = MAINTAINKTRUSS(graph,L,l,supE)
        l+=1
    return ansG

def LCTC(graph,szLimit,Q):
    supE, TE = EDGETRUSS(graph)
    steiner = STEINER(TE,graph,Q)
    G0 = FINDG0(steiner.G,graph,Q,szLimit,TE)
    ansG = BUILKDELETE(G0,Q,supE)
    return ansG

def readData():
    f = open("../data/ego-Facebook/facebook/0.edges",'r')
    graph = defaultdict(list)
    for line in f.readlines():
        u,v = line.strip().split(" ")
        graph[int(u)].append(int(v))
        graph[int(v)].append(int(u))
    ff = open(r"F:\桌面\CodeTraining\BigDataLearn\Algorithm\data\ego-Facebook\facebook\ques.txt",'r')
    Q = {int(x) for x in ff.readline().strip().split(" ")}
    return graph,INF,Q

graph,szLimit,Q = readData()
print(LCTC(graph,szLimit,Q))
