# File: mod_hello.py
# Date: 2018-08-03
# Author: Matt Weidner <matt.weidner@gmail.com>
# Description: Snozzberry module
#
import json
import random
import time

responses = [ "Squirrel’s don’t eat snozzberries, you moron. Unless they're on crack.",
              "All I know about snozzberries is they taste like snozzberries.",
              "So THAT's what they're calling the new Adobe Flash exploit.",
              "Back at you!",
              "Have you tasted a snozzberry? Nasty...",
              "Do you know where I can get some?",
              "Who's your supplier? Let me guess... @miller1371?",
              "Who's your supplier? Let me guess... @Ryan Hopkins?",
              "One does not simply TASTE a snozzberry.",
              "You can't eat just one!"

        ]

def get_commands():
    return [{"command": "snozzberry", "callback": say_snozz},
            {"command": "snozzberries", "callback": say_snozz},]

def say_snozz(args):
    return random.choice(responses)


def init():
    print("[DEBUG] [mod_hello.py] init()")
    pass

def main():
    pass

if __name__ == "modules.mod_hello":
    init()

if __name__ == "__main__":
    main()
