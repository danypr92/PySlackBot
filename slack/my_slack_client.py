#!/usr/bin/python

import os
from slackclient import SlackClient

class MySlackClient:

    sc = None
    default_ch = None

    def __init__(self, slack_token, default_ch):
        self.sc = SlackClient(slack_token)
        self.default_ch = default_ch

    def send_message_log(self, msg):
        self.sc.api_call(
          "chat.postMessage",
          channel=self.default_ch,
          text=msg
        )