import os
from flask import Flask, request
from slack import WebClient
from slackeventsapi import SlackEventAdapter
import chess
from message_blocks import MessageBlocks

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
@app.route('/slack/interactive')
def button(event_data):
    # Checks for type button
    if event_data["actions"]["type"] == "button":
        # Accept Button
        if event_data["actions"]["action_id"] == "accept_challenge":
            sender_id = event_data["event"]["value"]
        # Deny Button
        if event_data["actions"]["action_id"] == "deny_challenge":
            slack_events_adapter.chat_delete()


# Running the app
if __name__ == "__main__":
    app.run(port=3000)
