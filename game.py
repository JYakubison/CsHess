import os
import chess

class Game:

    def __init__(self, user1_id, user2_id, channel_id):
        self.user1_id = user1_id
        self.user2_id = user2_id
        self.channel_id = channel_id