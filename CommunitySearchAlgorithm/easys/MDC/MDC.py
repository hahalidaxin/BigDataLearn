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
    f = open(filename,'r')
    if(type==1) :
        graph = defaultdict(list)
        for line in f.readlines():
            line= line.strip('\n').split(' ')
            u,v = int(line[0]),int(line[1])
            graph[u].append(v)
            graph[v].append(u)
        return graph
    elif(type==0):
        line = f.readline()
        list = line.strip().split(" ")
        return list
def checkIteration(listQ,graph):
    return True
def checkDeleteNode(u):
    return True
def MDC(listQ,graph):
    degDict = defaultdict(list) #每个不同的度对应一个列表，存储相应度的节点
    ansMaxDeg = 0
    ansGraph = graph
    for u in graph.keys():
        degDict[u.__len__()].append(u)
    degList = sorted(graph.keys(),key=lambda x:x)
    minDeg = degList[0]
    while(checkIteration()):
        tmpList = degDict[minDeg]
        if(tmpList.__len__() > 0);
            flag = 0
            for v in tmpList:
                if(checkDeleteNode(v)):
                    #删除节点v
                    flag = 1
                    flagtoMinDeg = 0
                    for x in graph[v]:
                        if(graph[x].__len__()==minDeg and not flagtoMinDeg):
                            minDeg-=1
                            flagtoMinDeg=1
                        graph[x].remove(v)
                        degDict[graph[x].__len__()-1].append(x)
                        degDict[graph[x].__len__()].remove(x)
                    graph.remove(v)
                    break
            if(not (flag==0)): break     #最低deg的节点不能删除 到达迭代终点
        while(degDict[minDeg].__len__()==0): minDeg+=1
        if(minDeg>ansMaxDeg):
            ansMaxDeg = minDeg
            ansGraph = copy.copy(graph)
    return ansGraph

if __name__ == "__main__" :
    res = anylizeDir('/data')
    for i in range(res['edges'].__len__()):
        listQ = readData(res['query'][i])
        graph = readdData(res['edges'][i])
        ans = MDC(listQ,graph)
        print(ans)