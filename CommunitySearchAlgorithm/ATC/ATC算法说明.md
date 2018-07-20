# ATC模型-算法总结

## DEFINATION
略去
## PROBLEM
给一个G(V,E)，查询点集Q=(Vq,Wq)，两个参数k,d，找到一个ATC H，满足：
1) H是一个(k,d) Truss
2) 满足1)的基础上，有一个最大的Attribute Score f(H,Wq)

## ALGORITHM
1) Steiner：计算覆盖Q的斯坦纳树T
2) ExtendertoGt：将T拓展，得到满足一定条件的子图Gt
3) BULK：使用BULK算法，轮次删除Gain值最小的一批节点，然后进行KDTrussMaintain维护KD-Truss的性质。

### Details
1) Steiner：计算斯坦纳树时的,e边权设置为1+求和 w属于Wq（lamba*(maxTE(G)-TE(G nodes with w)))
2) ExtendertoGt：根据AttributeScore的值，向着其值增加最多的方向进行bfs拓展（这里不懂作者所说的方法）
3) BULK：根据kdtruss的性质进行维护，删除点边知道Q中的节点不再联通（这里不懂作者所说的如何进行快速地同时维护SupE和distG的方法，但是由于缩图之后图的sz不大因此有着比较大的自由发挥空间）
4) gain函数的计算，粗略将删除v的代价记为删除v与其相邻k-1度的点之后attributescore差值
5) 参数设置：如果kd没有预制，k设置为覆盖Q的最大k-truss，d设置为distG，ertral进行每次删点的个数控制。


## REFERENCE
[Attribute-Driven Community Search]("http://www.vldb.org/pvldb/vol10/p949-huang.pdf")