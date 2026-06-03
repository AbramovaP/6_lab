import tkinter as tk
import hashlib
import os

SIZE = 19
CELL = 30
WIN_W = SIZE * CELL
WIN_H = SIZE * CELL + 120
USERS_FILE = "users.txt"

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()

def load_users() -> dict:
    users = {}
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    login, pwd_hash = line.strip().split(":")
                    users[login] = pwd_hash
    return users

def save_user(login: str, pwd_hash: str):
    with open(USERS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{login}:{pwd_hash}\n")


def create_game_state():
    return {
        "pole": [[0 for _ in range(SIZE)] for _ in range(SIZE)],
        "game_over": False,
        "black_stones": 50
    }

def check_five(pole, x, y):
    for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
        cnt = 1
        for s in (1, -1):
            nx, ny = x, y
            while True:
                nx += dx * s
                ny += dy * s
                if 0 <= nx < SIZE and 0 <= ny < SIZE and pole[ny][nx] == 1:
                    cnt += 1
                else:
                    break
        if cnt == 5:
            return "win"
        if cnt > 5:
            return "overline"
    return None

def count_open(pole, x, y, length):
    total = 0
    for dx, dy in [(1, 0), (0, 1), (1, 1), (1, -1)]:
        cnt = 1
        open_ends = 0
        for s in (1, -1):
            nx, ny = x, y
            while True:
                nx += dx * s
                ny += dy * s
                if 0 <= nx < SIZE and 0 <= ny < SIZE:
                    if pole[ny][nx] == 1:
                        cnt += 1
                    elif pole[ny][nx] == 0:
                        open_ends += 1
                        break
                    else:
                        break
                else:
                    break
        if cnt == length and open_ends == 2:
            total += 1
    return total

def forbidden_move(pole, x, y):
    test_pole = [row[:] for row in pole]
    test_pole[y][x] = 1

    overline = check_five(test_pole, x, y) == "overline"
    threats = count_open(test_pole, x, y, 3) + count_open(test_pole, x, y, 4)

    return overline or threats >= 2

def has_legal_moves(pole):
    for y in range(SIZE):
        for x in range(SIZE):
            if pole[y][x] == 0 and not forbidden_move(pole, x, y):
                return True
    return False

def make_move(game_state, x, y):
    if game_state["game_over"]:
        return False, "Игра окончена"

    if not (0 <= x < SIZE and 0 <= y < SIZE):
        return False, "Координаты вне поля"

    if game_state["pole"][y][x] != 0:
        return False, "Клетка занята"

    if forbidden_move(game_state["pole"], x, y):
        return False, "Запрещённый ход"

    game_state["pole"][y][x] = 1
    game_state["black_stones"] -= 1

    res = check_five(game_state["pole"], x, y)
    if res == "win":
        game_state["game_over"] = True
        return True, "Победа! Построено 5 в ряд."

    if not has_legal_moves(game_state["pole"]):
        game_state["game_over"] = True
        return True, "Поражение. Нет допустимых ходов."

    if game_state["black_stones"] <= 0:
        game_state["game_over"] = True
        return True, "Камни закончились. Ничья."

    return True, f"Камней осталось: {game_state['black_stones']}"

def pass_move(game_state):
    if game_state["game_over"]:
        return False, "Игра окончена"
    game_state["game_over"] = True
    return True, "Ничья (пас)"

def draw_board(canvas):
    for i in range(SIZE):
        canvas.create_line(
            CELL // 2, CELL // 2 + i * CELL,
            WIN_W - CELL // 2, CELL // 2 + i * CELL
        )
        canvas.create_line(
            CELL // 2 + i * CELL, CELL // 2,
            CELL // 2 + i * CELL, WIN_W - CELL // 2
        )

def draw_stone(canvas, x, y):
    r = CELL // 2 - 2
    cx = x * CELL + CELL // 2
    cy = y * CELL + CELL // 2
    canvas.create_oval(cx - r, cy - r, cx + r, cy + r, fill="black")

def show_message_window(parent, title, message):
    win = tk.Toplevel(parent)
    win.geometry("400x100+730+420")
    win.title(title)
    tk.Label(
        win, text=message, font=("Arial", 14, "bold")
    ).place(x=50, y=20)
    tk.Button(win, text="ОК", command=win.destroy).place(x=160, y=60)
    return win

def main():
    root = tk.Tk()
    root.geometry(f"{WIN_W}x{WIN_H}+500+50")
    root.title("Рэндзю — движок")

    game_state = create_game_state()

    center_x = WIN_W // 2
    txt = tk.Label(root, text="Введите логин и пароль", font=("Arial", 14, "bold"))
    txt.place(x=center_x - 110, y=60)

    tk.Label(root, text="Логин", font=("Arial", 12, "bold")).place(x=center_x - 110, y=130)
    login_entry = tk.Entry(root, width=15, bd=3)
    login_entry.place(x=center_x - 30, y=130)

    tk.Label(root, text="Пароль", font=("Arial", 12, "bold")).place(x=center_x - 110, y=170)
    password_entry = tk.Entry(root, width=15, bd=3, show="*")
    password_entry.place(x=center_x - 30, y=170)

    canvas = None
    msg_label = None

    def start_game():
        nonlocal canvas, msg_label

        txt.place_forget()
        login_entry.place_forget()
        password_entry.place_forget()
        start_btn.place_forget()

        game_state.update(create_game_state())

        if canvas:
            canvas.destroy()

        canvas = tk.Canvas(root, width=WIN_W, height=WIN_W, bg="#f0d9b5")
        canvas.place(x=0, y=0)
        draw_board(canvas)

        if msg_label:
            msg_label.config(
                text=f"Ход чёрных. Камней осталось: {game_state['black_stones']}"
            )
        else:
            msg_label = tk.Label(
                root,
                text=f"Ход чёрных. Камней осталось: {game_state['black_stones']}",
                font=("Arial", 12, "bold")
            )
            msg_label.place(x=10, y=WIN_W + 5)

        def click(event):
            x = event.x // CELL
            y = event.y // CELL
            success, msg = make_move(game_state, x, y)
            if success and game_state["pole"][y][x] == 1:
                draw_stone(canvas, x, y)
            msg_label.config(text=msg)

        canvas.bind("<Button-1>", click)

        tk.Button(root, text="Пас", width=10,
                  command=lambda: msg_label.config(text=pass_move(game_state)[1])
                  ).place(x=WIN_W - 220, y=WIN_W + 5)

        tk.Button(root, text="Новая игра", width=12,
                  command=start_game
                  ).place(x=WIN_W - 120, y=WIN_W + 5)

    def register():
        login = login_entry.get().strip()
        password = password_entry.get().strip()

        if not login or not password:
            show_message_window(root, "Ошибка", 'Пустое поле "Логин" или "Пароль"')
            return

        users = load_users()
        pwd_hash = hash_password(password)

        if login in users:
            if users[login] != pwd_hash:
                win = tk.Toplevel(root)
                win.geometry("400x120+730+420")
                win.title("Ошибка")
                tk.Label(win, text="Неверный пароль", font=("Arial", 14, "bold")).place(
                    x=120, y=20
                )
                tk.Button(win, text="ОК", command=win.destroy).place(x=160, y=70)
                return
            else:
                win = tk.Toplevel(root)
                win.geometry("400x120+730+420")
                win.title("Вход")
                tk.Label(
                    win, text=f"Вход выполнен", font=("Arial", 14, "bold")
                ).place(x=50, y=20)
                tk.Button(
                    win, text="Начать игру", command=lambda: [win.destroy(), start_game()]
                ).place(x=140, y=70)
                return
        else:
            save_user(login, pwd_hash)
            win = tk.Toplevel(root)
            win.geometry("400x120+730+420")
            win.title("Регистрация")
            tk.Label(
                win,
                text=f"Вы успешно зарегистрировались",
                font=("Arial", 14, "bold"),
            ).place(x=20, y=20)
            tk.Button(
                win, text="Начать игру", command=lambda: [win.destroy(), start_game()]
            ).place(x=140, y=70)

    start_btn = tk.Button(root, text="Войти / Зарегистрироваться", command=register)
    start_btn.place(x=center_x - 110, y=210)

    root.mainloop()

if __name__ == "__main__":
    main()