#图的边权默认为1
#没有考虑inner link，自环的情况

import os
import collections
from collections import defaultdict
import string

filename = "facebook/"

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

def modularity(tag_dict,map_dict):
    #根据tag和图的连接方式计算模块度
    m = 0
    community_dict = defaultdict(list)
    #同属一个社群的人都有谁
    for key in map_dict.keys():
        m += map_dict[key].__len__()
        community_dict[tag_dict[key]].append(key)

    Q = 0
    for com in community_dict.keys():
        sum_in = 0
        sum_tot = 0
        for u in community_dict[com]:
            sum_tot+=map_dict[u].__len__()
            for v in map_dict[u]:
                if(tag_dict[v]==tag_dict[u]) :
                    sum_in+=1;
        Q += (sum_in/m-(sum_tot/m)**2)
    return Q

def changeTagRound(tag_dict,map_dict,Q):
    tmp_tagDict = dict(tag_dict)
    for u in map_dict.keys():
        ori_com = tmp_tagDict[u]
        for v in map_dict[u]:
            if(tmp_tagDict[u]!=tmp_tagDict[v]):
                tmp_tagDict[u]=tmp_tagDict[v]
                Q_new = modularity(tmp_tagDict,map_dict)
                if(Q_new>Q):
                    Q = Q_new
                    ori_com = tmp_tagDict[u]
                else :
                    tmp_tagDict[u] = ori_com
    return Q,tmp_tagDict

def rebuildMap(tag_dict,map_dict):
    #将一个社区作为一个节点重新构造图
    map2 = defaultdict(list)
    for u in map_dict.keys():
        tagu = tag_dict[u]
        for v in map_dict.keys():
            tagv = tag_dict[v]
            if(tagu!=tagv and (map2[tagv].count(tagu)==0)) :
                map2[tagu].append(tagv)
                map2[tagv].append(tagu)
    tag2 = dict(zip(map2.keys(),map2.keys()))
    return tag2,map2

def fast_unfolding(tag_dict,map_dict):
    Q = 0
    Q_new = modularity(tag_dict,map_dict)
    while(Q != Q_new):
        Q = Q_new
        Q_new,tag_dict = changeTagRound(tag_dict,map_dict,Q)
    print(tag_dict)
    tag_dict2,map_dict2 = rebuildMap(tag_dict,map_dict)
    Q_new = modularity(tag_dict2, map_dict2)
    while (Q != Q_new):
        Q = Q_new
        Q_new, tag_dict2 = changeTagRound(tag_dict2, map_dict2,Q)
    tag_final = dict(zip(map_dict.keys(),[tag_dict2[tag_dict[x]] for x in map_dict.keys()]))
    return Q,tag_final

if __name__ == "__main__":
    res = anylizeDir(filename)
    for name in res['edges']:
        map_dict = readData(name)
        tag_dict = dict(zip(map_dict.keys(),map_dict.keys()))       #构造初始标签数组
        Q,tag_dict = fast_unfolding(tag_dict,map_dict)
        print(Q,"\n",tag_dict)