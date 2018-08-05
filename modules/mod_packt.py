# File: mod_packt.py
# Date: 2018-08-03
# Author: Matt Weidner <matt.weidner@gmail.com>
# Description: Discover and announce the Packt book of the day as advertised
#              at https://www.packtpub.com/packt/offers/free-learning
#
import json
import time

def get_commands():
    return [{"command": "packt", "callback": say_packt_book},
            {"command": "packtbook", "callback": say_packt_book}]

def say_packt_book(args):
    print("[mod_packt()]", args)
    print("")
    return "The packt and packtbook commands are not implemented."

    #
    # Returning a json-formatted string will be sent modified to Slack
    # via the active websocket.
    #
    #return json.dumps({"id": int(time.time()*100), "type": "message", "channel": args["channel"], "text": "You talking to me?\nStay in Slack and don't do school!\nMMMM'kay Bye!"})
    #
    # If a module returns a non-json string, the string will be inserted,
    # unmodified into a json frame and sent to the slack channel on which
    # the bot mention was detected.
    #
    #return "Aloha!"


def init():
    print("[DEBUG] [mod_packt.py] init()")
    pass

def main():
    pass

if __name__ == "modules.mod_packt":
    init()

if __name__ == "__main__":
    main()
