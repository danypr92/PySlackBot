#!/usr/bin/python

from slackclient import SlackClient

class MySlackClient:

    token = None
    sc = None
    default_ch = None

    def __init__(self, token, default_ch):
        self.token = token
        self.sc = SlackClient(token)
        self.default_ch = default_ch

    def send_message_log(self, msg):
        self.sc.api_call(
          "chat.postMessage",
          channel=self.default_ch,
          text=msg
          )


    def get_channels_list(self):
        formatted_channels = []
        channels = self.sc.api_call('channels.list', exclude_archived=1)
        for channel in channels['channels']:
            new_channel = {
                'name': channel['name'],
                'id': channel['id'],
                'creator': channel['creator']
            }
            formatted_channels.append(new_channel)
        return formatted_channels

    def retrieve_channel_messages(self, chat_id=None):
        if not chat_id: chat_id=self.default_ch
        print(self.sc.api_call(
            'mpim.history',
            channel=chat_id,
            count=1000
        ))

    def remove_chat_messages(self, user, chat_id):
        messages = retrieve_channel_messages(chat_id)
        for m in messages:
            if m['user'] == user:
                text = m['text']
                self.sc.api_call(
                    'chat.delete',
                    channel=chat_id,
                    ts=m['ts']
                )
                print('Deleted message: ' + text)
            else:
                print(r.text)
                exit

    def get_channel_info(self, channel_name):
        channels_list = self.get_channels_list()
        for channel in channels_list:
            if channel['name'] == channel_name: return channel
