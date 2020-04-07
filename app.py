import os
from flask import Flask, request
from slack import WebClient
from slackeventsapi import SlackEventAdapter
import chess

# Initializing the Flask app to host event adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(os.environ['CSHESS_SLACK_SIGNING_SECRET'], "/slack/events", app)

# Initializing web API client
slack_web_client = WebClient(token=os.environ['CSHESS_SLACK_BOT_TOKEN'])


# Expects input in form /challenge @user
@app.route('/slack/challenge', methods=['POST'])
def challenge():
    user_input = request.form['text']

    # Pretty poor way of confirming the format, REVISIT
    if user_input.startswith("<@"):
        user_id = user_input[2:user_input.index("|")]
    else:
        return "Incorrect Format"

    user_info = slack_web_client.users_info(user=user_id)

    return "Sent a challenge to: " + user_info['user']['name']


# Recieves Button input
# @app.route('/button', method=['GET'])
@slack_events_adapter.on("button")
def button(event_data):
    # Accept Button
    if event_data["event"]["text"] == "Accept":
        sender_id = event_data["event"]["value"]
    # Deny Button
    if event_data["event"]["text"] == "Deny":
        slack_events_adapter.chat.delete(slack_web_client, )


# Running the app
if __name__ == "__main__":
    app.run(port=3000)
