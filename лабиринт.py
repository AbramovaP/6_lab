import tkinter as tk
from tkinter import messagebox
import random

cell_size = 20
maze_width = 21
maze_height = 21
animation_delay = 30

maze = []
bot_x = 0
bot_y = 0
exits = []
searching = False
visited = set()

root = None
canvas = None

def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]
    
    def carve(x, y):
        maze[y][x] = 0
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx*2, y + dy*2
            if 0 < nx < width-1 and 0 < ny < height-1 and maze[ny][nx] == 1:
                maze[y+dy][x+dx] = 0
                carve(nx, ny)
    
    carve(1, 1)
    return maze

def setup_gui():
    global root, canvas
    
    root = tk.Tk()
    root.title("Лабиринт")
    
    canvas = tk.Canvas(
        root, 
        width=maze_width * cell_size,
        height=maze_height * cell_size,
        bg='white'
    )
    canvas.pack(pady=10)
    canvas.bind("<Button-1>", on_canvas_click)
    
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)
    
    tk.Button(button_frame, text="Новый лабиринт", command=generate_new_maze).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Начать поиск", command=start_search).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Очистить выходы", command=clear_exits).pack(side=tk.LEFT, padx=5)

def draw_maze():
    global maze, bot_x, bot_y, exits
    
    canvas.delete("all")
    
    for y in range(maze_height):
        for x in range(maze_width):
            color = 'black' if maze[y][x] == 1 else 'white'
            canvas.create_rectangle(
                x * cell_size, y * cell_size,
                (x + 1) * cell_size, (y + 1) * cell_size,
                fill=color, outline='gray'
            )
    
    for ex, ey in exits:
        canvas.create_rectangle(
            ex * cell_size, ey * cell_size,
            (ex + 1) * cell_size, (ey + 1) * cell_size,
            fill='green', outline=''
        )
    
    draw_bot()

def draw_bot():
    global bot_x, bot_y
    
    x1 = bot_x * cell_size + 2
    y1 = bot_y * cell_size + 2
    x2 = (bot_x + 1) * cell_size - 2
    y2 = (bot_y + 1) * cell_size - 2
    
    canvas.create_oval(x1, y1, x2, y2, fill='blue', outline='blue')

def on_canvas_click(event):
    global exits, searching
    
    if searching:
        return
        
    x = event.x // cell_size
    y = event.y // cell_size
    
    if (0 <= x < maze_width and 0 <= y < maze_height and 
        maze[y][x] == 0):
        if (x, y) in exits:
            exits.remove((x, y))
        else:
            exits.append((x, y))
        draw_maze()

def clear_exits():
    global exits
    exits = []
    draw_maze()

def generate_new_maze():
    global maze, bot_x, bot_y, exits, searching, visited
    
    maze = generate_maze(maze_width, maze_height)
    bot_x = maze_width // 2
    bot_y = maze_height // 2
    exits = []
    searching = False
    visited = set()
    draw_maze()

def start_search():
    global searching, visited
    
    if not exits:
        messagebox.showwarning("Предупреждение", "Сначала установите выходы кликом мыши!")
        return
    
    if searching:
        return
        
    searching = True
    visited = set()
    root.after(100, dfs_search)

def dfs_search():
    global searching, visited, bot_x, bot_y
    
    if not searching:
        return
        
    stack = [(bot_x, bot_y, [])]
    visited = set()
    
    while stack and searching:
        x, y, path = stack.pop()
        
        if (x, y) in visited:
            continue
            
        visited.add((x, y))
        bot_x, bot_y = x, y
        
        visualize_step(x, y, "visiting", path)

        if (x, y) in exits:
            visualize_step(x, y, "found", path)
            messagebox.showinfo("Успех", f"Выход найден в позиции ({x}, {y})")
            searching = False
            return
        
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (0 <= nx < maze_width and 0 <= ny < maze_height and 
                maze[ny][nx] == 0 and (nx, ny) not in visited):
                stack.append((nx, ny, path + [(x, y)]))
        
        root.update()
        root.after(animation_delay)
    
    searching = False

def visualize_step(x, y, state, path):
    global maze, exits
    
    canvas.delete("all")

    for yy in range(maze_height):
        for xx in range(maze_width):
            color = 'black' if maze[yy][xx] == 1 else 'white'
            if (xx, yy) in path:
                color = 'orange'
            elif (xx, yy) in visited and (xx, yy) != (x, y):
                color = 'light yellow'
            canvas.create_rectangle(
                xx * cell_size, yy * cell_size,
                (xx + 1) * cell_size, (yy + 1) * cell_size,
                fill=color, outline='gray'
            )
    for ex, ey in exits:
        canvas.create_rectangle(
            ex * cell_size, ey * cell_size,
            (ex + 1) * cell_size, (ey + 1) * cell_size,
            fill='green', outline=''
        )

    if state == "found":
        canvas.create_rectangle(
            x * cell_size, y * cell_size,
            (x + 1) * cell_size, (y + 1) * cell_size,
            fill='green', outline=''
        )

    draw_bot()

def main():
    setup_gui()
    generate_new_maze()
    root.mainloop()

if __name__ == "__main__":
    main()