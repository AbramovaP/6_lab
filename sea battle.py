import tkinter as tk
import tkinter.messagebox as messagebox
import random

GRID_SIZE = 10
CELL_PX = 36
COLORS = {
    "bg": "#f7f7f7", "grid_line": "#2f4f4f", "ship": "#2e8b57",
    "water": "#e6f4f7", "hit": "#c0392b", "miss": "#3498db",
    "hover_ok": "#9bff9b", "hover_bad": "#ff9bb3"
}
SHIP_LENGTHS = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
CELL_EMPTY, CELL_SHIP, CELL_HIT, CELL_MISS = 0, 1, 2, 3

def make_board():
    return {
        "grid": [[CELL_EMPTY]*GRID_SIZE for _ in range(GRID_SIZE)],
        "ships": [],
        "attacks": set()
    }

def neighbours(r, c):
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0: continue
            nr, nc = r+dr, c+dc
            if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                yield nr, nc

def can_place(board, r, c, length, horizontal):
    coords = [ (r, c+i) if horizontal else (r+i, c) for i in range(length) ]
    for rr, cc in coords:
        if not (0 <= rr < GRID_SIZE and 0 <= cc < GRID_SIZE): return False
        if board["grid"][rr][cc] != CELL_EMPTY: return False
        for nr, nc in neighbours(rr, cc):
            if board["grid"][nr][nc] == CELL_SHIP: return False
    return True

def place_ship(board, r, c, length, horizontal):
    if not can_place(board, r, c, length, horizontal): return False
    coords = set((r, c+i) if horizontal else (r+i, c) for i in range(length))
    board["ships"].append({"cells": coords, "hits": set()})
    for rr, cc in coords: board["grid"][rr][cc] = CELL_SHIP
    return True

def auto_place(board, lengths):
    board["grid"] = [[CELL_EMPTY]*GRID_SIZE for _ in range(GRID_SIZE)]
    board["ships"] = []
    board["attacks"] = set()
    for length in lengths:
        for _ in range(1000):
            r, c = random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1)
            horiz = random.choice([True, False])
            if place_ship(board, r, c, length, horiz): break
        else:
            return auto_place(board, lengths)

def receive_shot(board, r, c):
    if (r, c) in board["attacks"]: return None
    board["attacks"].add((r, c))
    if board["grid"][r][c] == CELL_SHIP:
        board["grid"][r][c] = CELL_HIT
        for ship in board["ships"]:
            if (r, c) in ship["cells"]:
                ship["hits"].add((r, c))
                if len(ship["hits"]) == len(ship["cells"]):
                    mark_around_sunk(board, ship)
                    return "sunk"
                return "hit"
    board["grid"][r][c] = CELL_MISS
    return "miss"

def mark_around_sunk(board, ship):
    for r, c in ship["cells"]:
        for nr in range(max(0, r-1), min(GRID_SIZE, r+2)):
            for nc in range(max(0, c-1), min(GRID_SIZE, c+2)):
                if board["grid"][nr][nc] == CELL_EMPTY:
                    board["grid"][nr][nc] = CELL_MISS

def all_sunk(board):
    return all(len(ship["hits"]) == len(ship["cells"]) for ship in board["ships"])

def bot_reset(state):
    state["available"] = [(r,c) for r in range(GRID_SIZE) for c in range(GRID_SIZE)]
    random.shuffle(state["available"])
    state["hit_stack"] = []

def bot_next_shot(state):
    if state["hit_stack"]:
        return state["hit_stack"].pop(0)
    if not state["available"]:
        return None
    return state["available"].pop()

def bot_feedback(state, coord, result):
    if result == "hit":
        r, c = coord
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE and (nr,nc) not in state["hit_stack"]:
                state["hit_stack"].append((nr,nc))
    elif result == "sunk":
        state["hit_stack"] = []

def make_controller():
    return {
        "player_board": make_board(),
        "cpu_board": make_board(),
        "ai": {"available": [], "hit_stack": []},
        "stage": "setup",
        "player_turn": True,
        "placement_index": 0,
        "orientation": True
    }

class GUI:
    def __init__(self, root):
        self.root = root
        root.title("Морской бой")
        self.controller = make_controller()
        self.cell = CELL_PX
        self.canvas_size = GRID_SIZE * self.cell
        self.dragging = False
        self.preview_items = []
        self.setup_ui()
        self.redraw_all()

    def setup_ui(self):
        top = tk.Frame(self.root, bg=COLORS["bg"])
        top.pack(fill=tk.X, padx=8, pady=6)
        tk.Button(top, text="Новая партия", command=self.new_game, width=12).pack(side=tk.LEFT, padx=4)
        
        info = tk.Frame(self.root, bg=COLORS["bg"])
        info.pack(fill=tk.X, padx=8, pady=4)
        self.count_label = tk.Label(info, text="", bg=COLORS["bg"], font=("Arial", 11))
        self.count_label.pack()
        
        main = tk.Frame(self.root, bg=COLORS["bg"])
        main.pack(pady=6, padx=10)
        
        right = tk.Frame(main, bg=COLORS["bg"])
        right.pack(side=tk.RIGHT, padx=12)
        tk.Label(right, text="Воды противника", bg=COLORS["bg"], font=("Arial", 11, "bold")).pack(pady=2)
        self.enemy_canvas = tk.Canvas(right, width=self.canvas_size, height=self.canvas_size, bg=COLORS["water"], highlightthickness=1)
        self.enemy_canvas.pack(padx=6, pady=6)
        self.enemy_canvas.bind("<Button-1>", self.on_enemy_click)
        
        left = tk.Frame(main, bg=COLORS["bg"])
        left.pack(side=tk.LEFT, padx=12)
        tk.Label(left, text="Ваш флот", bg=COLORS["bg"], font=("Arial", 11, "bold")).pack(pady=2)
        self.player_canvas = tk.Canvas(left, width=self.canvas_size, height=self.canvas_size, bg=COLORS["water"], highlightthickness=1)
        self.player_canvas.pack(padx=6, pady=6)
        
        binds = [
            ("<Button-1>", self.on_player_press),
            ("<B1-Motion>", self.on_player_motion),
            ("<ButtonRelease-1>", self.on_player_release),
            ("<Button-3>", self.on_player_right_click),
            ("<Motion>", self.on_player_hover)
        ]
        for ev, fn in binds:
            self.player_canvas.bind(ev, fn)

    def on_player_press(self, event):
        if self.controller["stage"] != "setup": return
        r, c = event.y // self.cell, event.x // self.cell
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            self.dragging = True
            self.update_preview_anchor(r, c)

    def on_player_motion(self, event):
        if not self.dragging: return
        r, c = event.y // self.cell, event.x // self.cell
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            self.update_preview_anchor(r, c)
        else:
            self.clear_preview()

    def on_player_release(self, event):
        if not self.dragging: return
        self.dragging = False
        r, c = event.y // self.cell, event.x // self.cell
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            self.player_place(r, c)
        self.clear_preview()

    def on_player_right_click(self, event):
        if self.controller["stage"] == "setup":
            self.controller["orientation"] = not self.controller["orientation"]
            if self.dragging: 
                r, c = event.y // self.cell, event.x // self.cell
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                    self.update_preview_anchor(r, c)

    def on_player_hover(self, event):
        if self.controller["stage"] != "setup": return
        r, c = event.y // self.cell, event.x // self.cell
        if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
            self.update_preview_anchor(r, c)
        else:
            self.clear_preview()

    def clear_preview(self):
        for item in self.preview_items:
            self.player_canvas.delete(item)
        self.preview_items = []

    def update_preview_anchor(self, r, c):
        self.clear_preview()
        idx = self.controller["placement_index"]
        if idx >= len(SHIP_LENGTHS): return
        length = SHIP_LENGTHS[idx]
        horiz = self.controller["orientation"]
        coords = [(r, c+i) if horiz else (r+i, c) for i in range(length)]
        valid = can_place(self.controller["player_board"], r, c, length, horiz)
        color = COLORS["hover_ok"] if valid else COLORS["hover_bad"]
        for rr, cc in coords:
            if 0 <= rr < GRID_SIZE and 0 <= cc < GRID_SIZE:
                x1, y1 = cc*self.cell, rr*self.cell
                x2, y2 = x1 + self.cell, y1 + self.cell
                rect = self.player_canvas.create_rectangle(x1, y1, x2, y2,
                                                         fill=color, outline=COLORS["grid_line"], stipple="gray50")
                self.preview_items.append(rect)

    def player_place(self, r, c):
        idx = self.controller["placement_index"]
        length = SHIP_LENGTHS[idx]
        if place_ship(self.controller["player_board"], r, c, length, self.controller["orientation"]):
            self.controller["placement_index"] += 1
            if self.controller["placement_index"] >= len(SHIP_LENGTHS):
                self.start_play()
            self.redraw_all()
            return True
        return False

    def start_play(self):
        if not self.controller["cpu_board"]["ships"]:
            auto_place(self.controller["cpu_board"], SHIP_LENGTHS)
        self.controller["stage"] = "playing"
        self.controller["player_turn"] = True
        bot_reset(self.controller["ai"])

    def on_enemy_click(self, event):
        if self.controller["stage"] != "playing" or not self.controller["player_turn"]: return
        r, c = event.y // self.cell, event.x // self.cell
        if not (0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE): return
        result = receive_shot(self.controller["cpu_board"], r, c)
        if result is None: return
        if all_sunk(self.controller["cpu_board"]):
            self.controller["stage"] = "ended"
            self.redraw_all()
            messagebox.showinfo("Победа", "Вы уничтожили все корабли противника!")
            return
        if result == "miss":
            self.controller["player_turn"] = False
            self.redraw_all()
            self.root.after(450, self.computer_turn)
        else:
            self.redraw_all()

    def computer_turn(self):
        if self.controller["stage"] != "playing" or self.controller["player_turn"]: return
        while True:
            shot = bot_next_shot(self.controller["ai"])
            if not shot:
                self.controller["player_turn"] = True
                return
            r, c = shot
            if (r, c) not in self.controller["player_board"]["attacks"]:
                break
        result = receive_shot(self.controller["player_board"], r, c)
        bot_feedback(self.controller["ai"], (r, c), result)
        self.redraw_all()
        if all_sunk(self.controller["player_board"]):
            self.controller["stage"] = "ended"
            messagebox.showinfo("Поражение", "Противник уничтожил все ваши корабли.")
            return
        if result == "miss":
            self.controller["player_turn"] = True
        else:
            self.root.after(300, self.computer_turn)

    def redraw_all(self):
        self.draw_player_board()
        self.draw_enemy_board()
        player_alive = sum(1 for s in self.controller["player_board"]["ships"] if len(s["hits"]) < len(s["cells"]))
        enemy_alive = sum(1 for s in self.controller["cpu_board"]["ships"] if len(s["hits"]) < len(s["cells"]))
        self.count_label.config(text=f"Ваши корабли: {player_alive}/10   |   Корабли противника: {enemy_alive}/10")

    def draw_board(self, canvas, board, show_ships):
        canvas.delete("all")
        for r in range(GRID_SIZE):
            for c in range(GRID_SIZE):
                x1, y1 = c*self.cell, r*self.cell
                x2, y2 = x1 + self.cell, y1 + self.cell
                state = board["grid"][r][c]
                if state == CELL_EMPTY:
                    fill = COLORS["water"]
                elif state == CELL_SHIP:
                    fill = COLORS["ship"] if show_ships else COLORS["water"]
                elif state == CELL_HIT:
                    fill = COLORS["hit"]
                else:
                    fill = COLORS["miss"]
                canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline=COLORS["grid_line"])
        for ship in board["ships"]:
            if len(ship["hits"]) == len(ship["cells"]):
                for r, c in ship["cells"]:
                    x1, y1 = c*self.cell, r*self.cell
                    x2, y2 = x1 + self.cell, y1 + self.cell
                    pad = int(self.cell * 0.18)
                    canvas.create_line(x1+pad, y1+pad, x2-pad, y2-pad, fill="black", width=2)
                    canvas.create_line(x1+pad, y2-pad, x2-pad, y1+pad, fill="black", width=2)
        for i in range(GRID_SIZE+1):
            canvas.create_line(0, i*self.cell, self.canvas_size, i*self.cell, fill=COLORS["grid_line"])
            canvas.create_line(i*self.cell, 0, i*self.cell, self.canvas_size, fill=COLORS["grid_line"])

    def draw_player_board(self):
        self.draw_board(self.player_canvas, self.controller["player_board"], True)

    def draw_enemy_board(self):
        self.draw_board(self.enemy_canvas, self.controller["cpu_board"], False)

    def new_game(self):
        self.controller = make_controller()
        self.redraw_all()

def main():
    root = tk.Tk()
    app = GUI(root)
    width, height = app.canvas_size*2 + 300, app.canvas_size + 160
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    root.mainloop()

if __name__ == "__main__":
    main()
