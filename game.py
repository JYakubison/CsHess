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

    # Returns the current turn as "White" or "Black"
    def get_turn(self):
        if self.game_board.turn == chess.WHITE:
            return "White"
        else:
            return "Black"
