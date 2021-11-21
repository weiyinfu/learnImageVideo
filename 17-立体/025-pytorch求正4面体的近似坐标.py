import torch

"""
在球上选择4个点，让这四个点之间的最小距离尽量大，最终就会得到正四面体。

下面的代码哪里错了，为啥无法反向传播
"""
n = 4
a = torch.rand((4, 2))
a.requires_grad = True


def forward():
    p = torch.column_stack((torch.cos(a[:, 0]) * torch.cos(a[:, 1]), torch.cos(a[:, 0]) * torch.sin(a[:, 1]), torch.sin(a[:, 0])))
    b = []
    for i in range(len(a)):
        for j in range(i):
            b.append(torch.linalg.norm(p[i] - p[j]))
    b = torch.tensor(b)
    b.requires_grad = True
    y = torch.min(b)
    return y


optimizer = torch.optim.Adam([a], lr=1e-1)
for i in range(10):
    optimizer.zero_grad()
    y = forward()
    y.backward(retain_graph=True)
    optimizer.step()
    print(y)
