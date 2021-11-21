import numpy as np

"""
无向连通图有n个结点，每个结点有k条边，求这个拓扑图。

只有求出拓扑图之后，才能够使用pytorch求正n面体。有了拓扑图，设定好各个边的长度，就能够求出一个具体的体来。

这种方法比较暴力，很难求出结果。  
"""
n = 6
k = 4
a = np.zeros((n, n), dtype=np.bool)


def set_nk(nn, kk):
    global n, k, a
    n = nn
    k = kk
    a = np.zeros((n, n), dtype=np.bool)


ans = None


def check():
    global ans
    good = np.all(np.count_nonzero(a, axis=0) == k) and np.all(np.count_nonzero(a, axis=1) == k)
    if not good:
        return False
    con = np.zeros(n, dtype=np.bool)
    q = [0]
    i = 0
    con[0] = True
    while i < len(q):
        for j in np.argwhere(a[q[i]]).reshape(-1):
            if not con[j]:
                con[j] = True
                q.append(j)
        i += 1
    if len(q) == n:
        ans = a.copy()
        return True
    return False


def go(x, y):
    if x == n:
        if check():
            return True
        return False
    if y == x:
        return go(x + 1, 0)
    if np.count_nonzero(a[x]) == k:
        return go(x + 1, 0)
    if np.count_nonzero(a[:, y]) == k:
        return go(x, y + 1)
    a[x, y] = 1
    a[y, x] = 1
    ans = go(x, y + 1)
    a[x, y] = 0
    a[y, x] = 0
    if ans:
        return ans
    ans = go(x, y + 1)
    if ans:
        return True
    return False


def main():
    global n, k
    ans_list = []
    for i, j in ((4, 3), (6, 4), (8, 3), (20, 5), (12, 3)):
        set_nk(i, j)
        print('solving', n, k)
        go(0, 0)
        ans_list.append(ans.copy())
        print(ans)


def test():
    set_nk(4, 3)
    go(0, 0)


main()
