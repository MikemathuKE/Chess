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
        if self.cell_highlight:
            self.cell_highlight.draw()
        if self.king_check_highlight:
            self.king_check_highlight.draw()

    def change_turn(self) -> None:
        if self.player_turn == Color.WHITE:
            self.player_turn = Color.BLACK
        else:
            self.player_turn = Color.WHITE

    def find_piece_by_position(self, _position: tuple):
        for character in self.characters:
            if character.get_grid_position() == _position:
                return character
        return None
    
    def find_piece_by_character(self, type, color):
        for character in self.characters:
            if isinstance(character, type):
                if color == character.get_piece_color():
                    return character
        return None
    
    def set_active_cell(self, _position: tuple):
        self.active_cell = _position
        if _position:
            center_x, center_y = Position(_position[0], _position[1]).get_center_pixel()
            self.cell_highlight = arcade.create_rectangle_outline(center_x=center_x, center_y=center_y, width=Position.MULTIPLIER, height=Position.MULTIPLIER, color=arcade.color.GREEN, border_width=5)
        else:
            self.cell_highlight = None

    def set_king_check(self, _position: tuple):
        if _position:
            center_x, center_y = Position(_position[0], _position[1]).get_center_pixel()
            self.king_check_highlight = arcade.create_rectangle_outline(center_x=center_x, center_y=center_y, width=Position.MULTIPLIER, height=Position.MULTIPLIER, color=arcade.color.RED, border_width=2)
        else:
            self.king_check_highlight = None

    def on_mouse_press(self, x, y, button, modifiers):
        click_pos = Position.interpret_position(x, y)

        if self.active_cell is None:
            piece = self.find_piece_by_position(click_pos)
            if piece:
                if piece.get_piece_color() == self.player_turn:
                    self.set_active_cell(click_pos)
                    # print(f"Active Cell: {self.active_cell}")
        else:
            active_character = None

            new_selection = self.find_piece_by_position(click_pos)
            if new_selection:
                if new_selection.get_piece_color() == self.player_turn:
                    self.set_active_cell(click_pos)
                    return

            #  Retrieve the active character
            active_character = self.find_piece_by_position(self.active_cell)

            # Calculate the direction and steps
            direction, steps = Movement.calculate_direction(self.active_cell, click_pos, active_character.is_inversed())

            # Check if the move is valid
            if active_character.move_valid(direction, steps):
                move_possible = True
                kill_piece = None

                # Check each step to see if there is a piece in the way
                move_possible, kill_piece = self.is_path_clear(active_character, self.active_cell, direction, steps)

                # If the move is valid, move the piece
                if move_possible:
                    allow_move = True
                    king_move = False
                    if isinstance(active_character, Pawn):
                        if ((direction == Movement.FORWARD_LEFT) or (direction == Movement.FORWARD_RIGHT)) and kill_piece:
                            allow_move = self.pawn_attack(active_character, direction, steps, kill_piece)
                        elif active_character.is_first_move():
                            allow_move = self.pawn_first_move(active_character, direction, steps)
                        elif (direction == Movement.FORWARD_LEFT) or (direction == Movement.FORWARD_RIGHT):
                            allow_move = self.pawn_en_passant(active_character, direction, steps)
                        elif self.get_piece_rank(active_character) == 8:
                            allow_move = self.pawn_upgrade(active_character)
                    if isinstance(active_character, King):
                        king_move = True
                        if steps == 2:
                            allow_move = self.king_castle(active_character, direction, steps)
                        if allow_move:
                            active_character.set_max_steps(1)

                    if allow_move:
                        print(self.active_cell)
                        if not self.is_checked_king(self.player_turn, self.active_cell, click_pos, king_move):
                            active_character.move(click_pos)
                            if kill_piece:
                                kill_piece.kill()
                                self.characters.remove(kill_piece)
                            self.set_active_cell(None)
                            self.change_turn()
                            self.is_checked_king(self.player_turn, None, None)
                    else:
                        print("Move Not Allowed")
                        self.set_active_cell(None)
                else:
                    print("Move Not Possible")
                self.set_active_cell(None)
            else:
                print("Move Not Valid")
                self.set_active_cell(None)

    def is_path_clear(self, piece, next_position: tuple, direction: str, steps: int, exclusion = None, inclusion = None):
        move_possible = False
        kill_piece = None
        for step in range(steps):
            next_position = Movement.predict_position(next_position, direction, 1, piece.is_inversed())

            kill_piece = self.find_piece_by_position(next_position)
            if kill_piece:
                if exclusion and (kill_piece.get_grid_position() == exclusion):
                    move_possible = True
                    kill_piece = None
                    break
                elif kill_piece.get_piece_color() == piece.get_piece_color():
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
            elif inclusion:
                if next_position == inclusion:
                    move_possible = False
                    kill_piece = None
                    print("A Position in the way will be occupied")
                    break
            else:
                # If there is no piece in the way, the move is possible
                move_possible = True
                pass

            if next_position[0] < 0 or next_position[1] < 0:
                return False, None
        return move_possible, kill_piece

    def pawn_upgrade(self, _pawn: Pawn) -> bool:                
        return False
    
    def pawn_first_move(self, _pawn: Pawn, direction: str, steps: int) -> bool:
        if steps <= 2:
            if direction == Movement.FORWARD:
                if _pawn.is_first_move():
                    _pawn.set_max_steps(1)
                    print("Taking Pawn First Steps")
                    return True
        print("Not Taking Pawn First Steps")
        return False
    
    def get_piece_rank(self, _piece) -> int:
        if _piece.get_piece_color() == Color.WHITE:
            return _piece.get_grid_position()[1] + 1
        else:
            return 8 - _piece.get_grid_position()[1]
    
    def pawn_en_passant(self, _pawn: Pawn, direction: str, steps: int) -> bool:
        if (direction == Movement.FORWARD_LEFT) or (direction == Movement.FORWARD_RIGHT):
            if steps == 1:
                # TODO: Check if previous move was a 2step opening move of a pawn
                print("Pawn En Passant")
                return False
        return False                    

    def pawn_attack(self, _pawn: Pawn, direction: str, steps: int, kill_piece) -> bool:
        if (direction == Movement.FORWARD_LEFT) or (direction == Movement.FORWARD_RIGHT):
            if steps == 1:
                if kill_piece:
                    if _pawn.is_first_move():
                        _pawn.set_max_steps(1)
                    print("Pawn Taking Another Piece")
                    return True
        print("Pawn Not Attacking")
        return False


    def king_castle(self, _king: King, direction: str, steps: int) -> bool:
        possible_castle = False
        expected_rook_pos = None
        if _king.get_piece_color() == Color.WHITE:
            if steps == 2:
                if direction == Movement.LEFT:
                    curr_rook_pos = (0, 0)
                    expected_rook_pos = (3, 0)
                    possible_castle = True
                    rook_steps = 3
                elif direction == Movement.RIGHT:
                    curr_rook_pos = (7, 0)
                    expected_rook_pos = (5, 0)
                    possible_castle = True
                    rook_steps = 2
        elif _king.get_piece_color() == Color.BLACK:
            if steps == 2:
                if direction == Movement.LEFT:
                    curr_rook_pos = (7, 7)
                    expected_rook_pos = (5, 7)
                    possible_castle = True
                    rook_steps = 3
                elif direction == Movement.RIGHT:
                    curr_rook_pos = (0, 7)
                    expected_rook_pos = (3, 7)
                    possible_castle = True
                    rook_steps = 2

        if possible_castle:
            castle_piece = self.find_piece_by_position(curr_rook_pos)
            if isinstance(castle_piece, Rook):
                if castle_piece.is_first_move():
                    if castle_piece.get_piece_color() == _king.get_piece_color():
                        if direction == Movement.LEFT:
                            rook_move = Movement.RIGHT
                        else:
                            rook_move = Movement.LEFT
                        move_possible, kill_piece = self.is_path_clear(castle_piece, curr_rook_pos, rook_move, rook_steps)
                        if move_possible:
                            castle_piece.move(expected_rook_pos)
                            print(f"Castle allowed {expected_rook_pos}")
                            return True
        return False

    def is_checked_king(self, color: Color, exclusion, inclusion, king_move = False) -> bool:
            
        king = self.find_piece_by_character(King, color)
        if king_move:
            king_pos = inclusion
            inclusion = None
        else:
            king_pos = king.get_grid_position()
        self.checking_pieces[color] = []
        for character in self.characters:
            if character.get_piece_color() != color:
                if not character.matches(king):
                    direction, steps = Movement.calculate_direction(character.get_grid_position(), king_pos, color == Color.WHITE)
                    if direction:
                        if character.move_valid(direction, steps):
                            if self.is_path_clear(character, character.get_grid_position(), direction, steps, exclusion, inclusion)[0]:
                                self.checking_pieces[color].append(character.get_grid_position())

        if inclusion in self.checking_pieces[color]:
            self.checking_pieces[color].remove(inclusion)                    
        if len(self.checking_pieces[color]) > 0:
            if not inclusion:
                self.set_king_check(king.get_grid_position())
            string_color = "White" if color == Color.WHITE else "Black"
            print(f"Pieces checking {string_color} king", self.checking_pieces)
            return True
        self.set_king_check(None)
        return False


    def is_check_mate(self) -> bool:
        pass

    def init_board(self):
        self.set_active_cell(None)
        self.display_board = arcade.ShapeElementList()

        light_bg = arcade.color.BLUE_GRAY
        dark_bg = arcade.color.BLUE_SAPPHIRE
        
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

        self.cell_highlight = None
        self.king_check_highlight = None
        self.checking_pieces = {
            Color.WHITE: [],
            Color.BLACK: []
        }

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