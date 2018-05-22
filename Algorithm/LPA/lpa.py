import collections
from collections import defaultdict
import os

LOOPLIMIT = 1000
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

def readData(filename):
    graph = defaultdict(list)
    f = open(filename,'r')
    for line in f.readlines():
        line= line.strip('\n').split(' ')
        u,v = int(line[0]),int(line[1])
        graph[u].append(v)
        graph[v].append(u)
    return graph

def getMost(nodeU):
    counter = collections.Counter(nodeU)
    tmpls = sorted(counter.items(),key = lambda it:-it[1])
    return tmpls[0][0]

def checkEnd(label,data):
    for x in data.keys():
        if(label[x] != getMost(data[x])):
            return 0
    return 1

def update(label,data):   #修改data数组
    for x in data.keys():
        data[x] = [label[i] for i in data[x]]

def main(mydata):
    data = mydata.copy()
    label = dict([(i,i) for i in data.keys()])
    loopcnt = 0
    while True:
        loopcnt += 1
        if(loopcnt>LOOPLIMIT or checkEnd(label,data)):
            if(loopcnt>LOOPLIMIT): print("Exit loop because of Limitation")
            else : print("Exit loop becase of Astringent")
            break
        for i in label.keys():
            label[i] = getMost(data[i])     #修改label标签
            update(label,data)
    return label

if __name__== '__main__':
    edgesFiles = anylizeDir("facebook").get('edges')
    for filename in edgesFiles:
        graph = readData(filename)
        print("DATA FROM" + filename + " :")
        print(main(graph))
