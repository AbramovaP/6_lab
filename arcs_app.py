import tkinter as tk
from tkinter import filedialog, messagebox, colorchooser


class Arc:
    def __init__(self, canvas, x, y, radius, start_angle, end_angle, color="black"):
        self.canvas = canvas
        self.center = [float(x), float(y)]
        self.radius = float(radius)
        self.start_angle = float(start_angle)
        self.end_angle = float(end_angle)
        self.extent = (self.end_angle - self.start_angle) % 360 or 360
        self.color = color
        self.item = None

    def draw(self):
        if self.item:
            self.canvas.delete(self.item)
        x0 = self.center[0] - self.radius
        y0 = self.center[1] - self.radius
        x1 = self.center[0] + self.radius
        y1 = self.center[1] + self.radius
        self.item = self.canvas.create_arc(
            x0,
            y0,
            x1,
            y1,
            start=self.start_angle,
            extent=self.extent,
            outline=self.color,
            style=tk.ARC,
            width=2,
        )

    def recolor(self, new_color):
        self.color = new_color
        self.draw()

    def move(self, dx, dy):
        self.center[0] += float(dx)
        self.center[1] += float(dy)
        self.draw()

    def rotate(self, angle):
        self.start_angle = (self.start_angle + float(angle)) % 360
        self.draw()


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("ЛР №8")
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.arcs = []
        self.selected_arc = None

        panel = tk.Frame(root)
        panel.pack(fill=tk.X, padx=6, pady=6)

        tk.Button(panel, text="Загрузить из файла", command=self.load_from_file).pack(
            side=tk.LEFT, padx=3
        )
        tk.Button(panel, text="Изменить цвет", command=self.change_color).pack(
            side=tk.LEFT, padx=3
        )

        tk.Label(panel, text="dx:").pack(side=tk.LEFT)
        self.entry_dx = tk.Entry(panel, width=5)
        self.entry_dx.insert(0, "20")
        self.entry_dx.pack(side=tk.LEFT)

        tk.Label(panel, text="dy:").pack(side=tk.LEFT)
        self.entry_dy = tk.Entry(panel, width=5)
        self.entry_dy.insert(0, "20")
        self.entry_dy.pack(side=tk.LEFT)

        tk.Button(panel, text="Сдвинуть", command=self.move_selected).pack(
            side=tk.LEFT, padx=3
        )
        tk.Button(
            panel, text="Повернуть (+30°)", command=lambda: self.rotate_selected(30)
        ).pack(side=tk.LEFT, padx=3)

        tk.Label(panel, text="Выбрать дугу:").pack(side=tk.LEFT, padx=(10, 0))
        self.arc_var = tk.StringVar(panel)
        self.arc_menu = tk.OptionMenu(panel, self.arc_var, ())
        self.arc_menu.pack(side=tk.LEFT)
        self.arc_var.trace("w", self.update_selected_arc)

        self.status = tk.Label(root, anchor="w")
        self.status.pack(fill=tk.X, padx=6, pady=(0, 6))

    def parse_line(self, line):
        line = line.strip()
        if not line or line.startswith("#"):
            return None
        parts = line.split(",") if "," in line else line.split()
        if len(parts) < 5:
            raise ValueError("Ожидалось минимум 5 значений: x y r start end [color]")
        x, y, r, a1, a2 = parts[:5]
        color = parts[5] if len(parts) >= 6 else "black"

        x = float(x)
        y = float(y)
        r = float(r)
        a1 = float(a1)
        a2 = float(a2)
        if r <= 0:
            raise ValueError("Радиус должен быть > 0")
        for ang in (a1, a2):
            if ang < 0 or ang > 360:
                raise ValueError("Угол должен быть в диапазоне 0..360")
        return x, y, r, a1, a2, color

    def load_from_file(self):
        path = filedialog.askopenfilename(
            title="Выберите файл с дугами",
            filetypes=[("Текст/CSV", "*.csv *.txt"), ("Все файлы", "*.*")],
        )
        if not path:
            return
        try:
            with open(path, "r", encoding="utf-8-sig") as f:
                self.arcs.clear()
                self.canvas.delete("all")
                line_no = 0
                names = []
                for raw in f:
                    line_no += 1
                    try:
                        parsed = self.parse_line(raw)
                        if not parsed:
                            continue
                        x, y, r, a1, a2, color = parsed
                        arc = Arc(self.canvas, x, y, r, a1, a2, color)
                        arc.draw()
                        self.arcs.append(arc)
                        names.append(f"Дуга {len(self.arcs)}")
                    except Exception as row_err:
                        messagebox.showerror(
                            "Ошибка данных", f"Строка {line_no}: {row_err}"
                        )
                if self.arcs:
                    self.selected_arc = self.arcs[0]
                    self.arc_var.set(names[0])
                    menu = self.arc_menu["menu"]
                    menu.delete(0, "end")
                    for name in names:
                        menu.add_command(
                            label=name, command=tk._setit(self.arc_var, name)
                        )
                    self.status.config(text=f"Загружено дуг: {len(self.arcs)}")
                else:
                    self.status.config(text="Не удалось загрузить ни одной дуги")
        except Exception as e:
            messagebox.showerror("Ошибка файла", str(e))

    def update_selected_arc(self, *args):
        name = self.arc_var.get()
        if not name:
            return
        try:
            index = int(name.split()[1]) - 1
            if 0 <= index < len(self.arcs):
                self.selected_arc = self.arcs[index]
        except:
            pass

    def change_color(self):
        if self.selected_arc:
            color = colorchooser.askcolor(title="Выберите цвет")[1]
            if color:
                self.selected_arc.recolor(color)

    def move_selected(self):
        if self.selected_arc:
            try:
                dx = float(self.entry_dx.get())
                dy = float(self.entry_dy.get())
                new_x = self.selected_arc.center[0] + dx
                new_y = self.selected_arc.center[1] + dy
                if (
                    0 < new_x < self.canvas.winfo_width()
                    and 0 < new_y < self.canvas.winfo_height()
                ):
                    self.selected_arc.move(dx, dy)
                else:
                    messagebox.showwarning(
                        "Внимание", "Перемещение выведет дугу за пределы холста!"
                    )
            except ValueError:
                messagebox.showerror("Ошибка", "Введите числовые значения dx и dy")

    def rotate_selected(self, angle):
        if self.selected_arc:
            self.selected_arc.rotate(angle)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
