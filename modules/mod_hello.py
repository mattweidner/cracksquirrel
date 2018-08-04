# File: mod_hello.py
# Date: 2018-08-03
# Author: Matt Weidner <matt.weidner@gmail.com>
# Description: Slackbot hello world module. Responds with a text message upon
#              detecting a mention.
#


def get_commands():
    return [{"command": "hello", "callback": say_hello},]

def say_hello(args):
    return "Aloha!"

def init():
    print("Initializing mod_hello...")
    pass

def main():
    pass

if __name__ == "modules.mod_hello":
    init()

if __name__ == "__main__":
    main()
