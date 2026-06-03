import tkinter as tk
from tkinter import messagebox

Player = "X"
Bot = "O"

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Крестики-нолики")
        self.root.resizable(False, False)

        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.board = [["" for _ in range(3)] for _ in range(3)]

        self.create_buttons()
        self.create_reset_button()

        self.player_turn = True

    def create_buttons(self):
        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    self.root,
                    text="",
                    font=("Arial", 40),
                    width=5,
                    height=2,
                    command=lambda x=i, y=j: self.player_move(x, y),
                )
                btn.grid(row=i, column=j, padx=1, pady=1)
                self.buttons[i][j] = btn

    def create_reset_button(self):
        reset_btn = tk.Button(
            self.root, text="Новая игра", font=("Arial", 14), command=self.reset
        )
        reset_btn.grid(row=3, column=0, columnspan=3, sticky="we", padx=2, pady=2)

    def player_move(self, x, y):
        if not self.player_turn:
            return
        if self.board[x][y] == "":
            self.make_move(x, y, Player)
            if self.check_winner(Player):
                messagebox.showinfo("Игра окончена", "Вы выиграли!")
                self.reset()
                return
            elif self.is_draw():
                messagebox.showinfo("Игра окончена", "Ничья!")
                self.reset()
                return
            else:
                self.player_turn = False
                self.root.after(250, self.bot_move)

    def bot_move(self):
        best_score = -float('inf')
        best_move = None
        
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == "":
                    self.board[i][j] = Bot
                    score = self.minimax(self.board, 0, False)
                    self.board[i][j] = ""
                    
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        
        if best_move:
            x, y = best_move
            self.make_move(x, y, Bot)
            if self.check_winner(Bot):
                messagebox.showinfo("Игра окончена", "Бот выиграл!")
                self.reset()
                return
            elif self.is_draw():
                messagebox.showinfo("Игра окончена", "Ничья!")
                self.reset()
                return
        
        self.player_turn = True

    def minimax(self, board, depth, is_maximizing):
        if self.check_winner_board(board, Bot):
            return 10 - depth
        if self.check_winner_board(board, Player):
            return depth - 10
        if self.is_draw_board(board):
            return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = Bot
                        score = self.minimax(board, depth + 1, False)
                        board[i][j] = ""
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if board[i][j] == "":
                        board[i][j] = Player
                        score = self.minimax(board, depth + 1, True)
                        board[i][j] = ""
                        best_score = min(score, best_score)
            return best_score

    def check_winner_board(self, board, player):
        for i in range(3):
            if all(board[i][j] == player for j in range(3)):
                return True
        for j in range(3):
            if all(board[i][j] == player for i in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)):
            return True
        if all(board[i][2 - i] == player for i in range(3)):
            return True
        return False

    def make_move(self, x, y, player):
        self.board[x][y] = player
        self.buttons[x][y].config(
            text=player, state="disabled", disabledforeground="navy"
        )

    def check_winner(self, player):
        return self.check_winner_board(self.board, player)

    def is_draw(self):
        return all(self.board[i][j] != "" for i in range(3) for j in range(3))

    def is_draw_board(self, board):
        return all(board[i][j] != "" for i in range(3) for j in range(3))

    def reset(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(text="", state="normal")
        self.player_turn = True


if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()