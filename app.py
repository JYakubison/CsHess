import os
from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

# Initializing the Flask app to host event adapter
app = Flask(__name__)
slack_events_adapter = SlackEventAdapter(os.environ['CSHESS_SLACK_SIGNING_SECRET'], "/slack/events", app)

# Initializing web API client
slack_web_client = WebClient(token=os.environ['CSHESS_SLACK_BOT_TOKEN'])

if __name__ == "__main__":
    app.run(port=3000)