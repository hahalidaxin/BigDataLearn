from collections import defaultdict

# 根据func(x) 对x进行排序 其中func(x)需要是数字
def bulksort(ls,func=lambda x:x):
    _max = max(func(x) for x in ls)
    _min = min(func(x) for x in ls)
    mapcompo = defaultdict(list)
    for x in ls:
        mapcompo[func(x)].append(x)
    s = [0 for i in range(_min, _max + 1)]
    for i in ls:
        s[func(i) - _min] += 1
    current = _min
    n = 0
    for i in s:
        while i > 0:
            ls[n] = current
            i -= 1
            n += 1
        current += 1
    index = defaultdict(int)
    ans = []
    for val in ls:
        ans.append(mapcompo[val][index[val]])
        index[val] += 1
    return ans


def radix_sort(ls, d=3):
    for i in range(d):
        s = [[] for k in range(10)]
        for j in ls:
            s[int(j / (10 ** i)) % 10].append(j)
        re = [a for b in s for a in b]
    return re


if __name__ == "__main__":
    s = [3,5,2]
    a = [2,1,0]
    print(bulksort(a,lambda x:s[x]))