class MessageBlocks:

    # Creates form for the challenge message
    @staticmethod
    def get_challenge_blocks(channel, user1_name, user1_id):
        CHALLENGE_TEXT_BLOCK = {
            "type": "section",
            "text": {
                "type": "plain_text",
                "text": user1_name + " has challenged you to a match!",
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
                    "value": user1_id,
                    "action_id": "accept_challenge"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Deny",
                    },
                    "style": "danger",
                    "value": user1_id,
                    "action_id": "deny_challenge"
                }
            ]
        }

        return {
            "channel": channel,
            "blocks": [
                CHALLENGE_TEXT_BLOCK,
                BUTTON_ACTION_BLOCK
            ]
        }

    @staticmethod
    def get_color_selection_block(channel, challenger_id):
        return {
            "channel": channel,
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "plain_text",
                        "text": "Would you rather play with:",
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "White \u2659"
                            },
                            "value": challenger_id,
                            "action_id": "white_pieces"
                        },
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "Black \u265F"
                            },
                            "value": challenger_id,
                            "action_id": "black_pieces"
                        }
                    ]
                }
            ]
        }
