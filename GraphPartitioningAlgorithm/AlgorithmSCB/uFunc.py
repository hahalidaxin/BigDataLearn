

# 计算将节点v从Server A移动到Server B的收益
def SCB(graph,v,A,B):
    PDSN_B, PDSN_nAB, PSSN, DSN_nAB, Bonus, Penalty = 0, 0, 0, 0, 0, 0
    for u in graph[v]['n']:
        if graph[u]['b']==A:
            Penalty = -1
            pssn = 1
            for neiu in graph[u]['n']:
                if graph[neiu]['b']!=A:
                    pssn = 0
                    break
            if pssn: PSSN += 1
        elif graph[u]['b']==B:
            Bonus = 1
            pdsn_b_flag = 1
            for neiu in graph[u]['n']:
                if graph[neiu]['b']==A:
                    pdsn_b_flag = 0
                    break
            if pdsn_b_flag: PDSN_B += 1
        else:
            DSN_nAB += 1
            pdsn_nab_flag = 1
            for neiu in graph[u]['n']:
                if graph[neiu]['b']==A:
                    pdsn_nab_flag = 0
                    break
            if pdsn_nab_flag: PDSN_nAB += 1
    print("PDSN:"+PDSN_B+" PDSN_nAB:"+PDSN_nAB+" PSSN:"+PSSN+" DSN_nAB:"+DSN_nAB+" Bonus:"+Bonus+" Penalty:"+Penalty)
    print("SCB: "+(PDSN_B + PDSN_nAB - PSSN - DSN_nAB + Bonus + Penalty))
    return PDSN_B + PDSN_nAB - PSSN - DSN_nAB + Bonus + Penalty


def readData():
    filepath = "../ExperimentDatasets/Ego/ego-Facebook/facebook/"
    f = open(filepath+"0.edges")
    graph = {}
    while True:
        line = f.readline()
        if len(line)==0: break
        u,v = line.strip().split()
        if graph.get(u) is None: graph[u]=[]
        if graph.get(v) is None: graph[v]=[]
        graph[u].append(v)
        graph[v].append(u)
    return graph


def testLoadBalance(servers,conE):
    keys_servers = servers.keys()
    for i in range(len(keys_servers)):
        svi = servers[keys_servers[i]]
        for j in range(i+1,len(keys_servers)):
            svj = servers[keys_servers[j]]
            if abs(svi.getload()-svj.getload()) > conE:
                return False
    return True


def testLoadAterTrans(servers,conE,iniSv,tarSv,nodeV):
    for sv in [tarSv,iniSv]:
        for svj in servers:
            if sv == svj: continue
            diff = sv.getload()-svj.getload()
            if sv == iniSv:
                diff -= tarSv.S[nodeV]
            if sv == tarSv:
                diff += tarSv.S[nodeV]
            if abs(diff) > conE:
                return False
    return True

