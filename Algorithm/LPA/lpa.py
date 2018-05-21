import collections
import random

filename = "0.edges"
def readData():
    graph = {}
    f = open(filename,'r')
    for line in f.readlines():
        line = line.split(" ")
        nodeu = graph.getdefault(int(line[0],[]))
        nodeu.append(int(line[1]))
        nodev = graph.getdefault(int(line[1],[]))
        nodev.append(int(line[0]))
    return graph

def getMost(nodeU):
    counter = collections.Counter(nodeU)
    ta = sorted(counter.items(),key = lambda x:x[1])

    maxc = ta[-1][1]
    maxlist = []
    for x in ta :
        if(x[1]==maxc):
            maxlist.append(x[0])

    random.shuffle(maxlist)
    return maxlist[0]

def checkEnd(cluster,data):
    flag = 0
    for x in data.keys():
        if(cluster[x] != getMost(data[x])):
            return 0
    return 1
def update(cluster,data):
    for x in data.keys():
        data[x] = [cluster[i] for i in data[x]]
def main(mydata):
    data = mydata.copy()
    cluster = dict([(_,_) for _ in data.keys()])
    while True:
        if(checkEnd(cluster,data)): break
        for i in cluster.keys():
            cluster[i] = getMost(data[i])
            update(cluster,data)
    return cluster

graph = readData()
main(graph)