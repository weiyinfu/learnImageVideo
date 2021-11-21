import torch
from tqdm import tqdm
"""
球面选4点，最大化点之间的最小距离，最终四个点之间的距离就会尽量原理，就得到了正四面体。
"""
n = 4
a = torch.rand((4, 2))
a.requires_grad = True
print(a.requires_grad, 'a')

b = []
for i in range(len(a)):
    for j in range(i):
        b.append((i, j))
b = torch.tensor(b)


def forward():
    p = torch.column_stack((torch.cos(a[:, 0]) * torch.cos(a[:, 1]), torch.cos(a[:, 0]) * torch.sin(a[:, 1]), torch.sin(a[:, 0])))
    y = torch.min(torch.linalg.norm(p[b[:, 0]] - p[b[:, 1]], dim=1))
    return -y, p


optimizer = torch.optim.Adam([a], lr=1e-3)
for i in tqdm(range(10000)):
    optimizer.zero_grad()
    y, p = forward()
    y.backward(retain_graph=True)
    optimizer.step()
    if i % 1000 == 0:
        print(y)
        print(torch.linalg.norm(p[b[:, 0]] - p[b[:, 1]], dim=1))

print(a)
