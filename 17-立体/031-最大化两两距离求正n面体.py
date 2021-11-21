import torch

"""
基于所有点之间的距离之和最大化
TODO:基于最大化体积的原理，求正n面体的坐标。  
"""


def solve(n, k):
    a = torch.rand((n, 2))
    a.requires_grad = True
    b = []
    for i in range(n):
        for j in range(n):
            b.append((i, j))
    b = torch.tensor(b)

    def forward():
        p = torch.column_stack((torch.cos(a[:, 0]) * torch.cos(a[:, 1]), torch.cos(a[:, 0]) * torch.sin(a[:, 1]), torch.sin(a[:, 0])))
        # 距离之和应该尽量大
        dis = torch.sum((p[b[:, 0]] - p[b[:, 1]]) ** 2)
        return -dis, p

    optimizer = torch.optim.Adam([a], lr=1e-3)
    i = 0
    while i < 10000:
        i += 1
        optimizer.zero_grad()
        y, p = forward()
        y.backward(retain_graph=True)
        optimizer.step()
        if i % 1000 == 0:
            print(i, y)
    return a


def main():
    ans = []
    for n, k in ((4, 3), (6, 4), (8, 3), (12, 3), (20, 5)):
        a = solve(n, k)
        ans.append(a)
        print(a)
    print(ans)


main()
