import time
import queue
import copy
import random
from collections import defaultdict
from collections import Counter
import sys
sys.path.append("../")
from AlgorithmATC import GraphFunc
from AlgorithmATC import ATindex
from AlgorithmATC.Steiner import Steiner
from AlgorithmATC import AttributeScoreFunc
import time

class locATC3Search:
    def __init__(self,graph_information,tempt_nodes_information,ExperimentalDataList):
        self.graph_information = graph_information
        self.tempt_nodes_information = tempt_nodes_information
        self.ExperimentalDataList = ExperimentalDataList
        self.INF = float('inf')
        self.erlta = 3
        self.attrTE = None
        self.attrSupE = None
        self.szlimits = 60
        return

    def cedge(self,u,v):
        return min(u,v),max(u,v)

    def getGraphWithAttrDist(self,graph,Wq,attrTE):
        delta = 3
        maxTe = max(attrTE[''].values())
        newG = defaultdict(list)
        for v in graph.keys():
            for u in graph[v][0]:
                if v>u: continue
                distuv = 1
                for w in Wq:
                    if attrTE[w].get(self.cedge(u, v)) is None:
                        distuv += maxTe
                    else:
                        distuv += delta*(maxTe - attrTE[w][self.cedge(u, v)])
                newG[v].append((u, distuv))
                newG[u].append((v, distuv))
        return dict(newG)

    def ExtendtoGt(self,steinerT,origraph,Wq,TE):
        que = queue.Queue()
        flag = defaultdict(int)
        newG = {}
        for v in steinerT.keys():
            que.put(v)
            flag[v] = 1
            newG[v] = [copy.deepcopy(steinerT[v]), copy.deepcopy(origraph[v][1])]
        Wqset = set(Wq)
        while not que.empty():
            u = que.get()
            for v in origraph[u][0]:
                if len(newG.keys()) >= self.szlimits:
                    return newG
                else:
                    # AttributeScore条件约束
                    newgwithu = GraphFunc.addNodewithG(newG, origraph, v)
                    # a1 = AttributeScoreFunc.attributeScore(newgwithu, Wqset)
                    # a2 = AttributeScoreFunc.attributeScore(newG, Wqset)
                    boolflag = AttributeScoreFunc.attributeScore(newgwithu, Wqset) >= AttributeScoreFunc. \
                            attributeScore(newG, Wqset)
                    if not boolflag:
                        boolflag = (AttributeScoreFunc.thetaFuncforWqSet(newG, Wqset&set(origraph[v][1]))
                                         >= AttributeScoreFunc.attributeScore(newG, Wqset)/2*len(newG))
                    if not boolflag:
                        boolflag = (AttributeScoreFunc.attributeScore(newgwithu,Wqset|set(origraph[v][1]))
                                        >= AttributeScoreFunc.attributeScore(newgwithu,Wqset))
                    if not boolflag:
                        continue
                    '''
                    if AttributeScoreFunc.thetaFuncforG(newG, list(Wq_extend & set(oriorigraph[v][1]))) < AttributeScoreFunc.\
                            attributeScore(newG, Wq_extend) / (2 * len(newG)): continue
                    '''
                    if newG.get(v) is None:
                        newG[v] = [[], copy.deepcopy(origraph[v][1])]
                    if newG[v][0].count(u) == 0:
                        newG[v][0].append(u)
                        newG[u][0].append(v)
                    if flag[v] == 0:
                        #Wq_extend = Wq_extend & set(graph[v][1])
                        flag[v] = 1
                        que.put(v)
        return newG

    def MaintainKDTruss(self,k,d,graph,Q,Wq):
        Gt = copy.deepcopy(graph)
        while GraphFunc.connected(Gt,Q):
            TE,supE = ATindex.StructuralTrussness(Gt)
            distG = GraphFunc.getDistG(Gt,Q)
            edgestodelete = {}
            for v in distG:
                if distG[v] > d:
                    for u in Gt[v][0]:
                        edgestodelete[self.cedge(u, v)] = 1
            for e in supE:
                if supE[e] < k-2:
                    edgestodelete[e] = 1
            if len(edgestodelete) == 0: return Gt
            Gt = GraphFunc.deleteEdges(Gt,edgestodelete)
            if len(Gt) == 0: break
        return Gt

    def BULK(self,graph, Q, Wq, k, d):
        l = 0
        Gl1 = copy.deepcopy(graph)
        distG = GraphFunc.getDistG(graph,Q)
        d = max(max(distG.values()),d)
        S = [v for v in Gl1.keys() if distG[v]<=d]
        Gl2 = GraphFunc.buildNewGraph(Gl1, S)
        ktemp = self.INF
        TE, supE = ATindex.StructuralTrussness(Gl2)
        for q in Q:
            ktmp = max(TE[self.cedge(q, v)] for v in Gl2[q][0])
            k = min(ktemp, ktmp)
        k = min(ktemp, k)
        while True:
            if k == 2: break
            if GraphFunc.connected(self.MaintainKDTruss(k,d,Gl2,Q,Wq),Q) : break
            k-=1
        Gl = self.MaintainKDTruss(k,d,Gl2,Q,Wq)
        maxfunc, ansg = -self.INF, None
        while GraphFunc.connected(Gl,Q):
            attriscore = AttributeScoreFunc.attributeScore(Gl, Wq)
            if maxfunc < attriscore:
                maxfunc, ansg = attriscore, copy.deepcopy(Gl)

            gain = AttributeScoreFunc.computeGainFunc(k,Gl,Wq)
            mingain = self.INF
            for v in gain:
                if gain[v] < mingain and not v in Q: mingain = gain[v]
            if mingain == self.INF :
                break
            S = [v for v in gain.keys() if gain[v] == mingain and not v in Q]
            if len(S) == 0:
                break
            S = random.sample(S, max(1,int(len(S)*self.erlta/(self.erlta+1))))
            edgesToDelete = GraphFunc.getNeighborEdges(Gl,S)
            Gl = GraphFunc.deleteEdges(Gl,edgesToDelete)
            Gl = self.MaintainKDTruss(k,d,Gl,Q,Wq)
        return list(ansg.keys())

    def prepareforATC(self,graph,Q,Wq):
        flag = defaultdict(int)
        color = 1
        for v in graph.keys():
            if not flag[v]:
                GraphFunc.dfsWithLable(v,graph,flag,color)
                color += 1
        countforQlabel = {color: sum(flag[q] == color for q in Q) for color in range(color)}
        qlabellist = sorted(countforQlabel,key = lambda x:-countforQlabel[x])
        countforGlabel = {color: sum(flag[i] == color for i in graph) for color in range(color)}
        maxcount = 1
        for color in qlabellist:
            if countforQlabel[color] != countforQlabel[qlabellist[0]]:
                break
            maxcount = max(maxcount,countforGlabel[color])
        maxcolor = -1
        for color in qlabellist:
            if countforQlabel[color] != countforQlabel[qlabellist[0]]:
                break
            if  maxcount == countforGlabel[color]:
                maxcolor = color
                break
        ans = [v for v in Q if flag[v]==maxcolor]
        return ans

    def locATC_MAIN(self,graph,Q,Wq,k=4,d=4,szlm=50):
        if szlm != 80:
            self.szlimits = szlm
        else :
            self.szlimits = 50
        nowQ = self.prepareforATC(graph,Q,Wq)
        global attrTE, attrSupE
        starttime = time.time()
        self.attrTE,self.attrSupE = ATindex.AttributedTrussness(graph,Wq,self.attrTE,self.attrSupE)
        endtime = time.time()
        steiner = Steiner(self.getGraphWithAttrDist(graph, Wq, self.attrTE),nowQ)  # steiner G 's :{v->[u1,u2...]}
        if steiner.G is None or len(steiner.G) == 0: return Q
        Gt = self.ExtendtoGt(steiner.G, graph, Wq, self.attrTE[''])
        ansg = self.BULK(Gt, nowQ, Wq, k, d)
        for q in Q:
            if not q in ansg :
                ansg.append(q)
        addedtime = endtime - starttime
        return ansg,addedtime

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
                'allmemberlen':0,
                'alladdedtime':0
            }
        for i in range(0,len(self.ExperimentalDataList)):
            print(" \t\t rk: {}".format(i))
            TestData = self.ExperimentalDataList[i]
            group_name = TestData[0]
            QVlist = TestData[1]
            QAlist = TestData[2]
            #print(" \t\t QVlist: "+str(QAlist)+", QAlist: "+str(QAlist)+", group_name: "+str(group_name))
            GMembers = self.graph_information['Groups'][group_name][0]
            SearchedMembers,addedtime = self.locATC_MAIN(self.tempt_nodes_information, QVlist, QAlist)
            [precision,recall,score] = self.F1Score(GMembers,SearchedMembers)
            #print(str([precision,recall,score]))
            results['allscore'] = results['allscore'] + score
            results['allprecision'] = results['allprecision'] + precision
            results['allrecall'] = results['allrecall'] + recall
            results['allmemberlen'] = results['allmemberlen'] + len(GMembers)
            results['alladdedtime'] = results['alladdedtime'] + addedtime
        endtime = time.time()
        duration = endtime-starttime
        build_duration = results['alladdedtime']
        query_duration = duration - build_duration
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
            TimeEvaluation = query_duration*1.0/len(self.ExperimentalDataList)/averagelen
        return [resultS,resultP,resultR,duration,build_duration,query_duration,TimeEvaluation]




if __name__ == "__main__":
    pass
    # atc = locATCSearch(graph_information,temp_nodes,experimentdatalist)
    # print(atc.main())
