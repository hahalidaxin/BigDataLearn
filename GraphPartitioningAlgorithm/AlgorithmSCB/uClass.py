
class Server:
    def __init__(self,arrS,name):
        # existC['r'] -> non-Primary copy
        # existC['v'] -> Virtual Primary Copy
        # existC['P'] -> Primary Copy
        self.existC = {'v': {}, 'p': {}, 'r': {}}
        self.load = 0
        self.name = name
        self.S = arrS

    def getload(self):
        return self.load

    def getname(self):
        return self.name

    def getExistC(self):
        return self.existC

    def recaculateload(self):
        self.load = 0
        for v in self.existC['p']:
            self.load += self.S[v]
        for v in self.existC['v']:
            self.load += self.S[v]

    def createCopy(self,graph,type,v):
        if type=='p':
            if self.existC['p'].get(v) is None:
                self.existC['p'][v] = 1
                self.load += self.S[v]
                self.graph[v]['b'] = self.getname()
        elif type=='v':
            if self.existC['r'].get(v) is not None:
                self.existC['v'][v] = 0
            if self.existC['v'].get(v) is None:
                self.existC['v'][v] = 1
                self.load += self.S[v]
        elif type=='r':
            if self.existC['v'].get(v) is not None:
                if self.existC['r'].get(v) is None:
                    self.existC['r'][v] = 1

    def removeCopy(self,graph,type,v):
        if type=='p' and self.existC['p'].get(v) is not None:
            self.existC['p'][v] = None
            self.load -= self.S[v]
            graph[v]['b'] = None
        elif type=='v' and self.existC['v'].get(v) is not None:
            self.existC['v'][v] = None
            self.load -= self.S[v]
        elif type=='r' and self.existC['r'].get(v) is not None:
            self.existC['r'][v] = None

    def getCopyNumof(self,type,v):
        return self.existC['r'].get(v,0)*(type&1) + self.existC['v'].get(v,0)*(type&2) + self.existC['p'].get(v,0)*(type&4)


class group:
    def __init__(self,graph,v,rank):
        self.graph = graph
        self.nodelist = [v]
        self.rank = rank
        self.internal_connection = 0
        self.external_connection = None
        self.externalEdgeSet = {}

    def cedge(self,u,v):
        return min(u,v), max(u,v)

    def getinternalConnection(self):
        return self.internal_connection

    def getexternalConnection(self):
        return len(self.externalEdgeSet)

    def getindex(self):
        return self.rank

    def getexternalSet(self):
        return self.externalEdgeSet

    def getnodeSize(self):
        return len(self.nodelist)

    def getExternalConnection(self,groupindex):
        self.external_connection = 0
        for v in self.nodelist:
            for u in self.graph[v]['n']:
                if groupindex[u] != self.rank:
                    self.external_connection += 1
                    self.externalEdgeSet.add(self.cedge(u,v))
        return self.external_connection

    def add_one_Member(self,v):
        self.nodelist.append(v)
        lenofintersec = len(set(self.graph[v]['n']) & (group.getexternalSet()))
        inneredge = len(group.getinternalConnection() + lenofintersec)
        exteredge = len(group.getexternalSet()) + len(self.graph[v]['n']) - lenofintersec
        self.internal_connection = inneredge
        self.external_connection = exteredge
        self.externalEdgeSet.add(v)


class Node:
    def __init__(self,graph,v):
        self.graph = graph
        self.list = [v]
        self.internalConnectionSet = set()
        self.externalConnectionSet = set(self.graph[v]['n'])


    def getInternalConnectionSet(self):
        return self.internalConnectionSet

    def getExternalConnectionSet(self):
        return self.externalConnectionSet

    def getNodeList(self):
        return self.list

    def getBetaScore(self):
        return  (len(self.getInternalConnnectionSet())-len(self.getExternalConnectionSet()))\
                    / len(self.getNodeList())

    def copyNode(self,v):
        self.list = v.getNodeList()
        self.internalConnectionSet = v.getInternalConnectionSet()
        self.externalConnectionSet = v.getExternalConnectionSet()

    @staticmethod
    def mergeNode(graph,NodeA,NodeB):
        mergedNode = Node(graph,None)
        mergedNode.internalConnectionSet = NodeA.getInternalConnectionSet() | NodeB.getInternalConnectionSet() | \
                                           (NodeA.getExternalConnectionSet() & NodeB.getExternalConnectionSet())
        mergedNode.externalConnectionSet = NodeA.getExternalConnectionSet() ^ NodeB.getExternalConnectionSet()
        mergedNode.list = NodeA.getNodeList() + NodeB.getNodeList()



class UFS:
    def __init__(self,nodelist):
        for node in nodelist:
            self.fa[node] = node

    def find(self,x):
        if self.fa[x] == x:
            return x
        else:
            self.fa[x] = self.find(self.fa[x])
            return self.fa[x]

    def union(self,x,y):
        self.fa[x] = y
        return y