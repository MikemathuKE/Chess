import arcade
import pandas as pd
from utils.utils import *
from characters.King import King
from characters.Queen import Queen
from characters.Bishop import Bishop
from characters.Knight import Knight
from characters.Rook import Rook
from characters.Pawn import Pawn

class Chess(arcade.Window):
    def __init__(self):
        super().__init__(900, 900, "Chess")
        arcade.set_background_color(arcade.color.AIR_FORCE_BLUE)

    def setup(self):
        self.asset_dir = "./assets"
        self.init_board()
        self.init_characters()

    def on_draw(self):
        self.clear()
        self.display_board.draw()
        self.characters.draw()

    def cell_click(self, cell: tuple) -> None:
        print(cell)

    def init_board(self):
        self.active_cell = None
        self.display_board = arcade.ShapeElementList()

        light_bg = arcade.color.BEAU_BLUE
        dark_bg = arcade.color.BALL_BLUE
        
        def swap_color(color: str) -> str:
            if color == light_bg:
                color = dark_bg
            elif color == dark_bg:
                color = light_bg
            return color

        color = light_bg
        for row in range(0, 8):
            for column in range(0, 8):
                center_x, center_y = Position(column, row).get_center_pixel()
                self.display_board.append(arcade.create_rectangle_filled(center_x=center_x, center_y=center_y, width=Position.MULTIPLIER, height=Position.MULTIPLIER, color=color))
                color = swap_color(color)
            color = swap_color(color)

    def init_characters(self):
        self.characters = arcade.SpriteList()
        self.white_rook_A = Rook(Position(0, 0), Color.WHITE, "white_rook.png")
        self.characters.append(self.white_rook_A)
        self.white_rook_B = Rook(Position(7, 0), Color.WHITE, "white_rook.png")
        self.characters.append(self.white_rook_B)

        self.black_rook_A = Rook(Position(0, 7), Color.BLACK, "black_rook.png")
        self.characters.append(self.black_rook_A)
        self.black_rook_B = Rook(Position(7, 7), Color.BLACK, "black_rook.png")
        self.characters.append(self.black_rook_B)

        self.white_knight_A = Knight(Position(1, 0), Color.WHITE, "white_knight.png")
        self.characters.append(self.white_knight_A)
        self.white_knight_B = Knight(Position(6, 0), Color.WHITE, "white_knight.png")
        self.characters.append(self.white_knight_B)

        self.black_knight_A = Knight(Position(1, 7), Color.BLACK, "black_knight.png")
        self.characters.append(self.black_knight_A)
        self.black_knight_B = Knight(Position(6, 7), Color.BLACK, "black_knight.png")
        self.characters.append(self.black_knight_B)

        self.white_bishop_A = Bishop(Position(2, 0), Color.WHITE, "white_bishop.png")
        self.characters.append(self.white_bishop_A)
        self.white_bishop_B = Bishop(Position(5, 0), Color.WHITE, "white_bishop.png")
        self.characters.append(self.white_bishop_B)

        self.black_bishop_A = Bishop(Position(2, 7), Color.BLACK, "black_bishop.png")
        self.characters.append(self.black_bishop_A)
        self.black_bishop_B = Bishop(Position(5, 7), Color.BLACK, "black_bishop.png")
        self.characters.append(self.black_bishop_B)

        self.white_queen = Queen(Position(3, 0), Color.WHITE, "white_queen.png")
        self.characters.append(self.white_queen)
        self.white_king  = King(Position(4, 0), Color.WHITE, "white_king.png")
        self.characters.append(self.white_king)

        self.black_queen = Queen(Position(3, 7), Color.BLACK, "black_queen.png")
        self.characters.append(self.black_queen)
        self.black_king  = King(Position(4, 7), Color.BLACK, "black_king.png")
        self.characters.append(self.black_king)

        self.white_pawn_A = Pawn(Position(0, 1), Color.WHITE, "white_pawn.png")
        self.characters.append(self.white_pawn_A)
        self.white_pawn_B = Pawn(Position(1, 1), Color.WHITE, "white_pawn.png")
        self.characters.append(self.white_pawn_B)
        self.white_pawn_C = Pawn(Position(2, 1), Color.WHITE, "white_pawn.png")
        self.characters.append(self.white_pawn_C)
        self.white_pawn_D = Pawn(Position(3, 1), Color.WHITE, "white_pawn.png")
        self.characters.append(self.white_pawn_D)
        self.white_pawn_E = Pawn(Position(4, 1), Color.WHITE, "white_pawn.png")
        self.characters.append(self.white_pawn_E)
        self.white_pawn_F = Pawn(Position(5, 1), Color.WHITE, "white_pawn.png")
        self.characters.append(self.white_pawn_F)
        self.white_pawn_G = Pawn(Position(6, 1), Color.WHITE, "white_pawn.png")
        self.characters.append(self.white_pawn_G)
        self.white_pawn_H = Pawn(Position(7, 1), Color.WHITE, "white_pawn.png")
        self.characters.append(self.white_pawn_H)

        self.black_pawn_A = Pawn(Position(0, 6), Color.BLACK, "black_pawn.png")
        self.characters.append(self.black_pawn_A)
        self.black_pawn_B = Pawn(Position(1, 6), Color.BLACK, "black_pawn.png")
        self.characters.append(self.black_pawn_B)
        self.black_pawn_C = Pawn(Position(2, 6), Color.BLACK, "black_pawn.png")
        self.characters.append(self.black_pawn_C)
        self.black_pawn_D = Pawn(Position(3, 6), Color.BLACK, "black_pawn.png")
        self.characters.append(self.black_pawn_D)
        self.black_pawn_E = Pawn(Position(4, 6), Color.BLACK, "black_pawn.png")
        self.characters.append(self.black_pawn_E)
        self.black_pawn_F = Pawn(Position(5, 6), Color.BLACK, "black_pawn.png")
        self.characters.append(self.black_pawn_F)
        self.black_pawn_G = Pawn(Position(6, 6), Color.BLACK, "black_pawn.png")
        self.characters.append(self.black_pawn_G)
        self.black_pawn_H = Pawn(Position(7, 6), Color.BLACK, "black_pawn.png")
        self.characters.append(self.black_pawn_H)