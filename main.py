#!/usr/bin/python

import time, os, configparser
import sys
from multiprocessing import Pool
from configparser import ConfigParser

from my_slack.my_slack_client import MySlackClient
from my_redis.my_redis import MyRedis
import utils.util_tools

def run(name):
    print("Start {}!".format(name))
    for i in range(30):
        time.sleep(5)
        msg = '{} said Hola Mundo! at {}'.format(name, time.ctime())
        key = 'HM_key_{}'.format(i)
        my_redis.setex(key, msg)

def runSpy(my_redis, my_slack_client):
    old_keys = []
    changes = {}
    while True:
        keys = my_redis.keys('*')
        new_keys = [{'key': key, 'value': my_redis.get(key) }
                    for key in keys if key not in old_keys]
        removed_keys = [key for key in old_keys if key not in keys]
        old_keys = keys

        news_message = utils.util_tools.humanize_dict(new_keys)
        removed_message = utils.util_tools.humanize_list(removed_keys)

        if news_message: my_slack_client.send_message_log("_*News*_:\n\n" + news_message)
        if removed_message: my_slack_client.send_message_log("_*Removed*_:\n\n" + removed_message)
        time.sleep(1)

def parse_args():
    args = sys.argv
    for val in args:
        if '-channel-info' == str(val):
            return "chl_info"
        if '-spy' is val:
            return 'spy'
        if '-send-msg' is val:
            return 'send_msg'



def get_configs():
    slack_conf_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'config/slack.ini'
        )
    print('Get Slack configuration from ' + slack_conf_path)
    configParser = ConfigParser()
    configParser.read(slack_conf_path)
    slack = {}
    slack['token'] = configParser.get('DEFAULT', 'token')
    try:
        slack['chat'] = configParser.get('DELETE_MESSAGES', 'chat')
        slack['user'] = configParser.get('DELETE_MESSAGES', 'user')
    except: True

    redis_conf_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'config/redis.ini'
        )
    print('Get Redis configuration from ' + redis_conf_path)
    configParser = ConfigParser()
    configParser.read(redis_conf_path)
    redis = {}
    redis['host'] = configParser.get('DEFAULT', 'host')
    redis['port'] = configParser.get('DEFAULT', 'port')

    return redis, slack

def main():

    redis_args, slack_args = get_configs()
    action = parse_args()

    my_slack_client = MySlackClient( slack_args['token'], slack_args['chat'] )
    my_redis = MyRedis(host=redis_args['host'], port=redis_args['port'])
    my_slack_client.send_message_log("_*News*_:\n\n")
    print(my_slack_client.get_channels_list())
    # runSpy(my_redis, my_slack_client)

if __name__ == '__main__':
    main()
