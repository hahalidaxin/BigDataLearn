import collections

a = [1,1,1,1,2,1213,12,1,2,3,2,2,21,3,3,12]
counter = collections.Counter(a)
list = sorted(counter.items(),key=lambda x:-x[1])
print(list[0][0])
print(list)