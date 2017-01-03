#!/usr/bin/python

import redis

expiration_default = 600

msg_t_action = "{}:\n*Key: {}\n*Value: {}"
class MyRedis:

    my_slack_client = None
    r = None

    def __init__(self, host, port, slack_client=None):
        self.r = redis.StrictRedis(host=host, port=port, db=0)
        if slack_client:
            self.my_slack_client = slack_client

    def setex(self, key, value, expiration=expiration_default):
        self.r.setex(key, expiration, value)
        if self.my_slack_client:
            msg = msg_t_action.format('SETEX', key, value)
            msg += '\n*Expiration: {}'.format(expiration)
            self.my_slack_client.send_message_log(msg=msg)
        pass

    def get(self, key):
        value = None
        value = self.r.get(key)
        if self.my_slack_client:
            msg = msg_t_action.format('GET', key, value)
            self.my_slack_client.send_message_log(msg=msg)
        return value


    def delete(self, key):
        value = self.get(key)
        self.r.delete(key)
        if self.my_slack_client:
            msg = msg_t_action.format('DELETE', key, value)
            self.my_slack_client.send_message_log(msg=msg)
        pass

    def keys(self, pattern):
        values = None
        values = self.r.keys(pattern)
        return values
