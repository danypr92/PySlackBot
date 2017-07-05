#!/usr/bin/python

import time
import sys
from multiprocessing import Pool

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
    redis_args = {}
    slack_args = {}
    for i, val in enumerate(args):
        if '-redis-h' in val:
            host = args[i+1]
            redis_args['host']= host
        if '-redis-p' in val:
            host = args[i+1]
            redis_args['port']= host
        if '-slack-ch' in val:
            slack_args['slack_ch'] = args[i+1]
        if '-slack-token' in val:
            slack_args['slack_token'] = args[i+1]

    if not redis_args:
        print("Need redis args. Ex:\npython main.py -redis-h 127.0.0.1 -redis-p 6379 [...]")
        exit(0)
    if not slack_args:
        print("Need slack args. Ex:\npython main.py [...] -slack-ch #chanelTest")
        exit(0)
    return redis_args, slack_args

def main():


    redis_args, slack_args = parse_args()

    host = redis_args.get('host')
    port = redis_args.get('port')
    slack_ch = slack_args.get('slack_ch')
    slack_token = slack_args.get('slack_token')
    my_slack_client = MySlackClient(slack_token, slack_ch)
    my_redis = MyRedis(host=host, port=port)
    # while():
    print('Run Slacklog Bot!')
    runSpy(my_redis, my_slack_client)
    # my_redis.setex('foo2', 'boo')
    #
    # my_redis.get('foo2')
    #
    # my_redis.delete('foo2')
    # p = Pool(5)
    # p.map(run,['T-A','T-B','T-C','T-D'])

if __name__ == '__main__':
    main()
