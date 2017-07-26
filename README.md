# PySlackBot
Test de bot para Slack que avisa del estado de Redis.

------------

__Python 2.7.12__

La libreria SlackClient no funciona para Python3



@@ Old and Deprecated

# slackAPI
My utils for SlackAPI

requirements.txt --> Python dependencies to install with pip

slack.example.ini --> Configuration of slack API. Create a new file named slack.ini with your own values of:

  * token --> Get token from: https://api.slack.com/custom-integrations/legacy-tokens

  * user --> Can get form mpim.history method. https://api.slack.com/methods/mpim.history

  * chat --> Can get from mpim.list method. https://api.slack.com/methods/mpim.list


--------------------------------
**chatUtils**

chatUtils/del-chat-msgs.py --> Remove last messages of user in select chat in last 1000 messages.
