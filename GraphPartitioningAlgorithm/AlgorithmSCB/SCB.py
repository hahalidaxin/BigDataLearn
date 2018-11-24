from . import uClass
from . import uFunc
import random
import queue

inf = float('inf')

class SCBAlgorithm:
    # servsers是服务器信息数组
    def __init__(self,graph,servers,W,S,nodeV,conX,conE,limiIte):
        self.conX = conX
        self.conE = conE
        self.limiIte = 10
        self.graph = graph
        self.servers = servers
        self.S = S
        self.W = W

        minload_server = self.InitialAssignment(self.servers)
        iniserver = self.servers[minload_server]
        self.servers[minload_server].createCopy('p', nodeV)
        self.DataAvailability(self.graph, self.servers, nodeV, iniserver, self.conX)
        self.NodeRelocationaSwaping(iniserver, nodeV)
        self.OfflineMerginaGroupBasedSwapping()

    def InitialAssignment(self):
        minloadserver, minload = None, inf
        for sv in self.servers:
            svload = self.servers[sv].getload()
            if svload < minload:
                minload, minloadserver = self.servers[sv].getload(), sv
        return sv

    def DataAvailability(self,nodeV,nodev_server):
        for u in graph[nodeV]['n']:
            u_server = self.servers[u]
            u_server.createCopy('r', nodeV)
            nodev_server.createCopy('r',u)
        if self.conX==0: return
        serverflag = {}
        for i in range(self.conX):
            minload, minloadserver = inf, None
            for sv in self.servers:
                if serverflag.get(sv) is None and sv.getload() < minload:
                    minload, minloadserver = sv.getload(), sv
                    serverflag[sv] = 1
            targetserver = self.servers[minloadserver]
            targetserver.createCopy('v', nodeV)

    def NodeRelocationaSwaping(self,inisv,nodeV):
        maxscb,maxscb_sv = -inf,None
        for sv in self.servers:
            if sv != inisv:
                svscb = uFunc.SCB(graph, nodeV, inisv, sv)
                if svscb > maxscb:
                    maxscb, maxscb_sv = svscb, sv
        if maxscb < 0 : return
        tarsv = self.servers[maxscb_sv]
        scb_nodeV = maxscb
        if uFunc.testLoadAterTrans(self.servers,self.conE,inisv,tarsv,nodeV):
            inisv.removeCopy('p',nodeV)
            tarsv.createCopy('p',nodeV)
            return
        maxscb,maxnodeu = -inf,None
        for u in tarsv.getNodesList():
            scb = uFunc.SCB(self.graph,u,tarsv,inisv)
            if scb > maxscb:
                maxscb, maxnodeu = scb,u
        if maxscb + scb_nodeV > 0:
            # 这个地方有待改正 可能还需要对于各自的pure节点进行copy的转移
            tarsv.removeCopy('p', maxnodeu)
            inisv.removeCopy('p', nodeV)

    def OfflineRelocationaSwapping(self):
        randomnodelist = random.sample(self.graph, self.limiIte)
        for u in randomnodelist:
            self.NodeRelocationaSwaping(u,graph[u]['b'])

    def OfflineMerginaGroupBasedSwapping(self):
        grouprank = 0
        nodeList = []
        for v in self.graph:
            nodeList.append(uClass.Node(self.graph,v))
        UFS = uClass.UFS(nodeList)
        for v in random.shuffle(nodeList):
            acrNode = UFS.find(v)
            if len(acrNode.getNodeList())!=1 :
                continue
            while True
                beta1 = acrNode.getBetaScore()
                mergeFlag = False
                for neiv in acrNode.getExternalConnectionSet():
                    acrNodev = UFS.find(neiv)
                    mergedNode = uClass.Node.mergeNode(self.graph,acrNodev,acrNode)
                    beta2 = acrNodev.getBetaScore()
                    if beta2 > beta1:
                        newNode = UFS.union(acrNode,acrNodev)
                        newNode.copyNode(mergedNode)
                        mergeFlag = True
                        break
                if mergeFlag==False:
                    break
        groupFlag = {}
        groups = []
        for v in nodeList:
            acrNodev = UFS.find(v)
            if groupFlag.get(acrNodev) is None:
                groupFlag[acrNodev] = 1
                groups.append(acrNodev)

        while True:
            maxsize, maxsizeGroup = -inf,None
            for group in groups:
                if group.getnodeSize() > maxsize:
                    maxsize, maxsizeGroup = group.getnodeSize(),group
            for group in groups:
                if group != maxsizeGroup and \
                        abs(group.getnodeSize()-maxsizeGroup.getnodeSize())<self.conE:
                    self.trySwapGroup(maxsizeGroup,group)

        # to enimate the side effect

    # 尝试交换 group in similar size and on a different server
    def trySwapGroup(self):
        pass


    # 如果 可以通过交换virtual Primary Copy的方式来减少non-Primary Copy 的数量 则进行
    def OfflineVirtualPrimarySwapping(self):
        for sv in self.servers:
            for virtualCP in sv.getExistC()['v']:
                for nonpriCP in sv.getExistC()['r']:
                    for svl in self.graph[nonpriCP]['v']:
                        if svl.getExistC()['r'].get(virtualCP) is not None:
                            sv.createCopy('v',nonpriCP)
                            svl.createCopy('v',virtualCP)












# SCB Algorithm 的主函数
# 参数说明 graph-图  W-数组-每个user的写频率 S-数组-每个user所占的load
# conK-总的服务器的个数 conX-全部的Virtual Primary Copy的数目限制  conE-任意两个服务器之间load差距限制
def MainSCBAlgorithm(graph,W,S,conK,conX,conE):
    pass


if __name__=="__main__":
    graph = uFunc.readData()
    print(str(graph))
