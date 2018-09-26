# File: mod_hello.py
# Date: 2018-08-03
# Author: Matt Weidner <matt.weidner@gmail.com>
# Description: Slackbot hello world module. Responds with a text message upon
#              detecting a mention.
#
import requests
import time

def get_commands():
    return [{"command": "weather", "callback": say_weather},]

def say_weather(args):
    location = "66801"
    print("[mod_wttr()] args", args)
    print(len(args["text"].split(" ")))
    ua = {"User-agent": "python-requests"}
    # http://wttr.in/66801?QT0
    r = requests.get("http://wttr.in/"+location+"?QT0", headers=ua)
    #
    # If a module returns a non-json string, the string will be inserted,
    # unmodified into a json frame and sent to the slack channel on which
    # the bot mention was detected.
    #
    r.encoding = None
    return r.text


def init():
    print("[DEBUG] [mod_wttr.py] init() Initializing mod_wttr...")
    pass

def main():
    print(say_weather({'type': 'message', 'user': 'U3GM4R9RD', 'text': '<@U9QSQEH0S> weather', 'client_msg_id': '741b5360-9e5c-4310-bee5-28bff51f552d', 'team': 'T3FA95B5F', 'channel': 'D9QSXR4D8', 'event_ts': '1536088569.000100', 'ts': '1536088569.000100'}))
    print(say_weather({'type': 'message', 'user': 'U3GM4R9RD', 'text': '<@U9QSQEH0S> weather boston', 'client_msg_id': '741b5360-9e5c-4310-bee5-28bff51f552d', 'team': 'T3FA95B5F', 'channel': 'D9QSXR4D8', 'event_ts': '1536088569.000100', 'ts': '1536088569.000100'}))
    pass

if __name__ == "modules.mod_wttr":
    init()

if __name__ == "__main__":
    main()
