import tkinter as tk
from tkinter import messagebox
import random
import time

class Minesweeper:
    def __init__(self, master):
        self.master = master
        self.master.title("扫雷游戏")
        self.master.resizable(False, False)
        
        # 难度设置
        self.difficulties = {
            '简单': {'rows': 9, 'cols': 9, 'mines': 10},
            '中等': {'rows': 16, 'cols': 16, 'mines': 40},
            '困难': {'rows': 16, 'cols': 30, 'mines': 99}
        }
        
        self.current_difficulty = '简单'
        self.init_game()
        
    def init_game(self):
        # 游戏状态
        self.game_over = False
        self.game_won = False
        self.first_click = True
        self.start_time = None
        self.timer_running = False
        
        # 获取当前难度设置
        config = self.difficulties[self.current_difficulty]
        self.rows = config['rows']
        self.cols = config['cols']
        self.total_mines = config['mines']
        
        # 游戏数据
        self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.revealed = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        self.flagged = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        
        # 创建界面
        self.create_widgets()
        
    def create_widgets(self):
        # 清除现有组件
        for widget in self.master.winfo_children():
            widget.destroy()
            
        # 顶部信息栏
        info_frame = tk.Frame(self.master, bg='#2c3e50')
        info_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 地雷计数
        self.mine_label = tk.Label(info_frame, text=f"地雷: {self.total_mines}", 
                                  bg='#2c3e50', fg='white', font=('Arial', 12, 'bold'))
        self.mine_label.pack(side=tk.LEFT, padx=20)
        
        # 计时器
        self.timer_label = tk.Label(info_frame, text="时间: 000", 
                                   bg='#2c3e50', fg='white', font=('Arial', 12, 'bold'))
        self.timer_label.pack(side=tk.RIGHT, padx=20)
        
        # 剩余标记数
        self.flag_label = tk.Label(info_frame, text=f"标记: {self.total_mines}", 
                                  bg='#2c3e50', fg='white', font=('Arial', 12, 'bold'))
        self.flag_label.pack(side=tk.RIGHT, padx=20)
        
        # 控制按钮栏
        control_frame = tk.Frame(self.master, bg='#ecf0f1')
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 难度选择
        difficulty_frame = tk.Frame(control_frame, bg='#ecf0f1')
        difficulty_frame.pack(side=tk.LEFT, padx=10)
        
        tk.Label(difficulty_frame, text="难度:", bg='#ecf0f1', font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.difficulty_var = tk.StringVar(value=self.current_difficulty)
        for difficulty in self.difficulties.keys():
            tk.Radiobutton(difficulty_frame, text=difficulty, variable=self.difficulty_var,
                          value=difficulty, bg='#ecf0f1', 
                          command=self.change_difficulty).pack(side=tk.LEFT, padx=5)
        
        # 重新开始按钮
        tk.Button(control_frame, text="重新开始", command=self.new_game,
                 bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                 padx=15, pady=5).pack(side=tk.RIGHT, padx=10)
        
        # 游戏板
        self.board_frame = tk.Frame(self.master, bg='#34495e')
        self.board_frame.pack(padx=10, pady=10)
        
        self.buttons = []
        for i in range(self.rows):
            button_row = []
            for j in range(self.cols):
                btn = tk.Button(self.board_frame, width=2, height=1, 
                              bg='#95a5a6', font=('Arial', 10, 'bold'),
                              relief=tk.RAISED, bd=2)
                btn.grid(row=i, column=j, padx=1, pady=1)
                btn.bind('<Button-1>', lambda e, r=i, c=j: self.left_click(r, c))
                btn.bind('<Button-3>', lambda e, r=i, c=j: self.right_click(r, c))
                button_row.append(btn)
            self.buttons.append(button_row)
            
        # 游戏说明
        help_frame = tk.Frame(self.master, bg='#ecf0f1')
        help_frame.pack(fill=tk.X, padx=5, pady=5)
        
        help_text = "操作说明: 左键点击揭开格子 | 右键标记地雷 | 数字表示周围地雷数"
        tk.Label(help_frame, text=help_text, bg='#ecf0f1', fg='#7f8c8d',
                font=('Arial', 9)).pack()
        
        # 启动计时器更新
        self.update_timer()
        
    def change_difficulty(self):
        self.current_difficulty = self.difficulty_var.get()
        self.new_game()
        
    def new_game(self):
        self.init_game()
        
    def place_mines(self, exclude_row, exclude_col):
        mines_placed = 0
        while mines_placed < self.total_mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            
            # 避免在第一次点击的位置及其周围放置地雷
            if (row == exclude_row and col == exclude_col) or \
               (abs(row - exclude_row) <= 1 and abs(col - exclude_col) <= 1):
                continue
                
            if self.board[row][col] != -1:
                self.board[row][col] = -1
                mines_placed += 1
                
                # 更新周围格子的数字
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        new_row, new_col = row + dr, col + dc
                        if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                            if self.board[new_row][new_col] != -1:
                                self.board[new_row][new_col] += 1
                                
    def left_click(self, row, col):
        if self.game_over or self.revealed[row][col] or self.flagged[row][col]:
            return
            
        if self.first_click:
            self.first_click = False
            self.place_mines(row, col)
            self.start_time = time.time()
            self.timer_running = True
            
        self.reveal_cell(row, col)
        self.check_win()
        
    def right_click(self, row, col):
        if self.game_over or self.revealed[row][col]:
            return
            
        self.flagged[row][col] = not self.flagged[row][col]
        self.update_button(row, col)
        self.update_flag_count()
        
    def reveal_cell(self, row, col):
        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return
        if self.revealed[row][col] or self.flagged[row][col]:
            return
            
        self.revealed[row][col] = True
        self.update_button(row, col)
        
        if self.board[row][col] == -1:
            self.game_over = True
            self.timer_running = False
            self.reveal_all_mines()
            messagebox.showinfo("游戏结束", "你踩到了地雷！")
            return
            
        # 如果是空白格子，自动展开周围
        if self.board[row][col] == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    self.reveal_cell(row + dr, col + dc)
                    
    def reveal_all_mines(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == -1:
                    self.revealed[i][j] = True
                    self.update_button(i, j)
                    
    def update_button(self, row, col):
        btn = self.buttons[row][col]
        
        if self.flagged[row][col]:
            btn.config(text='🚩', bg='#f39c12', fg='white')
        elif self.revealed[row][col]:
            if self.board[row][col] == -1:
                btn.config(text='💣', bg='#e74c3c', fg='white')
            elif self.board[row][col] == 0:
                btn.config(text='', bg='#ecf0f1', relief=tk.SUNKEN)
            else:
                colors = {1: '#3498db', 2: '#27ae60', 3: '#e74c3c', 4: '#9b59b6',
                         5: '#f39c12', 6: '#1abc9c', 7: '#34495e', 8: '#c0392b'}
                color = colors.get(self.board[row][col], '#2c3e50')
                btn.config(text=str(self.board[row][col]), bg='#ecf0f1', 
                          fg=color, relief=tk.SUNKEN)
        else:
            btn.config(text='', bg='#95a5a6', relief=tk.RAISED)
            
    def update_flag_count(self):
        flag_count = sum(sum(row) for row in self.flagged)
        remaining = self.total_mines - flag_count
        self.flag_label.config(text=f"标记: {remaining}")
        
    def check_win(self):
        # 检查是否所有非地雷格子都被揭开
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != -1 and not self.revealed[i][j]:
                    return
                    
        self.game_won = True
        self.game_over = True
        self.timer_running = False
        elapsed_time = int(time.time() - self.start_time) if self.start_time else 0
        messagebox.showinfo("恭喜获胜！", f"你赢了！用时 {elapsed_time} 秒")
        
    def update_timer(self):
        if self.timer_running and self.start_time:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"时间: {elapsed:03d}")
        
        # 每1000毫秒更新一次
        self.master.after(1000, self.update_timer)

def main():
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()

if __name__ == "__main__":
    main()
