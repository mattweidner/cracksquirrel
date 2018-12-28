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
    return json.dumps({"id": int(time.time()*100), "type": "message", "channel": args["channel"], "text": "You talking to me?\nStay in Slack and don't do school!\nMMMM'kay Bye!", "attachments": [{"fallback": "test attachment", "color": "#2eb886","pretext": "Optional text that appears above the attachment block","author_name": "Bobby Tables","author_link": "http://flickr.com/bobby/","author_icon": "http://flickr.com/icons/bobby.jpg","title": "Slack API Documentation","title_link": "https://api.slack.com/", "image_url": "http://my-website.com/path/to/image.jpg","thumb_url": "http://example.com/path/to/thumb.png", "footer": "Slack API","footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png"}]})
    return json.dumps({"id": int(time.time()*100), "type": "message", "channel": args["channel"], "text": "You talking to me?\nStay in Slack and don't do school!\nMMMM'kay Bye!"})
    #
    # If a module returns a non-json string, the string will be inserted,
    # unmodified into a json frame and sent to the slack channel on which
    # the bot mention was detected.
    #
    #return "Aloha!"


def init():
    print("[DEBUG] [mod_hello.py] init()")
    pass

def main():
    print(say_hello({"channel": "ANNOUNCE"}))
    pass

if __name__ == "modules.mod_hello":
    init()

if __name__ == "__main__":
    main()
