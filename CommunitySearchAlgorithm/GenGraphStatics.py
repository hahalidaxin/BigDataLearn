import AlgorithmATC.ATindex as ATI


def cedge(u,v):
    return min(u,v), max(u,v)


def gengraphstatics(graph):
    V = len(graph)
    # E = sum(len(graph[v][0]) for v in graph)/2

    edgedict = {}
    for v in graph:
        for u in graph[v][0]:
            edgedict[cedge(u, v)] = 1
    E = len(edgedict)

    dmax = max(len(graph[v][0]) for v in graph)
    Tao = max(ATI.StructuralTrussness(graph)[0].values())
    attrdict = {}
    for v in graph:
        for w in graph[v][1]:
            attrdict[w] = 1
    A = len(attrdict)
    attrV = sum(len(graph[v][1]) for v in graph)
    print("V: ",V)
    print("E: ",E)
    print("dmax: ",dmax)
    print("Tao: ",Tao)
    print("A: ",A)
    print("attrV: ",attrV)
    print(V, E, dmax, Tao, A, attrV)

if __name__ == "__main__":
    gengraphstatics(EXT.tempt_nodes_information)