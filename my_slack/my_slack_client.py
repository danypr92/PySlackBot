#!/usr/bin/python
import sys, time
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

    def del_parties_msgs(self, user_id, parties_except=None):
        parties = self.get_parties_list()
        for party in parties:
            if party['id'] not in parties_except:
                messages = self.retrieve_channel_messages(party['id'])
                for m in messages:
                    if m['user'] == user_id:
                        self.remove_chat_message(user_id=user_id, chat_id=party['id'], ts=m['ts'])

    def get_parties_list(self):
        formatted_channels = []
        parties = self.sc.api_call('mpim.list', exclude_archived=1)
        print(parties)
        for party in parties['groups']:
            new_channel = {
                'name': party['name'],
                'id': party['id'],
                'creator': party['creator']
            }
            formatted_channels.append(new_channel)
        return formatted_channels

    def retrieve_channel_messages(self, chat_id=None):
        if not chat_id: chat_id=self.default_ch
        messages = self.sc.api_call(
            'mpim.history',
            channel=chat_id,
            count=1000
        )
        return messages['messages']

    def del_private_chats_msgs(self, user_id, chats_except=None):
        chats = self.get_private_chats_list()
        for chat in chats:
            print(chat)
            if chat['id'] not in chats_except:
                messages = self.retrieve_chat_messages(chat['id'])
                for m in messages:
                    if m['user'] == user_id:
                        print("Removing: " + m['text'])
                        self.remove_chat_message(user_id=user_id, chat_id=chat['id'], ts=m['ts'])
                        time.sleep(1)

    def retrieve_chat_messages(self, chat_id):
        messages = self.sc.api_call(
            'im.history',
            channel=chat_id,
            count=1000
        )
        return messages['messages']


    def get_private_chats_list(self):
        chats = self.sc.api_call(
          "im.list"
          )
        formatted_chats = []
        for chat in chats['ims']:
            if chat['user'] not in ['U0UFSEW80', 'U0UFNRLUQ']:
                formatted_chats.append({
                    'id': chat['id'],
                    'user': chat['user']
                })
        return formatted_chats

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
        print(formatted_channels)
        return formatted_channels

    def remove_chat_message(self, chat_id, user_id, ts):
        self.sc.api_call(
            'chat.delete',
            channel=chat_id,
            ts=ts
        )

    def get_channel_info(self, channel_name):
        channels_list = self.get_channels_list()
        for channel in channels_list:
            if channel['name'] == channel_name: return channel
