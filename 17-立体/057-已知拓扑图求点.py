import numpy as np
import torch
from tqdm import tqdm

"""
给出拓扑图来，验证能否找出点来。  
对于正十二面体，比较难找出来，运行花费时间比较长。正十二面体中部有犬牙交互之态，这个问题很有可能是非凸的，这就导致点移动的时候无法往最优结构上移动。  
"""
CUBES = [
    [[1, 0], [2, 1], [3, 0], [3, 2], [2, 0], [3, 1]],
    [[1, 0], [7, 3], [6, 4], [6, 2], [5, 4], [7, 5], [5, 1], [7, 6], [2, 0], [4, 0], [3, 2], [3, 1]],
    [[1, 0], [2, 0], [2, 1], [3, 0], [3, 1], [4, 0], [4, 2], [4, 3], [5, 1], [5, 2], [5, 3], [5, 4]],
    [[19, 16], [11, 8], [12, 9], [17, 14], [18, 15], [13, 10], [14, 3], [15, 6], [8, 6], [8, 7], [15, 4], [9, 5], [9, 7], [10, 3], [16, 1], [10, 7], [13, 6], [13, 2], [11, 4], [11, 5], [12, 3], [14, 2], [16, 5], [12, 1], [17, 0], [17, 1], [18, 2], [19, 4], [19, 0], [18, 0]],
    [[1, 0], [7, 1], [7, 3], [7, 5], [8, 1], [8, 2], [8, 3], [11, 9], [9, 3], [9, 4], [9, 8], [10, 4], [10, 5], [10, 6], [10, 9], [11, 3], [11, 5], [11, 7], [7, 0], [6, 5], [8, 4], [11, 10], [6, 2], [2, 0], [6, 0], [4, 2], [6, 4], [3, 1], [2, 1], [5, 0]]]


def solve(WHICH):
    n = np.max(CUBES[WHICH]) + 1
    edges = np.array(CUBES[WHICH])
    a = torch.rand((n, 2))
    a.requires_grad = True

    def forward():
        p = torch.column_stack((torch.cos(a[:, 0]) * torch.cos(a[:, 1]), torch.cos(a[:, 0]) * torch.sin(a[:, 1]), torch.sin(a[:, 0])))
        dis = torch.linalg.norm(p[edges[:, 0]] - p[edges[:, 1]], dim=1)
        y = -torch.min(dis)
        return y, dis

    optimizer = torch.optim.Adam([a], lr=1e-4)
    for i in tqdm(range(int(1e9))):
        optimizer.zero_grad()
        y, dis = forward()
        y.backward(retain_graph=True)
        optimizer.step()
        if i % 10000 == 0:
            print(f"solving {WHICH} iter {i} y={y} {torch.max(dis) - torch.min(dis)}")
            if torch.max(dis) - torch.min(dis) < 1e-2:
                break
    y, dis = forward()
    print("最终结果", y, dis)
    return a.data


ans = []
for i in range(4,len(CUBES)):
    resp = solve(i)
    ans.append(resp)
