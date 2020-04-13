import os
import json
import logging

from flask import Flask, request
from slack import WebClient
from slackeventsapi import SlackEventAdapter
import chess

from message_blocks import MessageBlocks
from game import Game

# Initializing the Flask app to host event adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(os.environ['CSHESS_SLACK_SIGNING_SECRET'], "/slack/events", app)

# Initializing web API client
slack_web_client = WebClient(token=os.environ['CSHESS_SLACK_BOT_TOKEN'])

game_dict = {}


# Expects input in form /challenge @user
@app.route('/slack/challenge', methods=['POST'])
def challenge():
    user_input = request.form['text']

    # Save the user info of the user who typed the command
    user1_info = slack_web_client.users_info(user=request.form['user_id'])
    user1_id = user1_info["user"]["id"]

    # Pretty poor way of confirming the format, REVISIT NEEDS TO BE OPTIMIZED
    if user_input.startswith("<@"):
        user2_id = user_input[2:user_input.index("|")]
    else:
        return "Incorrect Format"

    user2_info = slack_web_client.users_info(user=user2_id)

    # Opening a conversation with player being challenged
    response = slack_web_client.conversations_open(users=user2_id)
    challenge_channel_id = response["channel"]["id"]

    challenge_response = slack_web_client.chat_postMessage(**MessageBlocks.get_challenge_blocks(
        channel=challenge_channel_id,
        user1_name=user1_info["user"]["profile"]["display_name"],
        user1_id=user1_id),
                                                           text="You have been challenged by " +
                                                                user1_info["user"]["profile"]["display_name"])

    return "Sent a challenge to: " + user2_info["user"]["profile"]["display_name"]


# Recieves Button input
# @app.route('/button', method=['GET'])
@app.route('/slack/interactive', methods=["POST"])
def button():
    payload_data = json.loads(request.form["payload"])

    # Checks for type button
    if payload_data["actions"][0]["type"] == "button":

        # Recipient User
        receiver_info = slack_web_client.users_info(user=payload_data["user"]["id"])
        receiver_id = receiver_info["user"]["id"]

        # Challenger user
        sender_info = slack_web_client.users_info(user=payload_data["actions"][0]["value"])
        sender_id = sender_info["user"]["id"]

        # Accept Button
        if payload_data["actions"][0]["action_id"] == "accept_challenge":
            # Deleting message
            slack_web_client.chat_delete(channel=payload_data["channel"]["id"], ts=payload_data["message"]["ts"])
            # Post Color Select Message
            slack_web_client.chat_postMessage(**MessageBlocks.get_color_selection_block(
                channel=payload_data["channel"]["id"], challenger_id=sender_id),
                                              text="Select a color!")

        # Deny Button
        elif payload_data["actions"][0]["action_id"] == "deny_challenge":
            # Deleting message
            slack_web_client.chat_delete(channel=payload_data["channel"]["id"], ts=payload_data["message"]["ts"])
            # Print Challenge Denied message to receiver
            slack_web_client.chat_postMessage(channel=payload_data["channel"]["id"],
                                              text=sender_info["user"]["profile"][
                                                       "display_name"] + "\'s challenge was denied")

            # Opening a conversation to tell sender challenge was denied
            response = slack_web_client.conversations_open(users=sender_id)
            challenge_channel_id = response["channel"]["id"]
            slack_web_client.chat_postMessage(channel=challenge_channel_id,
                                              text=receiver_info["user"]["profile"][
                                                       "display_name"] + " denied your challenge")

        # White Pieces button
        elif payload_data["actions"][0]["action_id"] == "white_pieces":
            # Deleting message
            slack_web_client.chat_delete(channel=payload_data["channel"]["id"], ts=payload_data["message"]["ts"])
            slack_web_client.chat_postMessage(channel=payload_data["channel"]["id"],
                                              text="You selected white. Good Luck!")

            # Creating group DM for game
            dm_data = slack_web_client.conversations_open(users=[sender_id, receiver_id])

            # Saving game in dictionary
            game_dict[dm_data["channel"]["id"]] = Game(challenger_name=sender_info["user"]["profile"]["display_name"],
                                                       recipient_name=receiver_info["user"]["profile"]["display_name"],
                                                       challenger_id=sender_id,
                                                       recipient_id=receiver_id,
                                                       channel=dm_data["channel"]["id"],
                                                       recipient_color=chess.WHITE)

            # Starting game message
            slack_web_client.chat_postMessage(**game_dict[dm_data["channel"]["id"]].start_game_message())

            # Print Game Board
            slack_web_client.chat_postMessage(**game_dict[dm_data["channel"]["id"]].print_board_block())

        # Black Pieces button
        elif payload_data["actions"][0]["action_id"] == "black_pieces":
            # Deleting message
            slack_web_client.chat_delete(channel=payload_data["channel"]["id"], ts=payload_data["message"]["ts"])
            slack_web_client.chat_postMessage(channel=payload_data["channel"]["id"],
                                              text="You selected black. Good Luck!")
            # Creating group DM for game
            dm_data = slack_web_client.conversations_open(users=[sender_id, receiver_id])

            # Saving game in dictionary
            game_dict[dm_data["channel"]["id"]] = Game(challenger_name=sender_info["user"]["profile"]["display_name"],
                                                       recipient_name=receiver_info["user"]["profile"]["display_name"],
                                                       challenger_id=sender_id,
                                                       recipient_id=receiver_id,
                                                       channel=dm_data["channel"]["id"],
                                                       recipient_color=chess.BLACK)


            # Starting game message
            slack_web_client.chat_postMessage(**game_dict[dm_data["channel"]["id"]].start_game_message())

            # Print Game Board
            slack_web_client.chat_postMessage(**game_dict[dm_data["channel"]["id"]].print_board_block())

        return ""


# Running the app
if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    app.run(port=3000)
