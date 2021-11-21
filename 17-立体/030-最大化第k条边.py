import numpy as np
import torch

"""
基于最大化最小边的原理，求正n面体的坐标。  

这样做需要一个前置条件：求出正多面体中的所有边，这就需要先生成正多面体的拓扑图。 

"""


def solve(n, k):
    a = torch.rand((n, 2))
    a.requires_grad = True

    def forward():
        p = torch.column_stack((torch.cos(a[:, 0]) * torch.cos(a[:, 1]), torch.cos(a[:, 0]) * torch.sin(a[:, 1]), torch.sin(a[:, 0])))
        edges = []
        for i in range(n):
            dis_list = []
            for j in range(n):
                if j == i:
                    continue
                dis_list.append(torch.linalg.norm(p[j] - p[i]))
            dis_list = np.array(dis_list)
            ind = np.argsort(dis_list)
            edges.extend(dis_list[ind[:k]])
        ind = np.argmin(edges)
        return -edges[ind], p, edges

    optimizer = torch.optim.Adam([a], lr=1e-3)
    i = 0
    while i < 10000:
        i += 1
        optimizer.zero_grad()
        y, p, edges = forward()
        y.backward(retain_graph=True)
        optimizer.step()
        if i % 1000 == 0:
            print(i, y, edges)
    return a


def main():
    ans = []
    for n, k in ((4, 3), (6, 4), (8, 3), (12, 3), (20, 5)):
        a = solve(n, k)
        ans.append(a)
        print(a)
    print(ans)


main()
