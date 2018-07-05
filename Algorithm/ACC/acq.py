import os
import sys
import copy
from collections import defaultdict

sys.path.append(r"F:\桌面\CodeTraining\BigDataLearn\Algorithm")
import CommunitySearch as CS

#分解法求解coreG数组
def CORES(graph):
    bin,deg,pos,vert={},{},{},{}
    md = 0
    for v in graph.keys():
        deg[v] = graph[v].__len__()
        if(deg[v]>md): md=deg[v]
    for d in range(0,md+1): bin[d]=0
    for v in graph.keys(): bin[deg[v]]+=1
    start = 1
    for d in range(0,md+1):
        num = bin[d]
        bin[d]=start
        start+=num
    for v in graph.keys():
        pos[v]=bin[deg[v]]
        vert[pos[v]]=v
        bin[deg[v]]+=1
    for d in range(md,0,-1):
        bin[d]=bin[d-1]
    bin[0]=1
    for i in range(1,len(vert)+1):
        v = vert[i]
        for u in graph[v]:
            if(deg[u]>deg[v]) :
                du = deg[u]
                pu = pos[u]
                pw = bin[du]
                w = vert[pw]
                if(u!=w) :
                    pos[u]=pw
                    pos[w]=pu
                    vert[pu]=w
                    vert[pw]=u
                bin[du] += 1
                deg[u] -= 1
    return deg
#添加了anchor属性的并查集
class AFU:
    class node:
        def __init__(self, parent,anchor):
            self.parent,self.anchor = parent,anchor
            self.rank = 0
    def __init__(self):
        self.NS = defaultdict(self.node)
    def MAKESET(self,x):
        self.NS[x] = self.node(-1,x)
    def find(self,x):
        if(x.parent ==-1) : return x
        else :
            return self.find(x.parent)
    def FIND(self,x):
        return self.find(self.NS[x])
    def UNION(self,x,y):
        xRoot = self.FIND(x)
        yRoot = self.FIND(y)
        if(xRoot==yRoot): return
        if (xRoot.rank<yRoot.rank) :
            xRoot.parent = yRoot
        elif (xRoot.rank>yRoot.rank):
            yRoot.parent = xRoot
        else :
            yRoot.parent = xRoot
            xRoot.rank += 1
    def UPDATEANCHOR(self,x,coreG,y):
        xRoot = self.find(x)
        if(coreG[xRoot.anchor]>coreG[y]):
            xRoot.anchor = y

class CL_TREE:
        class treenode:
            def __init__(self,coreNum,vertexSet,property):
                self.coreNum = coreNum
                self.vertexSet = vertexSet
                self.invertedList = defaultdict(set)       #property ->List of Vertex owing the property
                self.childList = []
                for v in vertexSet:
                    for p in property[v]:
                        self.invertedList[p].add(v)
        def __init__(self,graph,property):
            self.root = self.BUILDINDEX(graph,property)
        # 构建CL-Tree
        def dfs(self,v,label,graph,rank):
            label[v]=rank
            for u in graph[v]:
                if(not(label[u])):
                    self.dfs(u,label,graph,rank)
        def ConnectedComponents(self,newG):
            label = defaultdict(int)
            rank = 1
            for v in newG.keys():
                if(not label[v]):
                    self.dfs(v,label,newG,rank)
                    rank+=1
            return label
        def BUILDINDEX(self,graph,property):
            self.property = property
            afu = AFU()
            for v in graph.keys(): afu.MAKESET(v)
            coreG = self.coreG = CORES(graph)
            V = defaultdict(set)
            kmax = 0
            for v in graph.keys():
                V[coreG[v]].add(v)
                kmax = max(kmax, coreG[v])
            k,map,flag = kmax,{},defaultdict(int)
            while (k >= 0):
                tV = set()
                for v in V[k]:
                    tV.add(afu.FIND(v))
                    flag[v]=1
                newG = buildSubgraph(graph,list(flag.keys()))
                label = self.ConnectedComponents(newG)
                compo = defaultdict(set)
                for v in label.keys():
                    if(v in V[k]): compo[label[v]].add(v)
                for i in compo.keys():
                    Pi = self.treenode(k,compo[i],property)
                    for v in compo[i]:
                        map[v]=Pi
                        for u in graph[v]:
                            if(coreG[u]>=coreG[v]):
                                afu.UNION(u,v)
                            if(coreG[u]>coreG[v]):
                                uRoot = afu.FIND(u)
                                uAnchor = uRoot.anchor
                                pt = map.get(uAnchor)
                                Pi.childList.append(pt)
                            # 基于Vk的每个连通子集进行操作
                        vRoot = afu.FIND(v)
                        if(coreG[vRoot.anchor]>coreG[v]):
                            afu.UPDATEANCHOR(vRoot,coreG,v)
                k-=1
            sons = set(graph.keys())
            minCore = min(coreG[v] for v in graph.keys() if (coreG[v]))
            root = self.treenode(0, {v for v in graph.keys() if not coreG[v]} ,property)
            root.childList = list({map[afu.FIND(v).anchor] for v in graph.keys() if (coreG[v]==minCore)})
            return root
        def findR(self,root,q,end,top,ans):
            flag = defaultdict(int)
            self.tFindR(root,flag,q,end,top,ans)

        def tFindR(self,root,flag,q,end,top,ans):
            flag[root]=1
            if (q in root.vertexSet):
                ans[root.coreNum] = root
                return True
            for v in root.childList:
                if(not flag[v]):
                    resBool = self.tFindR(v,flag,q,end,top,ans)
                    if(resBool and end<=root.coreNum<=top):
                        ans[root.coreNum] = root
                    if(resBool): return True
            return False
        def findGSt(self,R,St,c):
            ans = set()
            cmax = max(R.keys())
            for i in range(c,cmax+1):
                if(R.get(i) is None): continue
                root = R[i]
                flag = 0
                tans = set()
                for s in St:
                    if (flag == 0):
                        flag = 1
                        tans = root.invertedList[s]
                    else:
                        tans = tans & root.invertedList[s]
                ans = ans|tans
            return ans
def buildSubgraph(graph,vertices):
    newG = defaultdict(list)
    for v in vertices:
        newG[v] = []
        for u in graph[v]:
            if(u<v and vertices.count(u)):
                newG[v].append(u)
                newG[u].append(v)
    return newG

def findcoreGkExist(graph,k):
    coreG = CORES(graph)
    maxcore = max(coreG.values())
    return maxcore if (maxcore>=k) else -1

#主算法 Inc-S算法 递增序、空间友好的算法
def INCS(G,Property,cltree,q,k,S):
    #x寻找一条路径，这条路径上包含有q节点，而且满足路径上节点的coreG位于[end,top]之间
    R = {}
    cltree.findR(cltree.root,q,k,cltree.coreG[q],R)
    l = 0
    FAI = []
    for p in S:
        stt = set()
        stt.add(p)
        if(Property[q].count(p)): FAI.append((stt,k))
    POSY = defaultdict(list)
    while True:
        l += 1
        for St,c in FAI:
            GS = list(cltree.findGSt(R,St,c))
            newG = buildSubgraph(graph, GS)
            m,n = 0,newG.keys().__len__()
            m = (sum(newG[v].__len__() for v in newG.keys()))/2
            if(not (m-n<((k**2-k)/2-1))) :
                maxcoreG = findcoreGkExist(newG,k)
                if(maxcoreG!=-1) : POSY[l].append((St,maxcoreG))

        if(POSY[l].__len__()):
            FAI=[]
            posi=POSY[l]
            for i in range(posi.__len__()):
                si,corei = posi[i]
                for j in range(i+1,posi.__len__()):
                    sj,corej = posi[j]
                    if(len(si)==len(sj)):
                        st = si | sj
                        if (len(st) == len(si) + 1):
                            #这里没有利用lemma1进行剪枝
                            c = max(corei,corej)
                            FAI.append((st,c))
        else :
            break
    print(POSY[l-1])
    '''
    #dfs(cltree.root)
    #在这里进行了选择，永远选择第一个构造答案
    S,c = POSY[l-1][0]
    ans = set()
    cmax = max(R.keys())
    for i in range(c,cmax+1):
        rt = R[i]
        tans = set()
        flag = 0
        for prop in S:
            if(flag==0):
                flag = 1
                tans = rt.invertedList[prop]
            else:
                tans = tans & rt.invertedList[prop]
                if(rt.invertedList[prop].__len__()==0):
                    tans = set()
        ans=ans|tans
    return ans
    '''
def readData(filename):
    f = open(filename,'r')
    N = int(f.readline())
    graph = {}
    property = {}
    for i in range(N):
        line = f.readline()
        str = line.strip().split(" ")
        property[int(str[0])] = []
        for w in str[1:]:
            property[int(str[0])].append(w)
    for i in range(N):
        line =f.readline()
        str = line.strip().split(" ")
        graph[int(str[0])]=[]
        for v in str[1:]:
            graph[int(str[0])].append(int(v))
    line = f.readline()
    str = line.strip().split(" ")
    q,k = int(str[0]),int(str[1])
    line = f.readline()
    str = line.strip().split(" ")
    S = list(str)
    return graph,property,q,k,S

flag = defaultdict(int)

def test_dfs(rt):
    print("vertextSet: ",rt.vertexSet)
    print("invertedList: ",rt.invertedList)
    print("coreNum",rt.coreNum)
    #print(rt)
    #print("childList",rt.childList)
    print("")
    flag[rt]=1
    for v in rt.childList:
        if(not flag[v]):
            test_dfs(v)

if __name__=="__main__":

    print(CS.graph_information)
    print(CS.tempt_nodes_information)
    G = CS.tempt_nodes_information

    #graph,property,q,k,S = readData("data.txt")
    graph = {v:G[v][0] for v in G.keys()}
    property = {v:G[v][1] for v in G.keys()}
    print(property)
    cltree = CL_TREE(graph,property)
    test_dfs(cltree.root)
    #cltree = CL_TREE(graph,property)
    S = set([93, 78, 53, 157, 142])
    ans = INCS(graph,property,cltree,"71",1,S)
    #dfs(cltree.root)
    print(ans)
