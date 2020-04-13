import os
import chess


class Game:

    def __init__(self, challenger_name, recipient_name, challenger_id, recipient_id, channel, recipient_color):
        # Setting the colors of the players
        if recipient_color == chess.WHITE:
            self.white_name = recipient_name
            self.white_id = recipient_id
            self.black_name = challenger_name
            self.black_id = challenger_id
        else:
            self.black_name = recipient_name
            self.black_id = recipient_id
            self.white_name = challenger_name
            self.white_id = challenger_id

        self.channel = channel

        self.game_board = chess.Board(
            fen=chess.STARTING_FEN)  # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

    def start_game_message(self):
        DIVIDER_BLOCK = {"type": "divider"}
        HEADING_BLOCK = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": " ♖ *New Game Starting!* ♜"
            }
        }
        PLAYER_BLOCK = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "\u2654 *White* - " + self.white_name + "\n \u265A *Black*  - " + self.black_name
            }
        }
        return {
            "channel": self.channel,
            "blocks": [
                DIVIDER_BLOCK,
                DIVIDER_BLOCK,
                HEADING_BLOCK,
                PLAYER_BLOCK
            ],
            "text": "New Game Starting!"
        }

    # TEMPORARY FIX TILL CUSTOM PRINT IS CREATED
    # Make More customized board print function in future
    def print_board_block(self):
        DIVIDER_BLOCK = {"type": "divider"}
        BOARD_BLOCK = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": self.game_board.unicode()
            }
        }

        if self.game_board.turn == chess.WHITE:
            current_turn = " It's White's - " + self.white_name + "'s turn!\n"
        else:
            current_turn = " It's Black's - " + self.black_name + "'s turn!\n"
        CURRENT_TURN_BLOCK = {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": current_turn
            }
        }

        return {
            "channel": self.channel,
            "blocks": [
                DIVIDER_BLOCK,
                BOARD_BLOCK,
                CURRENT_TURN_BLOCK,
                DIVIDER_BLOCK
            ],
            "text": "It is " + self.get_turn() + "'s Turn!"
        }

    # Checks a move and makes it if valid, returns a string with either: success_move, invlalid_move, out_of_turn, invalid_user, invalid_form
    def check_move(self, user_id, move_text):
        # Checks if white user posted, and if it is their turn
        if self.game_board.turn == chess.WHITE and user_id == self.white_id:
            try:
                new_move = chess.Move.from_uci(uci=move_text)

                # Checks if move is legal
                if new_move in self.game_board.legal_moves:
                    self.game_board.push(new_move) # Pushes new move to the board
                    return "success_move"
                else:
                    return "invalid_move"
            except ValueError: # Triggers if new move is in an invalid form
                return "invalid_form"

        # Checks if black user poster, and if it is their turn
        elif self.game_board.turn == chess.BLACK and user_id == self.black_id:
            try:
                new_move = chess.Move.from_uci(uci=move_text)

                # Checks if move is legal
                if new_move in self.game_board.legal_moves:
                    self.game_board.push(new_move) # Pushes new move to the board
                    return "success_move"
                else:
                    return "invalid_move"
            except ValueError: # Triggers if new move is in an invalid form
                return "invalid_form"
        elif user_id == self.white_id or user_id == self.black_id:
            return "out_of_turn"
        else:
            return "invalid_user"

    # Returns the current turn as "White" or "Black"
    def get_turn(self):
        if self.game_board.turn == chess.WHITE:
            return "White"
        else:
            return "Black"
