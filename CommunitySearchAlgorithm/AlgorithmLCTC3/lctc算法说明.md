# LCTC模型-算法总结

## DEFINATION

* **k-truss**
<br> G的一个**联通子图H**，且H的任意一条边都包含在至少k-2个三角形中。

* **TRUSSNESS**
1) 图的trussness：t(H)=min<sub>e∈E(H)</sub>{sup<sub>H</sub>(e)}，用来衡量一个图的紧密程度
2) 边的trussness：t(e)=max<sub>H⊆G^e∈E(H)</sub>{t(H)}， 包含边e的k最大的一个truss
3) 点的trussness：t(v)=max<sub>H⊆G^v∈V(H)</sub>{t(H)}，包含v的k最大的一个truss

* **QUERY DISTANCE**
<br>dist<sub>G</sub>(u,v)定义为在图G中两点uv之间的最短路距离。
<br>dist<sub>G</sub>(v,Q)=max<sub>q∈Q</sub>dist<sub>G</sub>(v,q) 一个点到Q中所有点最短距离 中的最大值
<br>dist<sub>G</sub>(H,Q)=max<sub>u∈H</sub>dist<sub>G</sub>(u,Q)

* **GRAPH DIAMETER**
<br>diam(G) = max<sub>u,v∈G</sub>{dist<sub>G</sub>(u,v)}

* **CTC (closest truss community)**

1) 联通的k-truss，覆盖所有的查询顶点Q，且有k最大
2) **满足1)条件的基础上**，直径最小。（应对free rider effect)


* **其他**
<br> sup<sub>G</sub>(e)为图G中e所在的三角形的个数
<br> 性质：在一个k-truss中，deg(u)>=k-1

## PROPERTIES
* **LEMMA 1**
<br> 对于一个满足CTC定义的联通k-truss而言，我们有k<={t(q1),...,t(qr)}

* **LEMMA 2**
<br>dist<sub>G</sub>(G,Q)<=diam(G)<=2dist<sub>G</sub>(G,Q)


## ALGORITHM BASIC
### BASIC FRAMEWORK
> **FIND G0** : 找到一个最大的联通k-truss，要去满足包含Q，且k最大
> <br>l=0 ; 定义Gl = k-truss
> <br>进入迭代，每次迭代删除dist<sub>G</sub>(v,Q)最大的节点，删除该节点和与之相连的边
> <br>**K-truss Maintenance** : 维护k-truss的属性 ; l+=1
> <br>迭代终止条件：不再含有包含Q的联通子图
> <br>返回答案：arg min{dist<sub>Gl</sub>(G,Q)} 所有Gl之中 dist<sub>Gl</sub>(G,Q)最小的那个Gl

### FIND G0
> k = min{t(q1)...t(qr)}
> <br> V(G0)={} ,Sk=Q；对于一个给定的k，我们处理每一个v∈Sk，按照BFS的方法访问它的每一个相邻节点，然后添加与之相邻的满足k<=t(u,v)<=kmax的边进入G0，kmax是所有没有被访问的边的最大可能trussness。
> <br> 同时如果相邻节点u没有在Sk中，将u加入到Sk中。
> <br> 访问完所有相邻节点之后，将v加入到Sl，l=max{t(u,v),u是相邻节点，t(u,v)<k}
> <br> 检查在G0中Q是否已经联通，如果联通则迭代结束，否则，k-=1，继续迭代;

### K-TRUSS MAINTAIN
> 需要删除节点集合Vd之后任然返回一个k-truss
> <br> 把所有的与Vd顶点相连的边放入S节点
> <br> 对于每一条S中的边(u,v)，检查所有三角形uvw，sup(u,w)-1,sup(v,w)-1;对于每一条不属性S
中的边，如果sup(e)<k-2则加入S；
> <br> 在G中删除(u,v) 迭代终点S为空

## ALGORITHM LCTC
**Input:** 给定一个G(V,E)，Q   <br>
**Ouput:** 要求返回一个满足覆盖所有Q而且子图个数<=k，同时k-truss最大的子图。
1) 根据G构造一棵斯坦纳树，斯坦纳树应用近似算法，是一棵覆盖所有的Q且相对dist最小的树
2) 拓展斯坦纳树T成为新图Gt，拓展的边需要满足truss比T中最小边truss大。同时需要满足节点个数限制
3) 分解算法计算G0，
4) 在G0上应用BULKDELETE算法，通过删边构造k-truss，选择其中直径最小的k-truss


## REFERENCES
 X. Huang, L. V. Lakshmanan, J. X. Yu, and H. Cheng. Approximate closest
community search in networks. PVLDB, 9(4):276–287, 2015