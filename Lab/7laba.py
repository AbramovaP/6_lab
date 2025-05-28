import math
import time
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

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

def compare_performance():
    try:
        n_max = int(max_n_entry.get())
        if n_max < 0:
            raise ValueError("n должно быть неотрицательным")
    except ValueError as e:
        messagebox.showerror("Ошибка ввода", str(e))
        return
    
    output_text.delete(1.0, tk.END)
    
    header = (f"{'n':<3} | {'Итерационное':<22} | {'Рекурсия':<32} | "
             f"{'Время итерации (мс)':<19} | {'Время рекурсии (мс)':<19}\n")
    output_text.insert(tk.END, header)
    output_text.insert(tk.END, "-"*120 + "\n")
    
    for n in range(n_max + 1):
        try:
            start_iter = time.perf_counter()
            fi = F_iter(n)
            time_iter = (time.perf_counter() - start_iter) * 1000
            
            start_rec = time.perf_counter()
            fr = F_rec(n)
            time_rec = (time.perf_counter() - start_rec) * 1000 
            
            line = (f"{n:<3} | {fi:<22.14e} | {fr:<32.14e} | "
                   f"{time_iter:<19.5f} | {time_rec:<19.5f}\n")
            
        except RecursionError:
            line = (f"{n:<3} | {'-'*22} | {'RecursionError':<32} | "
                   f"{'-'*19} | {'-'*19}\n")
        except Exception as e:
            line = (f"{n:<3} | {'Error':<22} | {str(e):<32} | "
                   f"{'-'*19} | {'-'*19}\n")
        
        output_text.insert(tk.END, line)
        output_text.see(tk.END)

root = tk.Tk()
root.title("Сравнение времени выполнения")
root.geometry("900x600+400+200")

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

control_frame = ttk.Frame(main_frame)
control_frame.pack(fill=tk.X, pady=5)

ttk.Label(control_frame, text="Максимальное n:", foreground="#01579B").pack(side=tk.LEFT)
max_n_entry = ttk.Entry(control_frame, width=10)
max_n_entry.pack(side=tk.LEFT, padx=5)
ttk.Button(control_frame, text="Сравнить", command=compare_performance).pack(side=tk.LEFT)

output_frame = ttk.Frame(main_frame)
output_frame.pack(fill=tk.BOTH, expand=True)

output_text = scrolledtext.ScrolledText(
    output_frame,
    wrap=tk.WORD,
    width=100,
    height=25,
    font=('Consolas', 10)
)
output_text.pack(fill=tk.BOTH, expand=True)

root.mainloop()
