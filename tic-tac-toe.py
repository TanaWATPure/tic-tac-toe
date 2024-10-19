import tkinter as tk
from tkinter import messagebox
import time
import math

class TicTacToe:
    def __init__(self, root):
        """
        เกม XO (Tic-Tac-Toe)
        Created by Tanawat Chitratta
        """
        
        self.root = root
        self.root.title("เกม XO - Tic-Tac-Toe")
        
        
        self.colors = {
            'bg': '#2C3E50',      
            'button': '#34495E',   
            'X': '#E74C3C',     
            'O': '#3498DB',     
            'win': '#2ECC71',     
            'draw': '#F1C40F',    
            'credit': '#95A5A6'   
        }
        
        
        self.root.configure(bg=self.colors['bg'])
        self.root.minsize(400, 550)  
        
        
        self.current_player = "X"  
        self.board = [""] * 9     
        self.buttons = []         
        self.animation_in_progress = False  
        
        
        self.main_frame = tk.Frame(root, bg=self.colors['bg'])
        self.main_frame.pack(expand=True, padx=20, pady=20)
        
        
        self.title_label = tk.Label(
            self.main_frame,
            text="เกม Tic-Tac-Toe",
            font=('Helvetica', 24, 'bold'),
            bg=self.colors['bg'],
            fg='white'
        )
        self.title_label.pack(pady=(0, 20))
        
        
        self.board_frame = tk.Frame(
            self.main_frame,
            bg=self.colors['bg']
        )
        self.board_frame.pack()
        
        # จัดการตารางกริด
        for i in range(3):
            self.board_frame.grid_rowconfigure(i, weight=1)
            self.board_frame.grid_columnconfigure(i, weight=1)
        
        self.create_buttons()
        
        # สร้างป้ายแสดงตาของผู้เล่น
        self.turn_label = tk.Label(
            self.main_frame,
            text="ตาผู้เล่น X",
            font=('Helvetica', 16),
            bg=self.colors['bg'],
            fg='white'
        )
        self.turn_label.pack(pady=20)
        
        # สร้างปุ่มเริ่มเกมใหม่
        self.reset_button = tk.Button(
            self.main_frame,
            text="เริ่มเกมใหม่",
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['button'],
            fg='white',
            relief='flat',
            padx=20,
            pady=10,
            command=self.reset_game
        )
        self.reset_button.pack(pady=10)
        
        # เครดิตผู้พัฒนา
        credit_frame = tk.Frame(self.main_frame, bg=self.colors['bg'])
        credit_frame.pack(pady=(20, 0))
        
        credit_label = tk.Label(
            credit_frame,
            text="Created by",
            font=('Helvetica', 10),
            bg=self.colors['bg'],
            fg=self.colors['credit']
        )
        credit_label.pack()
        
        developer_label = tk.Label(
            credit_frame,
            text="Tanawat Chitratta",
            font=('Helvetica', 12, 'bold'),
            bg=self.colors['bg'],
            fg='white'
        )
        developer_label.pack()
        
        # เพิ่มเอฟเฟกต์เมื่อเมาส์ชี้ที่ปุ่ม
        self.reset_button.bind('<Enter>', self.on_enter)
        self.reset_button.bind('<Leave>', self.on_leave)

    # สร้างปุ่มกดทั้ง 9 ช่อง
    def create_buttons(self):
        
        for i in range(9):
            button = tk.Button(
                self.board_frame,
                text="",
                font=('Helvetica', 32, 'bold'),
                width=3,
                height=1,
                bg=self.colors['button'],
                fg='white',
                relief='flat',
                command=lambda i=i: self.make_move(i)
            )
            button.grid(
                row=i//3,
                column=i%3,
                padx=3,
                pady=3,
                sticky="nsew"
            )
            button.bind('<Enter>', lambda e, btn=button: self.button_hover(btn, True))
            button.bind('<Leave>', lambda e, btn=button: self.button_hover(btn, False))

            self.buttons.append(button)
    # ฟังก์ชันจัดการการเดินของผู้เล่น
    def make_move(self, index):
        
        if self.animation_in_progress:
            return
            
        if self.board[index] == "" and not self.check_winner():
            button = self.buttons[index]
            self.board[index] = self.current_player
            
            button.config(
                text=self.current_player,
                disabledforeground=self.colors[self.current_player],
                state='disabled',
                bg=self.colors['button']
            )
            
            self.root.after(0, self.animate_mark, button, self.current_player)
            
            if self.check_winner():
                self.turn_label.config(
                    text=f"ผู้เล่น {self.current_player} ชนะ!",
                    fg=self.colors[self.current_player]
                )
                self.root.after(1500, self.reset_game)
            elif "" not in self.board:
                self.turn_label.config(
                    text="เสมอ!",
                    fg=self.colors['draw']
                )
                self.root.after(1500, self.reset_game)
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                self.turn_label.config(
                    text=f"ตาผู้เล่น {self.current_player}",
                    fg='white'
                )
     # ตรวจสอบผู้ชนะ
    def check_winner(self):
       
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # แถวนอน
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # แถวตั้ง
            (0, 4, 8), (2, 4, 6)              # แนวทแยง
        ]
        
        for a, b, c in winning_combinations:
            if (self.board[a] == self.board[b] == self.board[c] and 
                self.board[a] != ""):
                for pos in (a, b, c):
                    self.buttons[pos].config(bg=self.colors['win'])
                return True
        return False

    # เริ่มเกมใหม่
    def reset_game(self):
        
        self.current_player = "X"
        self.board = [""] * 9
        
        for button in self.buttons:
            button.config(
                text="",
                bg=self.colors['button'],
                state='normal',
                fg='white'
            )
            
        self.turn_label.config(
            text="ตาผู้เล่น X",
            fg='white'
        )

    def on_enter(self, e):
        self.reset_button.config(bg='#436B8C')

    def on_leave(self, e):
        self.reset_button.config(bg=self.colors['button'])

    def button_hover(self, button, entering):
        if button['state'] != 'disabled':
            button.config(bg='#436B8C' if entering else self.colors['button'])

    # แอนิเมชั่นเมื่อกดเลือกช่อง
    async def animate_mark(self, button, player):
        
        self.animation_in_progress = True
        frames = 10
        for i in range(frames):
            scale = math.sin((i / frames) * math.pi/2)
            font_size = int(20 + scale * 12)
            button.config(font=('Helvetica', font_size, 'bold'))
            button.update()
            time.sleep(0.02)
        self.animation_in_progress = False

def main():
    """
    เริ่มต้นเกม XO
    Created by Tanawat Chitratta
    """
    root = tk.Tk()
    root.title("เกม XO - Created by Tanawat Chitratta")
    
    try:
        root.iconbitmap('game_icon.ico')
    except:
        pass
        
    game = TicTacToe(root)
    root.mainloop()

if __name__ == "__main__":
    main()