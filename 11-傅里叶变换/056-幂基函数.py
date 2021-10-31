import sympy as sp

"""
在区间[left,right]上求一组正交多项式，若模长为1，则成为标准正交多项式。  

正交多项式还可以带权，integral(f1*f2*w)=0,成为区间region上的带权正交多项式。  

给定区间，求n阶正交多项式，存在2**n种组合。  
"""
a = []

x = sp.symbols('x')

region = (0, 1)


def get(n):
    k = [sp.Symbol(f"k{i}") for i in range(n + 1)]
    y = 0
    for i in range(n + 1):
        y = y + k[i] * x ** i
    return k, y


def solve(y, k):
    system = [
        sp.integrate(y * y, (x, *region)) - 1,  # 模长为1
    ]
    for i in a:
        now = sp.integrate(y * i, (x, *region))
        system.append(now)
    ans = sp.solve(system, k)
    return ans


def main():
    for i in range(0, 10):
        k, y = get(i)
        ans = solve(y, k)
        print('每次求新函数都会得到2组解', len(ans))
        ans = ans[1]
        yy = y.subs({kk: vv for kk, vv in zip(k, ans)})
        a.append(yy)
        print(i, yy)


main()
