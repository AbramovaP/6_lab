import time
import itertools
import string

K = 3
T = 1

letters = list(string.ascii_letters)
digits = list(string.digits)
letters_and_digits = letters + digits

print("Часть 1: генерация всех возможных паролей")

def generate_passwords_algorithmic(K, T):
    result = []
    def backtrack(path, used, pos):
        if len(path) == K:
            if any(c in digits for c in path):
                result.append("".join(path))
            return
        candidates = letters if pos < T else letters_and_digits
        for ch in candidates:
            if ch not in used:
                path.append(ch)
                used.add(ch)
                backtrack(path, used, pos + 1)
                path.pop()
                used.remove(ch)
    
    backtrack([], set(), 0)
    return result

start_time = time.time()
passwords_alg = generate_passwords_algorithmic(K, T)
time_alg = time.time() - start_time
print(f"Алгоритмический способ: {len(passwords_alg)} паролей, время = {time_alg:.4f} сек")

def generate_passwords_functional(K, T):
    all_chars = list(letters_and_digits)
    valid_passwords = []

    for combo in itertools.permutations(all_chars, K):
        if all(c in letters for c in combo[:T]) and any(c in digits for c in combo):
            valid_passwords.append("".join(combo))
    return valid_passwords

start_time = time.time()
passwords_func = generate_passwords_functional(K, T)
time_func = time.time() - start_time
print(f"Функциональный способ: {len(passwords_func)} паролей, время = {time_func:.4f} сек")

print("\nЧасть 2: Усложнённое условие")
print("Ограничение: первая буква - заглавная.")
print("Целевая функция: минимизировать количество заглавных букв в пароле.")

def generate_optimized_passwords(K, T):
    result = []
    def backtrack(path, used, pos):
        if len(path) == K:
            if any(c in digits for c in path):
                if path[0] in string.ascii_uppercase:
                    result.append("".join(path))
            return
        candidates = letters if pos < T else letters_and_digits
        for ch in candidates:
            if ch not in used:
                path.append(ch)
                used.add(ch)
                backtrack(path, used, pos + 1)
                path.pop()
                used.remove(ch)

    backtrack([], set(), 0)
    return result

start_time = time.time()
optimized_passwords = generate_optimized_passwords(K, T)
time_opt = time.time() - start_time
print(f"С учётом ограничений: {len(optimized_passwords)} паролей, время = {time_opt:.4f} сек")

def fewest_uppercase(pw):
    return sum(1 for c in pw if c in string.ascii_uppercase)

best_password = min(optimized_passwords, key=fewest_uppercase)
print(f"Пароль с минимальным числом заглавных букв: {best_password}, количество заглавных = {fewest_uppercase(best_password)}")
