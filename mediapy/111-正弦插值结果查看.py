import numpy as np
import pylab as plt
import sympy as sp
from sympy import atan2, sqrt

x1, x2, y1, y2, y1_, y2_ = sp.symbols("x1 x2 y1 y2 y1_ y2_")
ans = [(
    sqrt((-y1_ ** 2 + y2_ ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)) * (-y1 ** 2 * y2_ ** 2 + y1_ ** 2 * y2 ** 2) / (y1_ ** 2 - y2_ ** 2), (atan2(y1 * sqrt((-y1_ ** 2 + y2_ ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)), -y1_ * sqrt((y1 ** 2 - y2 ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2))) - atan2(y2 * sqrt((-y1_ ** 2 + y2_ ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)), -y2_ * sqrt((y1 - y2) * (y1 + y2) / ((y1 * y2_ - y1_ * y2) * (y1 * y2_ + y1_ * y2))))) / (x1 - x2),
    (x1 * atan2(y2 * sqrt((-y1_ ** 2 + y2_ ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)), -y2_ * sqrt((y1 - y2) * (y1 + y2) / ((y1 * y2_ - y1_ * y2) * (y1 * y2_ + y1_ * y2)))) - x2 * atan2(y1 * sqrt((-y1_ ** 2 + y2_ ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)), -y1_ * sqrt((y1 ** 2 - y2 ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)))) / (x1 - x2)), (
    sqrt((-y1_ ** 2 + y2_ ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)) * (-y1 ** 2 * y2_ ** 2 + y1_ ** 2 * y2 ** 2) / (y1_ ** 2 - y2_ ** 2), (atan2(y1 * sqrt((-y1_ ** 2 + y2_ ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)), y1_ * sqrt((y1 ** 2 - y2 ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2))) - atan2(y2 * sqrt((-y1_ ** 2 + y2_ ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)), y2_ * sqrt((y1 - y2) * (y1 + y2) / ((y1 * y2_ - y1_ * y2) * (y1 * y2_ + y1_ * y2))))) / (x1 - x2),
    (x1 * atan2(y2 * sqrt((-y1_ ** 2 + y2_ ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)), y2_ * sqrt((y1 - y2) * (y1 + y2) / ((y1 * y2_ - y1_ * y2) * (y1 * y2_ + y1_ * y2)))) - x2 * atan2(y1 * sqrt((-y1_ ** 2 + y2_ ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)), y1_ * sqrt((y1 ** 2 - y2 ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)))) / (x1 - x2)), (
    sqrt((-y1_ ** 2 + y2_ ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)) * (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2) / (y1_ ** 2 - y2_ ** 2), (atan2(-y1 * sqrt((-y1_ ** 2 + y2_ ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)), y1_ * sqrt((y1 ** 2 - y2 ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2))) - atan2(-y2 * sqrt((-y1_ ** 2 + y2_ ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)), y2_ * sqrt((y1 - y2) * (y1 + y2) / ((y1 * y2_ - y1_ * y2) * (y1 * y2_ + y1_ * y2))))) / (x1 - x2),
    (x1 * atan2(-y2 * sqrt((-y1_ ** 2 + y2_ ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)), y2_ * sqrt((y1 - y2) * (y1 + y2) / ((y1 * y2_ - y1_ * y2) * (y1 * y2_ + y1_ * y2)))) - x2 * atan2(-y1 * sqrt((-y1_ ** 2 + y2_ ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)), y1_ * sqrt((y1 ** 2 - y2 ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)))) / (x1 - x2)), (
    sqrt((-y1_ ** 2 + y2_ ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)) * (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2) / (y1_ ** 2 - y2_ ** 2),
    (atan2(-y1 * sqrt((-y1_ ** 2 + y2_ ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)), -y1_ * sqrt((y1 ** 2 - y2 ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2))) - atan2(-y2 * sqrt((-y1_ ** 2 + y2_ ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)), -y2_ * sqrt((y1 - y2) * (y1 + y2) / ((y1 * y2_ - y1_ * y2) * (y1 * y2_ + y1_ * y2))))) / (x1 - x2),
    (x1 * atan2(-y2 * sqrt((-y1_ ** 2 + y2_ ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)), -y2_ * sqrt((y1 - y2) * (y1 + y2) / ((y1 * y2_ - y1_ * y2) * (y1 * y2_ + y1_ * y2)))) - x2 * atan2(-y1 * sqrt((-y1_ ** 2 + y2_ ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)), -y1_ * sqrt((y1 ** 2 - y2 ** 2) / (y1 ** 2 * y2_ ** 2 - y1_ ** 2 * y2 ** 2)))) / (x1 - x2))]


def solve(X1, X2, Y1, Y2, Y1_, Y2_, ind):
    A, w, phi = ans[ind]
    ma = {x1: X1, x2: X2, y1: Y1, y2: Y2, y1_: Y1_, y2_: Y2_}
    res = [complex(v.evalf(subs=ma)) for v in (A, w, phi)]
    res = np.array(res)
    return res


def main():
    AA, ww, phiphi = 2, 1.5, 1
    xx = np.linspace(2 * np.pi / ww, np.pi / ww, 100)
    yy = AA * np.sin(ww * xx + phiphi)
    i, j = np.random.choice(np.arange(len(xx)), 2)
    if i > j:
        i, j = j, i
    X1, X2, Y1, Y2, Y1_, Y2_ = xx[i], xx[j], yy[i], yy[j], (yy[i] - yy[i - 1]) / (xx[i] - xx[i - 1]), (yy[j + 1] - yy[j]) / (xx[j + 1] - xx[j])
    print('计算斜率', Y1_, Y2_, AA * ww * np.cos(ww * np.array([xx[i], xx[j]]) + phiphi))
    print("真实答案", AA, ww, phiphi)
    # x = np.linspace(X1, X2, 100)

    for k in range(len(ans)):
        A, w, phi = solve(X1, X2, Y1, Y2, Y1_, Y2_, k)
        print(i, A, w, phi, type(A), type(w), type(phi))
        y = A * np.sin(w * xx + phi)
        plt.plot(xx, y, label=f'{k}')
        plt.vlines([xx[i], xx[j]], np.min(y), np.max(y))
    plt.plot(xx, yy, label='real')
    plt.legend()
    plt.show()


main()
