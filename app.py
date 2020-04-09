import os
from flask import Flask, request
from slack import WebClient
from slackeventsapi import SlackEventAdapter
import chess
from message_blocks import MessageBlocks
import json

# Initializing the Flask app to host event adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(os.environ['CSHESS_SLACK_SIGNING_SECRET'], "/slack/events", app)

# Initializing web API client
slack_web_client = WebClient(token=os.environ['CSHESS_SLACK_BOT_TOKEN'])

# Dictionary to hold all of the challenges
challenges_dictionary = {}


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

    m_blocks = MessageBlocks(channel=challenge_channel_id,
                             user1_name=user1_info["user"]["profile"]["display_name"],
                             user1_id=user1_id)

    challenge_response = slack_web_client.chat_postMessage(**m_blocks.get_challenge_blocks(), text="You have been "
                                                                                                   "challenged by " +
                                                                                                   user1_info[
                                                                                                       "user"][
                                                                                                       "profile"][
                                                                                                       "display_name"])

    return "Sent a challenge to: " + user2_info["user"]["profile"]["display_name"]


# Recieves Button input
# @app.route('/button', method=['GET'])
@app.route('/slack/interactive', methods=["POST"])
def button():
    payload_data = json.loads(request.form["payload"])
    # Checks for type button

    if payload_data["actions"][0]["type"] == "button":

        # Info of user who clicked on the button and who sent the challenge
        receiver_info = slack_web_client.users_info(user=payload_data["user"]["id"])
        receiver_id = receiver_info["user"]["id"]
        
        sender_info = slack_web_client.users_info(user=payload_data["actions"][0]["value"])
        sender_id = sender_info["user"]["id"]
    
        # Accept Button
        if payload_data["actions"][0]["action_id"] == "accept_challenge":
            sender = 0
        # Deny Button
        if payload_data["actions"][0]["action_id"] == "deny_challenge":
            slack_web_client.chat_delete(channel=payload_data["channel"]["id"], ts=payload_data["message"]["ts"])
            # Print Challenge Denied message to reciever
            slack_web_client.chat_postMessage(channel=payload_data["channel"]["id"],
                                              text=sender_info["user"]["profile"]["display_name"] + "\'s challenge "
                                                                                                    "was denied")

            # Opening a conversation to tell sender challenge was denied
            response = slack_web_client.conversations_open(users=sender_id)
            challenge_channel_id = response["channel"]["id"]
            slack_web_client.chat_postMessage(channel=challenge_channel_id,
                                              text=receiver_info["user"]["profile"]["display_name"] + " denied your "
                                                                                                      "challenge")


# Running the app
if __name__ == "__main__":
    app.run(port=3000)
