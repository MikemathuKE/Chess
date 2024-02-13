import arcade, yaml, time
from utils.utils import *
from characters.King import King
from characters.Queen import Queen
from characters.Bishop import Bishop
from characters.Knight import Knight
from characters.Rook import Rook
from characters.Pawn import Pawn
from pyglet.image import load as pyglet_load

class PawnSwitch(arcade.View):
    def __init__(self, window, game_view, color: Color, upgrade_piece: Pawn):
        self.window = window
        self.color = color
        self.upgrade_piece = upgrade_piece
        self.game_view = game_view
        super().__init__(self.window)

    def on_draw(self):
        self.background.draw()
        self.text.draw()

        light_bg = arcade.color.BLUE_GRAY
        dark_bg = arcade.color.BLUE_SAPPHIRE
        
        def swap_color(color: str) -> str:
            if color == light_bg:
                color = dark_bg
            elif color == dark_bg:
                color = light_bg
            return color

        color = light_bg
        for i in range(2,6):
            center_x, center_y = Position(i, 3).get_center_pixel()
            cell_highlight = arcade.create_rectangle_filled(center_x=center_x, center_y=center_y, width=Position.MULTIPLIER, height=Position.MULTIPLIER, color=color)
            cell_highlight.draw()
            color = swap_color(color)

        self.rook.draw()
        self.queen.draw()
        self.knight.draw()
        self.bishop.draw()

    def on_show_view(self):
        self.background = arcade.create_rectangle_filled(center_x=self.window.width/2, center_y=self.window.height/2, width=self.window.width, height=self.window.height, color=arcade.color.AIR_FORCE_BLUE)
        self.text = arcade.create_text_sprite("Choose Piece to Upgrade To: ", self.window.width/3, self.window.height*2/3, color=arcade.color.WHITE_SMOKE, font_size=20)

        color_str = "white" if self.color == Color.WHITE else "black"
        self.rook = Rook(Position(2, 3), Color.WHITE, f"{color_str}_rook.png")
        self.queen = Queen(Position(3, 3), Color.WHITE, f"{color_str}_queen.png")
        self.knight = Knight(Position(4, 3), Color.WHITE, f"{color_str}_knight.png")
        self.bishop = Bishop(Position(5, 3), Color.WHITE, f"{color_str}_bishop.png")

    def on_mouse_press(self, x, y, button, modifiers):
        pos = Position.interpret_position(x, y)
        if pos == self.rook.get_grid_position():
            self.game_view.upgrade_pawn(self.upgrade_piece, self.rook)
        elif pos == self.queen.get_grid_position():
            self.game_view.upgrade_pawn(self.upgrade_piece, self.queen)
        elif pos == self.knight.get_grid_position():
            self.game_view.upgrade_pawn(self.upgrade_piece, self.knight)
        elif pos == self.bishop.get_grid_position():
            self.game_view.upgrade_pawn(self.upgrade_piece, self.bishop)

        self.window.show_view(self.game_view)

class WinnerView(arcade.View):
    def __init__(self, window: arcade.Window, winner: Color, last_board, last_play):
        super().__init__(window)
        self.window = window
        self.winner = winner
        self.last_board = last_board
        self.last_play = last_play


    def setup(self):
        color_str = "WHITE" if self.winner == Color.WHITE else "BLACK"
        text_color = arcade.color.WHITE_SMOKE if self.winner == Color.WHITE else arcade.color.BLACK_OLIVE
        self.background = arcade.create_rectangle_filled(center_x=self.window.width/2, center_y=self.window.height/2, width=self.window.width, height=self.window.height, color=text_color)
        self.text = arcade.create_text_sprite(f"CHECK MATE! {color_str} WINS!", self.window.width/5, self.window.height*2/3, color=text_color, font_size=40)

    def on_draw(self):
        self.background.draw()
        self.last_board.draw()
        self.last_play.draw()
        self.text.draw()

    def on_show_view(self):
        self.setup()
        # print(self.winner)
        

class GameView(arcade.View):
    def __init__(self, window: arcade.Window):
        super().__init__(window)
        self.window = window

    def setup(self):
        self.asset_dir = "./assets"
        self.player_turn = Color.WHITE
        self.winner = None
        self.killed_pieces = {}
        self.init_board()
        self.init_characters()
        self.win_sound = arcade.load_sound(f"{self.asset_dir}/win.wav")
        self.move_sound = arcade.load_sound(f"{self.asset_dir}/move.wav")
        self.attack_sound = arcade.load_sound(f"{self.asset_dir}/attack.wav")
        self.check_sound = arcade.load_sound(f"{self.asset_dir}/check.wav")

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
                        allow_move, kill_piece = self.is_pawn_move_allowed(active_character, direction, steps, kill_piece)
                    if isinstance(active_character, King):
                        king_move = True
                        if steps == 2:
                            allow_move = self.king_castle(active_character, direction, steps)
                            if allow_move:
                                active_character.set_max_steps(1)

                    if allow_move:
                        # print(self.active_cell)
                        if not self.is_checked_king(self.player_turn, self.active_cell, click_pos, king_move):
                            self.add_history(active_character, active_character.get_grid_position(), click_pos, steps, direction)
                            active_character.move(click_pos)
                            if kill_piece:
                                kill_piece.kill()
                                self.characters.remove(kill_piece)
                                arcade.play_sound(self.attack_sound)
                            else:
                                arcade.play_sound(self.move_sound)
                            self.set_active_cell(None)
                            self.change_turn()
                            if self.king_check_logic():
                                # print("Game Over")
                                arcade.play_sound(self.win_sound)
                                self.winner = Color.WHITE if self.player_turn == Color.BLACK else Color.BLACK
                                winner_view = WinnerView(self.window, self.winner, self.display_board, self.characters)
                                self.window.show_view(winner_view)
                            if self.king_check_highlight:
                                arcade.play_sound(self.check_sound)
                            
                    else:
                        # print("Move Not Allowed")
                        self.set_active_cell(None)
                else:
                    # print("Move Not Possible")
                    self.set_active_cell(None)
            else:
                # print("Move Not Valid")
                self.set_active_cell(None)
        self.serialize_game(self.gametimestamp)

    def king_check_logic(self) -> bool:
        on_check = self.is_checked_king(self.player_turn, None, None, actual_check=True)

        if on_check:
            if self.is_check_mate(self.player_turn):
                return True
        else:
            self.set_king_check(None)
        return False

    def is_pawn_move_allowed(self, active_character, direction, steps, kill_piece):
        allow_move = True
        if isinstance(active_character, Pawn):
            # print(self.get_piece_rank(active_character))
            if ((direction == Movement.FORWARD) and kill_piece):
                allow_move = False
                kill_piece = None
            elif ((direction == Movement.FORWARD_LEFT) or (direction == Movement.FORWARD_RIGHT)) and kill_piece:
                allow_move = self.pawn_attack(active_character, direction, steps, kill_piece)
            elif active_character.is_first_move():
                allow_move = self.pawn_first_move(active_character, direction, steps)
                kill_piece = None            
            elif (direction == Movement.FORWARD_LEFT) or (direction == Movement.FORWARD_RIGHT):
                # print("Checking for En Passant")
                allow_move, kill_piece_pos = self.pawn_en_passant(active_character, direction, steps)
                kill_piece = self.find_piece_by_position(kill_piece_pos)
            
            if self.get_piece_rank(active_character) == 7:
                pawn_view = PawnSwitch(self.window, self, self.player_turn, active_character)
                self.window.show_view(pawn_view)
        return allow_move, kill_piece

    def is_path_clear(self, piece, next_position: tuple, direction: str, steps: int, exclusion = None, inclusion = None):
        move_possible = False
        kill_piece = None
        for step in range(steps):
            next_position = Movement.predict_position(next_position, direction, 1, piece.is_inversed())

            kill_piece = self.find_piece_by_position(next_position)
            if kill_piece:
                if exclusion and (kill_piece.get_grid_position() in exclusion):
                    move_possible = True
                    kill_piece = None
                    break
                elif kill_piece.get_piece_color() == piece.get_piece_color():
                    # If it is the same color, the move is not possible
                    # print("Same color piece in the way ", kill_piece.get_name())
                    move_possible = False
                    kill_piece = None
                    break
                elif step != steps - 1:
                    # If steps do not match current pos, the move is not possible
                    move_possible = False
                    kill_piece = None
                    # print("Another piece is blocking the way")
                    break
                else:
                    # If it is not the same color and steps do not match current pos, the move is possible
                    move_possible = True
                    break
            elif inclusion:
                if next_position == inclusion:
                    move_possible = False
                    kill_piece = None
                    # print("A Position in the way will be occupied")
                    break
            else:
                # If there is no piece in the way, the move is possible
                move_possible = True
                pass

            if next_position[0] < 0 or next_position[1] < 0:
                return False, None
            if next_position[0] >= 8 or next_position[1] >= 8:
                return False, None
        return move_possible, kill_piece

    def upgrade_pawn(self, _pawn: Pawn, new_piece) -> None:
        position = _pawn.get_grid_position()
        new_piece.set_grid_position(Position(position[0], position[1]))
        self.characters.remove(_pawn)
        self.characters.append(new_piece)
        self.king_check_logic()
        self.serialize_game(self.gametimestamp)
    
    def pawn_first_move(self, _pawn: Pawn, direction: str, steps: int) -> bool:
        if steps <= 2:
            if direction == Movement.FORWARD:
                if _pawn.is_first_move():
                    _pawn.set_max_steps(1)
                    # print("Taking Pawn First Steps")
                    return True
        # print("Not Taking Pawn First Steps")
        return False
    
    def get_piece_rank(self, _piece) -> int:
        if _piece.get_piece_color() == Color.WHITE:
            return _piece.get_grid_position()[1] + 1
        else:
            return 8 - _piece.get_grid_position()[1]
    
    def pawn_en_passant(self, _pawn: Pawn, direction: str, steps: int) -> bool:
        if isinstance(_pawn, Pawn):
            if (direction == Movement.FORWARD_LEFT) or (direction == Movement.FORWARD_RIGHT):
                if steps == 1:
                    last_move = self.history[-1]
                    if "_pawn" in last_move["piece"]:
                        if last_move["piece"] != _pawn.get_name():
                            if last_move["steps"] == 2:
                                pawn_pos = _pawn.get_grid_position()
                                if (last_move["_to"][1] == pawn_pos[1]) and ((last_move["_to"][0] == pawn_pos[0]-1) or (last_move["_to"][0] == pawn_pos[0]+1)):
                                    return True, last_move["_to"]
        return False, None                 

    def pawn_attack(self, _pawn: Pawn, direction: str, steps: int, kill_piece) -> bool:
        if (direction == Movement.FORWARD_LEFT) or (direction == Movement.FORWARD_RIGHT):
            if steps == 1:
                if kill_piece:
                    if _pawn.is_first_move():
                        _pawn.set_max_steps(1)
                    # print("Pawn Taking Another Piece")
                    return True
        # print("Pawn Not Attacking")
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
                            # print(f"Castle allowed {expected_rook_pos}")
                            return True
        return False
    
    def is_check_mate(self, color: Color) -> bool:
        king = self.find_piece_by_character(King, color)
        # print("Checking for Check Mate for ", king.get_piece_color())

        no_fix = True
        for movt in king.get_direction_constraints():
            expected_king_pos = Movement.predict_position(king.get_grid_position(), movt, 1, king.is_inversed())
            move_possible, kill_piece = self.is_path_clear(king, king.get_grid_position(), movt, 1)
            if move_possible:
                # print(f"Checking for King move from {king.get_grid_position()} to {expected_king_pos}")
                if not self.is_checked_king(color, king.get_grid_position(), expected_king_pos, king_move=True):
                    no_fix = False
                    # print(f"Expected King Pos freeing from check: {expected_king_pos}")
                    break
        
        pawn_count = 0
        if no_fix:
            # print("King Cannot Move")
            for character in self.characters:
                if character.get_piece_color() == color:
                    if not isinstance(character, King):
                        for movt in character.get_direction_constraints():
                            for steps in range(1, character.get_max_steps()+1):
                                expected_character_pos = Movement.predict_position(character.get_grid_position(), movt, steps, character.is_inversed())
                                move_possible, kill_piece = self.is_path_clear(character, character.get_grid_position(), movt, steps, None, None)
                                if move_possible:
                                    allow_move = True
                                    if isinstance(character, Pawn):
                                        allow_move, kill_piece = self.is_pawn_move_allowed(character, movt, steps, kill_piece)
                                    if allow_move:
                                        if not self.is_checked_king(color, exclusion=character.get_grid_position(), inclusion=expected_character_pos, moved_char=character):
                                            no_fix = False
                                            # print(f"Piece {character.get_name()} at {character.get_grid_position()} blocks king by moving to {expected_character_pos} and attacking {kill_piece}")
                                            break

        if no_fix:
            # print("Check Mate")
            pass
        
        return no_fix

    def is_checked_king(self, color: Color, exclusion: tuple, inclusion: tuple, king_move = False, moved_char = None, actual_check=False) -> bool:            
        king = self.find_piece_by_character(King, color)
        if king_move:
            king_pos = inclusion
            inclusion = None
        else:
            king_pos = king.get_grid_position()
        self.checking_pieces[color] = []
        for character in self.characters:
            if character.get_piece_color() != color:
                # if (king_move and (character.get_grid_position() == inclusion)) or (not king_move):
                    if not character.matches(king):
                        if moved_char:
                            if character.matches(moved_char):
                                direction, steps = Movement.calculate_direction(moved_char.get_grid_position(), king_pos, color == Color.WHITE)
                            else:
                                direction, steps = Movement.calculate_direction(character.get_grid_position(), king_pos, color == Color.WHITE)
                        else:
                            direction, steps = Movement.calculate_direction(character.get_grid_position(), king_pos, color == Color.WHITE)
                        # print(f"Checking Piece {character.get_name()} at {character.get_grid_position()} moving to ", Movement.predict_position(character.get_grid_position(), direction, steps))

                        if direction:
                            if character.move_valid(direction, steps):
                                # print(direction, steps)
                                if king_move:
                                    path_clear = self.is_path_clear(character, character.get_grid_position(), direction, steps, [exclusion, king_pos])[0]
                                else:
                                    path_clear = self.is_path_clear(character, character.get_grid_position(), direction, steps, [exclusion], inclusion)[0]

                                if path_clear:
                                    self.checking_pieces[color].append(character.get_grid_position())
                                    # print(f"Checking piece {character.get_name()} at {character.get_grid_position()}")

        # print(self.checking_pieces[color])
        if inclusion in self.checking_pieces[color]:
            self.checking_pieces[color].remove(inclusion)                    
        if len(self.checking_pieces[color]) > 0:
            if actual_check:
                self.set_king_check(king.get_grid_position())
            # string_color = "White" if color == Color.WHITE else "Black"
            # print(f"Pieces checking {string_color} king", self.checking_pieces)
            return True
        return False

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

        self.history = []
        game_data = self.deserialize_game("game_start", "bin")
        for key in game_data.keys():
            if key == "player_turn":
                self.player_turn = game_data[key]
            elif key == "killed_pieces":
                self.killed_pieces = game_data[key]
            elif key == "history":
                self.history = game_data[key]
            elif "_rook" in key:
                for piece in game_data[key]:
                    self.characters.append(Rook(Position(piece["position"][0], piece["position"][1]), piece["color"], piece["texture"]))
            elif "_knight" in key:
                for piece in game_data[key]:
                    self.characters.append(Knight(Position(piece["position"][0], piece["position"][1]), piece["color"], piece["texture"]))
            elif "_bishop" in key:
                for piece in game_data[key]:
                    self.characters.append(Bishop(Position(piece["position"][0], piece["position"][1]), piece["color"], piece["texture"]))
            elif "_queen" in key:
                for piece in game_data[key]:
                    self.characters.append(Queen(Position(piece["position"][0], piece["position"][1]), piece["color"], piece["texture"]))
            elif "_king" in key:
                for piece in game_data[key]:
                    self.characters.append(King(Position(piece["position"][0], piece["position"][1]), piece["color"], piece["texture"]))
            elif "_pawn" in key:
                for piece in game_data[key]:
                    self.characters.append(Pawn(Position(piece["position"][0], piece["position"][1]), piece["color"], piece["texture"]))

        self.gametimestamp = "game_"+str(time.time())
        self.serialize_game(self.gametimestamp)

    def add_history(self, _piece, start_pos: tuple, end_pos: tuple, steps, direction):
        self.history.append({
            "piece": _piece.get_name(),
            "_from": start_pos,
            "_to": end_pos,
            "steps": steps,
            "direction": direction
        })

    def serialize_game(self, title="game", folder='game'):
        character_map = {
            "player_turn": self.player_turn,
            "killed_pieces": self.killed_pieces,
            "history": self.history,
            "winner": self.winner,
            "white_rook": [],
            "black_rook": [],
            "white_knight": [],
            "black_knight": [],
            "white_bishop": [],
            "black_bishop": [],
            "white_queen": [],
            "black_queen": [],
            "white_king": [],
            "black_king": [],
            "white_pawn": [],
            "black_pawn": []
        }

        for character in self.characters:
            curr = character_map[character.get_name()].append({
                "position": character.get_grid_position(),
                "color": character.get_piece_color(),
                "texture": character.get_name() + ".png"
            })

        data = yaml.dump(character_map, default_flow_style=False)
        with open(f"./{folder}/{title}.yml", "w") as file:
            file.write(data)
        self.king_check_logic()

    def deserialize_game(self, file_name, folder="game"):
        with open(f"./{folder}/{file_name}.yml", "r") as file_name:
            data = yaml.load(file_name, Loader=yaml.Loader)
        return data

class Chess(arcade.Window):
    def __init__(self):
        super().__init__(900, 900, "Chess")
        arcade.set_background_color(arcade.color.AIR_FORCE_BLUE)
        gameview = GameView(self)
        gameview.setup()
        self.show_view(gameview)
        self.set_icon(pyglet_load("./assets/Icon.ico"))