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
    term1 = 2 * F_rec(n - 1) / get_fact(n)
    term2 = F_rec(n - 3) / get_fact(2 * n)
    return sign * (term1 + term2)

def F_iter(n):
    if n < 2:
        return 1
    f = [1, 1, 1] 
    
    for i in range(2, n + 1):
        sign = -1 if i % 2 else 1
        if i == 2:
            term1 = 2 * f[1] / get_fact(i)
            term2 = 1 / get_fact(2 * i)  
        else:
            term1 = 2 * f[2] / get_fact(i)
            term2 = f[0] / get_fact(2 * i)
        new_val = sign * (term1 + term2)
        
        if i >= 2:
            f[0], f[1], f[2] = f[1], f[2], new_val
    
    return f[2]

def compare(n_max):
    print(f"{'n':<3} | {'Итерационное':<22} | {'Рекурсия':<32} | {'Время итерации':<19} | {'Время рекурсии':<19}")
    print("-" * 110)
    for n in range(n_max + 1):
        try:
            start = time.perf_counter()
            fi = F_iter(n)
            t1 = (time.perf_counter() - start) * 1000

            start = time.perf_counter()
            fr = F_rec(n)
            t2 = (time.perf_counter() - start) * 1000

            print(f"{n:<3} | {fi:<22.14e} | {fr:<32.14e} | {t1:<19.5f} | {t2:<19.5f}")
        except RecursionError:
            print(f"{n:<3} | {'-'*22} | {'RecursionError':<32} | {'-'*19} | {'-'*19}")

if __name__ == "__main__":
    compare(20)
