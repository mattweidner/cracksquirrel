# File: mod_hello.py
# Date: 2018-08-03
# Author: Matt Weidner <matt.weidner@gmail.com>
# Description: Slackbot hello world module. Responds with a text message upon
#              detecting a mention.
#
import json
import time

def get_commands():
    return [{"command": "hello", "callback": say_hello},]

def say_hello(args):
    print("[mod_hello()]", args)
    #
    # Returning a json-formatted string will be sent modified to Slack
    # via the active websocket.
    #
    return json.dumps({"id": int(time.time()*100), "type": "message", "channel": args["channel"], "text": "You talking to me?\nStay in nuts and don't do school!\nMMMM'kay Bye!"})
    #
    # If a module returns a non-json string, the string will be inserted,
    # unmodified into a json frame and sent to the slack channel on which
    # the bot mention was detected.
    #
    #return "Aloha!"


def init():
    print("[DEBUG] [mod_hello.py] init() Initializing mod_hello...")
    pass

def main():
    pass

if __name__ == "modules.mod_hello":
    init()

if __name__ == "__main__":
    main()
