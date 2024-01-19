import tkinter as tk
import pandas as pd
from utils.utils import *
from characters.King import King
from characters.Queen import Queen
from characters.Bishop import Bishop
from characters.Knight import Knight
from characters.Rook import Rook
from characters.Pawn import Pawn

class Chess:
    def __init__(self, window):
        self.asset_dir = "./assets"
        self.init_window(window)
        self.init_board()
        self.init_characters()

    def cell_click(self, cell: tuple) -> None:
        print(cell)

    def init_window(self, window):
        self.window = window
        self.window.title("Chess")
        self.window.geometry("900x900")
        self.window.resizable(False, False)
        self.window.configure(bg="#FFFFFF")

    def init_board(self):
        self.active_cell = None
        self.board = pd.DataFrame(index=range(8), columns=range(8))
        self.display_board = []

        self.board_frame = tk.Frame(self.window, width=800, height=800, padx=50, pady=50)
        self.board_frame.pack()

        light_bg = "#ADD8E6"
        dark_bg = "#1F51FF"
        
        def swap_color(color: str) -> str:
            if color == light_bg:
                color = dark_bg
            elif color == dark_bg:
                color = light_bg
            return color

        color = light_bg
        for i in range(0, 8):
            self.display_board.append(self.row_board(color, i, swap_color))
            color = swap_color(color)        

    def init_characters(self):
        white_rook_A = Rook(Position(0, 0), Color.WHITE, "white_rook.png")
        white_rook_B = Rook(Position(7, 0), Color.WHITE, "white_rook.png")

        black_rook_A = Rook(Position(0, 7), Color.BLACK, "black_rook.png")
        black_rook_B = Rook(Position(7, 7), Color.BLACK, "black_rook.png")

        white_knight_A = Knight(Position(1, 0), Color.WHITE, "white_knight.png")
        white_knight_B = Knight(Position(6, 0), Color.WHITE, "white_knight.png")

        black_knight_A = Knight(Position(1, 7), Color.BLACK, "black_knight.png")
        black_knight_B = Knight(Position(6, 7), Color.BLACK, "black_knight.png")

        white_bishop_A = Bishop(Position(2, 0), Color.WHITE, "white_bishop.png")
        white_bishop_B = Bishop(Position(5, 0), Color.WHITE, "white_bishop.png")

        black_bishop_A = Bishop(Position(2, 7), Color.BLACK, "black_bishop.png")
        black_bishop_B = Bishop(Position(5, 7), Color.BLACK, "black_bishop.png")

        white_queen = Queen(Position(3, 0), Color.WHITE, "white_queen.png")
        white_king  = King(Position(4, 0), Color.WHITE, "white_king.png")

        black_queen = Queen(Position(3, 7), Color.BLACK, "black_queen.png")
        black_king  = King(Position(4, 7), Color.BLACK, "black_king.png")

        white_pawn_A = Pawn(Position(0, 1), Color.WHITE, "white_pawn.png")
        white_pawn_B = Pawn(Position(1, 1), Color.WHITE, "white_pawn.png")
        white_pawn_C = Pawn(Position(2, 1), Color.WHITE, "white_pawn.png")
        white_pawn_D = Pawn(Position(3, 1), Color.WHITE, "white_pawn.png")
        white_pawn_E = Pawn(Position(4, 1), Color.WHITE, "white_pawn.png")
        white_pawn_F = Pawn(Position(5, 1), Color.WHITE, "white_pawn.png")
        white_pawn_G = Pawn(Position(6, 1), Color.WHITE, "white_pawn.png")
        white_pawn_H = Pawn(Position(7, 1), Color.WHITE, "white_pawn.png")

        black_pawn_A = Pawn(Position(0, 6), Color.BLACK, "black_pawn.png")
        black_pawn_B = Pawn(Position(1, 6), Color.BLACK, "black_pawn.png")
        black_pawn_C = Pawn(Position(2, 6), Color.BLACK, "black_pawn.png")
        black_pawn_D = Pawn(Position(3, 6), Color.BLACK, "black_pawn.png")
        black_pawn_E = Pawn(Position(4, 6), Color.BLACK, "black_pawn.png")
        black_pawn_F = Pawn(Position(5, 6), Color.BLACK, "black_pawn.png")
        black_pawn_G = Pawn(Position(6, 6), Color.BLACK, "black_pawn.png")
        black_pawn_H = Pawn(Position(7, 6), Color.BLACK, "black_pawn.png")
        
        # Pack Board
        self.board.at[*white_rook_A.position.abs_position()] = white_rook_A
        self.board.at[*white_rook_B.position.abs_position()] = white_rook_B

        self.board.at[*black_rook_A.position.abs_position()] = black_rook_A
        self.board.at[*black_rook_B.position.abs_position()] = black_rook_B

        self.board.at[*white_knight_A.position.abs_position()] = white_knight_A
        self.board.at[*white_knight_B.position.abs_position()] = white_knight_B

        self.board.at[*black_knight_A.position.abs_position()] = black_knight_A
        self.board.at[*black_knight_B.position.abs_position()] = black_knight_B

        self.board.at[*white_bishop_A.position.abs_position()] = white_bishop_A
        self.board.at[*white_bishop_B.position.abs_position()] = white_bishop_B

        self.board.at[*black_bishop_A.position.abs_position()] = black_bishop_A
        self.board.at[*black_bishop_B.position.abs_position()] = black_bishop_B

        self.board.at[*white_queen.position.abs_position()] = white_queen
        self.board.at[*white_king.position.abs_position()] = white_king

        self.board.at[*black_queen.position.abs_position()] = black_queen
        self.board.at[*black_king.position.abs_position()] = black_king

        self.board.at[*white_pawn_A.position.abs_position()] = white_pawn_A
        self.board.at[*white_pawn_B.position.abs_position()] = white_pawn_B
        self.board.at[*white_pawn_C.position.abs_position()] = white_pawn_C
        self.board.at[*white_pawn_D.position.abs_position()] = white_pawn_D
        self.board.at[*white_pawn_E.position.abs_position()] = white_pawn_E
        self.board.at[*white_pawn_F.position.abs_position()] = white_pawn_F
        self.board.at[*white_pawn_G.position.abs_position()] = white_pawn_G
        self.board.at[*white_pawn_H.position.abs_position()] = white_pawn_H

        self.board.at[*black_pawn_A.position.abs_position()] = black_pawn_A
        self.board.at[*black_pawn_B.position.abs_position()] = black_pawn_B
        self.board.at[*black_pawn_C.position.abs_position()] = black_pawn_C
        self.board.at[*black_pawn_D.position.abs_position()] = black_pawn_D
        self.board.at[*black_pawn_E.position.abs_position()] = black_pawn_E
        self.board.at[*black_pawn_F.position.abs_position()] = black_pawn_F
        self.board.at[*black_pawn_G.position.abs_position()] = black_pawn_G
        self.board.at[*black_pawn_H.position.abs_position()] = black_pawn_H

    def row_board(self, color: str, row_index, swap_color):
        width = 12
        height = 5

        row = []
        lbl = tk.Button(self.board_frame, bg=color, width=width, height=height)
        lbl.bind('<Button-1>', lambda e: self.cell_click((row_index, 0)))
        lbl.grid(row=row_index, column=0)
        row.append(lbl)
        color = swap_color(color)

        lbl_1 = tk.Button(self.board_frame, bg=color, width=width, height=height)
        lbl_1.bind('<Button-1>', lambda e: self.cell_click((row_index, 1)))
        lbl_1.grid(row=row_index, column=1)
        row.append(lbl_1)
        color = swap_color(color)

        lbl_2 = tk.Button(self.board_frame, bg=color, width=width, height=height)
        lbl_2.bind('<Button-1>', lambda e: self.cell_click((row_index, 2)))
        lbl_2.grid(row=row_index, column=2)
        row.append(lbl_2)
        color = swap_color(color)

        lbl_3 = tk.Button(self.board_frame, bg=color, width=width, height=height)
        lbl_3.bind('<Button-1>', lambda e: self.cell_click((row_index, 3)))
        lbl_3.grid(row=row_index, column=3)
        row.append(lbl_3)
        color = swap_color(color)

        lbl_4 = tk.Button(self.board_frame, bg=color, width=width, height=height)
        lbl_4.bind('<Button-1>', lambda e: self.cell_click((row_index, 4)))
        lbl_4.grid(row=row_index, column=4)
        row.append(lbl_4)
        color = swap_color(color)

        lbl_5 = tk.Button(self.board_frame, bg=color, width=width, height=height)
        lbl_5.bind('<Button-1>', lambda e: self.cell_click((row_index, 5)))
        lbl_5.grid(row=row_index, column=5)
        row.append(lbl_5)
        color = swap_color(color)

        lbl_6 = tk.Button(self.board_frame, bg=color, width=width, height=height)
        lbl_6.bind('<Button-1>', lambda e: self.cell_click((row_index, 6)))
        lbl_6.grid(row=row_index, column=6)
        row.append(lbl_6)
        color = swap_color(color)

        lbl_7 = tk.Button(self.board_frame, bg=color, width=width, height=height)
        lbl_7.bind('<Button-1>', lambda e: self.cell_click((row_index, 7)))
        lbl_7.grid(row=row_index, column=7)
        row.append(lbl_7)
        color = swap_color(color)

        return row