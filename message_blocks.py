class MessageBlocks:

    def __init__(self, channel, user1_name, user1_id):
        self.channel = channel
        self.username = "CsHess"
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""
        self.user1_name = user1_name
        self.user1_id = user1_id

    # Creates form for the challenge message
    def get_challenge_blocks(self):
        CHALLENGE_TEXT_BLOCK = {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": self.user1_name + " has challenged you to a match!",
            }
        }
        BUTTON_ACTION_BLOCK = {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Accept",
                    },
                    "style": "primary",
                    "value": self.user1_id,
                    "action_id": "accept_challenge"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Deny",
                    },
                    "style": "danger",
                    "value": self.user1_id,
                    "action_id": "deny_challenge"
                }
            ]
        }

        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                CHALLENGE_TEXT_BLOCK,
                BUTTON_ACTION_BLOCK
            ]
        }
