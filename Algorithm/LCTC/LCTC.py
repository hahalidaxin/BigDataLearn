import os
import copy
import queue
from collections import defaultdict

def cedge(u,v):
    return (min(u,v),max(u,v))
def EDGETRUSS(graph):
    #利用Improved Truss Decomposition算法 计算grapn中每条边的trussness
    TE = {}
    supE= defaultdict(int)
    edgeExist = defaultdict(int)
    for u in graph.keys():
        for v in graph[u]:
            e = cedge(u,v)
            if(edgeExist[e]==0):
                edgeExist[e]=1
                supE[cedge(u,v)] = len(set(graph[u])&set(graph[v]))
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
            if(not edgeExist[e]):
                lowestSup+=1
                numEdge-=1
                continue
            for w in graph[u]:
                e1 = cedge(v,w)
                e2 = cedge(u,w)
                if(edgeExist[e1] and edgeExist[e2]):
                    #维护vert 改变两条边在vert中的位置
                    for ex in [e1,e2]:
                        pw = bin[supE[ex]] if (supE[vert[lowestSup]]!=supE[ex]) else lowestSup+1
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
            lowestSup += 1
        k+=1
    return TE

class STEINER :
    def __init__(self,graph,Q):
        self.INF = 99999999
        self.G = self.CONSTRUCT(graph,Q)
        print(self.G)

    def SPFA(self,graph,Q):
        distG,inq,s= {},{},{}
        father = {}
        for v in graph.keys():
            distG[v] = self.INF
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
                if(distG[u]+1<distG[v]):
                    distG[v]=distG[u]+1
                    father[v]=u
                    s[v]=s[u]
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
        flag = defaultdict(int)
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
                    if(not(dist is None) and distG[v]+distG[u]+1==dist):
                        #v->s[v] u->s[u]
                        for x in [u,v]:
                            while(distG[x]):
                                if(x!=father[x]):
                                    newG[x].append((father[x],1))
                                    newG[father[x]].append((x,1))
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
    def CONSTRUCT(self,graph,Q):
        # 构造G1 #这里并没有考虑论文中所说的修改distG'的问题
        self.s,self.distG,self.father = self.SPFA(graph,Q)
        triList = []
        for u in graph.keys():
            for v in graph[u]:
                if(self.s[u]<self.s[v]):
                    triList.append((self.s[u],self.s[v],self.distG[u]+self.distG[v]+1))
        G1 = defaultdict(list)
        triList = sorted(triList, key=lambda x: x)
        for i in range(triList.__len__()):
            u,v,w = triList[i]
            if(i==0 or (u,v)!=triList[i-1][0:2]):
                G1[u].append((v,w))
                G1[v].append((u,w))
        G2 = self.KRUSKAL(G1)
        G3 = self.EXPAND(G2,graph)
        G4 = self.KRUSKAL(G3)
        G5 = self.DELETELEAF(G4,Q)
        return G5

def BFSEXTENDG(graph,oriGraph,szLimit,TE,kt):
    que = queue.Queue()
    for v in graph.keys():
        que.put(v)
    while(not que.empty()):
        u = que.get()
        for v in oriGraph[u]:
            if(TE[cedge(u,v)]>=kt):
                if(len(graph.keys())==szLimit):
                    return
                else :
                    graph[v].append((u,1))
                    graph[u].append((v,1))


def FINDG0(graph,oriGraph,Q,szLimit):
    #返回一个最大的k-truss，使得k-truss包含Q且k最大
    #First 使用truss-decomposition算法计算所有边的trussness
    # 这里接收到的graph是一棵steinertree

    TE = EDGETRUSS(oriGraph)

    kt = 99999999
    for v in graph.keys():
        for u,w in graph[v]:
            if(v<u): kt = min(kt,TE[cedge(v,u)])
    BFSEXTENDG(graph,oriGraph,szLimit,TE,kt)
    for v in graph:
        graph[v] = sorted(graph[v],key=lambda x:-TE(cedge(x[0],v))
    # 此时的graph是中间子图Gt
    k = 99999999
    for u in graph.keys():
        for v,w in graph[v]:
            k = min(k, TE[cedge(u, v)])
            #tmpdict[cedge(u,v)]=TE[cedge(u,v)]

    S=defaultdict(set)
    V,Vedge=set(),set()
    #vert = sorted(tmpdict.keys(),key=lambda x:-tmpdict[x])
    S[k]=Q
    G0 = defaultdict(list)
    while(connected(G0,Q)==False):
        while(not (S[k] is None)):
            v = S[k].pop()
            if (v in V):
                kmax = k+1
            else :
                kmax = 9999999999
                V.add(v)
            for u,w in graph[v]:
                if(TE[cedge(u,v)]<k):break;
                else :
                    G0.add(cedge(u,v))
                    if not(u in S[k]):
                        Vedge.add(cedge(u,v))
                        G0[u].append((v,1))
                        G0[v].append((u,1))
            l = 0
            for u,w in graph[v]:
                if not (cedge(u,v) in Vedge):
                    l=max(l,TE[cedge(u,v)])
            S[l].add(v)
        k-=1
    G0 = {}
    for v in V: G0[v] = []
    for u,v in Vedge:
        G0[u].append((v,1))
        G0[v].append((u,1))
    return G0

def dfs(v,graph,color,flag):
    flag[v] = color
    for u,w in graph[v]:
        if(not flag[u]):
            dfs(u,graph,color,flag)

def connected(graph,Q):
    flag = defaultdict(int)
    color = 0
    for v in graph.keys():
        if(not flag[v]):
            dfs(v,graph,color,flag)
            color += 1
    count = {}
    for v in Q:
        count[flag[v]]=1
    return True if count.__len__()==1 else False

def MaintainKTruss(graph,L,supE):
    S = set()
    flag = defaultdict(int)
    for v in L:
        for u in graph[v]:
            S.add(cedge(u,v))
    while(S.__len__()):
        u,v = S.pop()
        Nuv = set(graph[u])&set(graph[v])
        for w in Nuv:
            e1,e2 = cedge(u,w),cedge(v,w)
            for ex in [e1,e2]:
                supE[ex]-=1
                if(supE[ex]<k-2): S = S|set(ex)
        flag[cedge(u,v)]=1
    ansG={}
    for v in graph.keys():
        if(not v in L):
            ansG[v] = []
        for u in graph[v]:
            if(not flag(cedge(u,v))):
                ansG[v].append(u)
    return ansG
def BulkDelete(graph,Q):
    d = 9999999
    l = 0
    while(connectG(graph,Q)):
        distG = computeDistG(graph,Q)
        maxdistG = max(distG.values())
        if(maxdistG<d):
            d = maxdistG
        L = {x for x in distG.keys() if distG[x]>=d-1}
        graph = MaintainKTruss(graph,L)
        l+=1
def LCTC(graph,szLimit,Q):
    steiner = STEINER(graph,Q)
    G0 = FINDG0(steiner.G,graph,Q,szLimit)
    ans = BulkDelete(G0,Q)
    return ans

def readData(filename):
    f = open(filename,'r')
    N = int(f.readline())
    graph = {}
    for i in range(N):
        str = f.readline().strip().split()
        graph[int(str[0])]=[int(x) for x in str[1:]]
    szLimit = int(f.readline())
    Q = {int(x) for x in f.readline().strip().split(" ")}
    return graph,szLimit,Q

graph,szLimit,Q = readData("data.txt")
print(LCTC(graph,szLimit,Q))
