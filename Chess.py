import arcade
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
        self.player_turn = Color.WHITE

    def on_draw(self):
        self.clear()
        self.display_board.draw()
        self.characters.draw()

    def change_turn(self) -> None:
        if self.player_turn == Color.WHITE:
            self.player_turn = Color.BLACK
        else:
            self.player_turn = Color.WHITE

    def find_piece(self, _position: tuple):
        for character in self.characters:
            if character.get_grid_position() == _position:
                return character
        return None

    def on_mouse_press(self, x, y, button, modifiers):
        click_pos = Position.interpret_position(x, y)

        if self.active_cell is None:
            piece = self.find_piece(click_pos)
            if piece:
                if piece.get_piece_color() == self.player_turn:
                    self.active_cell = piece.get_grid_position()
                    print(f"Active Cell: {self.active_cell}")
        else:
            active_character = None

            #  Retrieve the active character
            active_character = self.find_piece(self.active_cell)

            # Calculate the direction and steps
            direction, steps = Movement.calculate_direction(self.active_cell, click_pos, active_character.is_inversed())
            print(direction, steps)

            # Check if the move is valid
            if active_character.move_valid(direction, steps):
                move_possible = True
                kill_piece = None
                print("Move Valid")

                # Check each step to see if there is a piece in the way
                next_position = self.active_cell
                for step in range(steps):
                    print(f"Calculation Step: ", step)
                    # Calculate the next position
                    print(f"Initial Position: {next_position}")
                    next_position = Movement.predict_position(next_position, direction, 1, active_character.is_inversed())
                    print(f"Next Position: {next_position}")
                    # Check if there is a piece in the way
                    kill_piece = self.find_piece(next_position)
                    if kill_piece:
                        # Check if the piece is the same color
                        if kill_piece.get_piece_color() == active_character.get_piece_color():
                            # If it is the same color, the move is not possible
                            move_possible = False
                            kill_piece = None
                            print("Same color piece in the way")
                            break
                        elif step != steps - 1:
                            # If steps do not match current pos, the move is not possible
                            move_possible = False
                            kill_piece = None
                            print("Another piece is blocking the way")
                            break
                        else:
                            # If it is not the same color and steps do not match current pos, the move is possible
                            move_possible = True
                            break
                    else:
                        # If there is no piece in the way, the move is possible\
                        move_possible = True
                        pass

                # If the move is valid, move the piece
                if move_possible:
                    print("Move Possible")
                    active_character.set_grid_position(Position(click_pos[0], click_pos[1]))
                    if kill_piece:
                        kill_piece.kill()
                        self.characters.remove(kill_piece)
                    self.active_cell = None
                    self.change_turn()
                else:
                    print("Move Not Possible")
                self.active_cell = None
            else:
                print("Move Not Valid")
                self.active_cell = None

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