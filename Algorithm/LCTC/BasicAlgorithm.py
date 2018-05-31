import string
import copy
from collections import defaultdict

def anylizeDir(path):
    res = defaultdict(list)
    for tname in os.listdir(path):
        wholename = os.path.join(path,tname)
        if(os.path.isdir(wholename)):
            res['dir'].append(wholename)
        else:
            _,type = tname.split('.')
            if(type=="edges"):
                res['edges'].append(wholename)
            else:
                res["elsefile"].append(wholename)
    return res

def readData(filename,type):
    if(type==0):
        graph = defaultdict(list)
        f = open(filename,'r')
        for line in f.readlines():
            line= line.strip('\n').split(' ')
            u,v = int(line[0]),int(line[1])
            graph[u].append(v)
            graph[v].append(u)
        return graph
    elif(type==1) :
        f = open(filename,'r')
        line = f.readline()
        ulist = line.strip().split(' ')
        return ulist

def cedge(u,v):
    return (min(u,v),max(u,v))
def trussDecomposition(graph):
    #利用truss-decomposition算法 计算grapn中每条边的trussness
    TE = {}
    supE,edgeExist= defaultdict(int),defaultdict(int),defaultdict(int)
    for u in graph.keys():
        for v in graph[u]:
            e = cedge(u,v)
            if(edgeExist[e]==0):
                edgeExist[e]=1
                supE((cedge(u,v))) = len(set(graph[u])&set(graph[v]))
    #构造vert 按照sup顺序存储所有的边 其中bin与pos是辅助数组 使得update操作能够在常数时间内完成
    vert = sorted(supE.keys(),key=lambda x:supE[x])
    bin,pos = {},{}
    last = -1,numEdge=vert.__len__()
    for i in range(numEdge):
        pos[vert[i]] = i
        if(supE[vert[i]] != last):
            bin[supE[vert[i]]]=i,last=supE[vert[i]]
    k,lowestSup = 2,0
    while(numEdge):
        while(supE[vert[lowestSup]]<=k-2):
            e = vert[lowestSup]
            u,v = e
            for w in graph[u]:
                e1 = cedge(v,w)
                e2 = cedge(u,w)
                if(edgeExist[e1]):
                    #维护vert 改变两条边在vert中的位置
                    for ex in [e1,e2]:
                        pw = max([supE[ex]],lowestSup+1)      #修改的地方 当lowestSup与ex的sup相同的时候
                        pu = pos[ex]
                        fe = vert[pw]
                        if(fe!=ex):
                            vert[pw]=ex
                            vert[pu]=fe
                            bin[supE[e1]]+=1
                        supE[ex]-=1
            TE[e]=k,edgeExist[e]=0,numEdge-=1
            lowestSup+=1
        k+=1
    return TE

def FindG0(Q,graph):
    #返回一个最大的k-truss，使得k-truss包含Q且k最大
    #First 使用truss-decomposition算法计算所有边的trussness
    tmpgrapn = copy.copy(graph)
    TE = trussDecomposition(tmpgraph)
    tmpdict = {},k=99999999
    for u in graph.keys():
        graph[u]=sorted(graph[u],lambda x:-TE[cedge(u,x)])
        k = min(k,TE[graph[u][0]])
        for v in graph[v];
            tmpdict[cedge(u,v)]=TE[cedge(u,v)]

    S=defaultdict(set),V=set()
    vert = sorted(tmpdict.keys(),key=lambda x:-tmpdict[x])
    maxTE = 0 , G0=set(Q)
    while(connected(Q,G0)==False):
        while(S[k] is not None):
            v = S[k].pop()
            if (v in Sk):
                kmax = k+1
            else :
                kmax = 9999999999
            for u in graph[v]:
                if(TE[cedge(u,v)]<k):break;
                else :
                    G0.add(cedge(u,v))
                    if(u is not in S[k]): S[k].add(u)
            l = 0
            for u in graph[v]:
                if(cedge(u,v) is not in G0);
                    l=max(l,TE[cedge(u,v)])
            S[l].add(v)
        k-=1
    return G0

def BasicAlgorithm(Q,graph):
    G0=FindG0(Q,graph)

if (__name__=="__main__"):
    res = anylizeDir("facebook")
    for i in res["edges"].__len__():
        Q = readData(res["query"][i],1)
        graph = readData(res["edges"][i],0)
        R = BasicAlgorithm(Q,graph)
        print(R)