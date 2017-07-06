#!/usr/bin/python

from slackclient import SlackClient

class MySlackClient:

    token = None
    sc = None
    default_ch = None

    def __init__(self, token, default_ch):
        self.token = token
        self.sc = SlackClient(slack_token)
        self.default_ch = default_ch

    def send_message_log(self, msg):
        self.sc.api_call(
          "chat.postMessage",
          channel=self.default_ch,
          text=msg
        )
