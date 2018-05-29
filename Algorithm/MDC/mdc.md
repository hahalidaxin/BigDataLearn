# MDC算法总结

## Problem2
### 问题描述
给定一个无向图G(V,E)，给定一系列顶点 Q⊂V，并且给定一个距离限制d，要求找出一个G的生成子图H(Vh,Eh)，满足如下条件：
* Vh 包含 Q
* H是连通的
* Dq(H)≤d
* 最小度函数fm(H)在所有H的可能方案中最大。

其中的Dq定义省略。

### 算法描述
GREEDY算法（不考虑d的限制）：
* 初始设置G0=G，每一步删除G中的一个节点
* 在第t步中，我们考虑在Gt-1中拥有最小度的节点u
* 将节点u删除，并删除与之相连的边，得到Gt
* 停止条件（设迭代次数为T）：
    1) 删除的u是Q中的节点
    2) 删除u之后Q中的节点不再连通
* 返回最优解：对于第t步得到的图Gt，定义G‘t为Gt包含Q的所有节点的子图，fm(G)代表G的最小度，则GO = arg max{fm(G't)} t⊂{0,1,2,...T-1}

## Problem3（考虑d的限制+一般化）
### 问题描述
给定一个无向图G(V,E)，给定一系列顶点 Q⊂V： f：Sv X V -> R,且f是一个单调不增函数，同样有一系列单调不增函数f1,f2...fk，要求找到G的一个生成子图H，使得H满足：

* 满足属性f1...fk
* 最大化所有子图H的f函数

### 算法描述
GREEDYGEN算法：
* 初始设置G0=G，每一步删除G中的一个节点
* 在第t步中，我们考虑：
    1) 在Gt-1中违背属性fj,j⊂[1,k]的节点u
    2) 如果不存在u，删除满足f(G,v)最小的节点
* 将节点u删除，并删除与之相连的边，得到Gt
* 停止条件（设迭代次数为T）：图G为空
* 返回最优解：返回子图Gt,t⊂[0,T-1]，Gt需要满足可以最大化f函数
> ps:Sv=2^G，f(G,v)是一个关于图G与v的一个节点函数。fj是1时代表满足属性，是0时代表不满足属性。

> 关于G最大化f函数的定义，需要满足min<sub>v⊂V(G)</sub>{f(G,v)}>=min<sub>v⊂V(H)</sub>{f(H,v)}。

## Problem4
### 问题描述
Problem2 + **|V<sub>H</sub>|<k** ，子集个数限制
> 经证明，该问题为一个NP-hard问题。
### 算法描述
#### GREEDYDIST算法
* 利用GREEDYGEN作为子程序进行迭代，根据size与d的单调性一致的特点，每次迭代提供一个d，迭代的终止条件：
    1) size满足限制
    2) Q中的节点已经不再连通
* 返回最优解：返回执行过程中产生的最小的图。
* 关于size的递减方法：因为作为GREEDYGEN输出的图的大小是单调的，所以可以用二分查找的方法尝试d的值。


#### GREEDYFAST算法
* 预处理：将原图局限为保留k’个到Q最近的顶点，k'被定义的尽可能小
* 在新图上运行GREEDY算法。

## REFERENCES
* M. Sozio and A. Gionis. The community-search problem and how to plan a successful cocktail party. In KDD, pages 939–948, 2010.