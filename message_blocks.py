class MessageBlocks:
    CHALLENGE_TEXT_BLOCK = {
        "type": "section",
        "text": {
            "type": "plain_text",
            "text": " has challenged you to a match!",
        }
    }
    def get_challenge_block(self, channel_id):
        return

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
                "value": "true"
            },
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Deny",
                },
                "style": "danger",
                "value": "click_me_123"
            }
        ]
    }
