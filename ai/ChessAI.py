from utils.utils import *

class ChessAI:

    def __init__(self, color: Color) -> None:
        self.color = color
        self.comp_vision = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]

        ### BIASES ###
        self.game_stage = float(0) # Weight that Evaluates at what stage the game is in, some evaluation functions take precedence when at later stages of the game
        self.defense_weight = float(1) # Weight that Evaluates when defense is paramount
        self.attack_weight = float(0) # Weight that Evaluates when attack is paramount

    ### CHESS BOARD VIEW/UPDATE ###
    def view_board(self, character_pieces) -> None:
        for character in character_pieces:
            pos_x, pos_y = character.get_position().get_grid_position()
            self.comp_vision[pos_x][pos_y] = character.get_id()

    def update_piece_movt(self, original_pos, new_pos) -> None:
        piece = self.comp_vision[original_pos[0]][original_pos[1]]
        self.comp_vision[original_pos[0]][original_pos[1]] = 0
        self.comp_vision[new_pos[0]][new_pos[1]] = piece

    ### COST FUNCTIONS ###
    """Evaluation function to check if pieces are defended"""
    def pieces_defended(self, character_pieces):
        pass
    
    """Evaluation function to check if the king is in danger"""
    def king_in_danger(self, character_pieces):
        pass

    """Evaluation function to check if queen is in danger"""
    def queen_in_danger(self, character_pieces):
        pass

    """Evaluation function to check if rook is in danger"""
    def rook_in_danger(self, character_pieces):
        pass

    """Evaluation function to check if bishop in danger"""
    def bishop_in_danger(self, character_pieces):
        pass
    
    """Evaluation function to check if knight in danger"""
    def knight_in_danger(self, character_pieces):
        pass

    """Evaluation function to check if ai controls the center of the board"""
    def center_in_control(self, character_pieces):
        pass

    """Evaluation function to check if ai has more pieces"""
    def more_pieces(self, character_pieces):
        pass

    """Evaluation function to check if pawn approaching upgrade"""
    def pawn_upgrade(self, character_pieces):
        pass

    """Evaluation function for attacking queen"""
    def attacking_queen(self, character_pieces):
        pass

    """Evaluation function for attacking king"""
    def attacking_king(self, character_pieces):
        pass

    """Evaluation function for attacking rook"""
    def attacking_rook(self, character_pieces):
        pass

    """Evaluation function for attacking bishop"""
    def attacking_bishop(self, character_pieces):
        pass

    """Evaluation function for attacking knight"""
    def attacking_knight(self, character_pieces):
        pass