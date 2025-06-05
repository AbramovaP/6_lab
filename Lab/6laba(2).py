import math
import time

def get_fact(n):
    b = 1  
    if n == 0:
        return 1
    for i in range(2, n + 1):
        b = b * i
    return b

def F_rec(n):
    if n < 2:
        return 1
    sign = -1 if n % 2 else 1
    term1 = 2 * F_rec(n - 1) / math.factorial(n)
    term2 = F_rec(n - 3) / math.factorial(2 * n)
    return sign * (term1 + term2)

def F_iter(n):
    f = f0 = f1 = f2 = 1
    f2n = 2
    if n < 3:
        return 1
    for i in range(3, n + 1):
        f *= i        
        f2n *= (2*n)*(2*n-1)
        sign = -1 if i % 2 else 1
        f2, f1, f0 = f1, f0, sign * (2 * f1 /f  + f2 / f2n)
    return f0

def compare(n_max):
    print(f"{'n':<3} | {'Итерационное':<22} | {'Рекурсия':<27} | {'Время итерации':<19} | {'Время рекурсии':<19}")
    print("-" * 110)
    for n in range(n_max + 1):
        try:
            start = time.perf_counter()
            fi = F_iter(n)
            t1 = (time.perf_counter() - start) * 1000

            start = time.perf_counter()
            fr = F_rec(n)
            t2 = (time.perf_counter() - start) * 1000

            print(f"{n:<3} | {fi:<22.14e} | {fr:<27.14e} | {t1:<19.5f} | {t2:<19.5f}")
        except RecursionError:
            print(f"{n:<3} | {'-'*22} | {'RecursionError':<32} | {'-'*19} | {'-'*19}")

if __name__ == "__main__":
    compare(20)
