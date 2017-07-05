#!/usr/bin/python

def humanize_dict(input_dict):
    news_message = ""
    for par in input_dict:
        news_message += "\t*{key}*: {value}\n".format(key=par['key'], value=par['value'])
    return news_message

def humanize_list(input_list):
    removed_message = ""
    for key in input_list:
        removed_message += "\t*{key}*".format(key=key)
    return removed_message
