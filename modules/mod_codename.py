# File: mod_codename.py
# Date: 2018-08-03
# Author: Matt Weidner <matt.weidner@gmail.com>
# Description: Slackbot cyber op codename generator
#
import json
import time

def get_commands():
    return [{"command": "codename", "callback": say_codename},]

def say_codename(args):
    print("[mod_codename()]", args)

    return "Codename not implemented."


def init():
    print("[DEBUG] [mod_codename.py] init() Initializing mod_codename...")
    pass

def main():
    pass

if __name__ == "modules.mod_codename":
    init()

if __name__ == "__main__":
    main()
