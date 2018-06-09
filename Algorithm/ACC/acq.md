# ACQ模型算法总结

## PROBLEM
(ACQ-Attributed Community Query) 给定一个G(V,E)，一个正整数k，q属于V，一个W(V)的子集S，要求返回一个Gq的集合，集合中的Gq满足：
1) q属于Gq
2) 任意点的度数>=k
3) 要求Gq中的点共享的存在于S中的属性尽可能多

## ALGORITHM

### k-CORE DECOMPOSITION
分解算法计算coreG[v]，计算每个节点的deg，根据deg递增的顺序逐步删除节点

### CL-TREE BUILD
构建一个CLtree树，所谓cltree树指的是每一个节点代表一个k-core，由于k-core与k+1-core的包含关系，形成一棵树，树的节点经过压缩，父节点的全部节点是其子节点的节点集合的并集。其中树的节点保存invertedList信息，记录一个节点中属性值对应的节点。
<br> 从k大的节点开始构造，利用加了一个属性anchor的并查集进行树节点集合的合并。之所以追加anchor属性是为了节点之间的连边。

### INC-S
利用CL-TREE简化操作
<br> 采用递增的顺序由单个S中的元素开始构造S‘
<br> 对于每个S’验证是否存在满足S‘的Gk[S']
<br> 首先在CLTREE上找到一条路径，这条路径从包含q的节点开始，向上寻找到coreG=k为止，所有的操作都在这条路径上的节点进行
<br> 对于一个<S’,c>判断是否可行：从R[c]开始判断是否存在G能够覆盖S'，如果有的话，讨论Gk[S']
<br> 拓展：根据已经可行的子集S1,S2构造新的St，如果S1和S2只存在一个不同，则生成候选st，st是两者的并集，则生成<St,max{,}>