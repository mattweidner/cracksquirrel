# File: mod_codename.py
# Date: 2018-08-03
# Author: Matt Weidner <matt.weidner@gmail.com>
# Description: Slackbot cyber op codename generator
#
import pathlib
import random

__ADJECTIVES = []
__NOUNS = []

def get_commands():
    return [{"command": "codename", "callback": say_codename},]

def say_codename(args):
    adj = random.choice(__ADJECTIVES)
    noun = random.choice(__NOUNS)
    return " ".join(["Your next cyber op will be known as OPERATION", adj.upper(), noun.upper()])

def init():
    global __ADJECTIVES, __NOUNS
    print("[DEBUG] [mod_codename.py] init()")
    adj_path = pathlib.Path("modules/codename/adjectives-clean.txt")
    noun_path = pathlib.Path("modules/codename/nouns-clean.txt")
    for line in adj_path.open():
        __ADJECTIVES.append(line.strip())
    for line in noun_path.open():
        __NOUNS.append(line.strip())

def main():
    init()
    say_codename({})
    pass

if __name__ == "modules.mod_codename":
    init()

if __name__ == "__main__":
    main()
