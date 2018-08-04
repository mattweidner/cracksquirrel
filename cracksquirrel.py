# File: secretsquirrel2.py
# Date: 2018-08-03
# Author: Matt Weidner <matt.weidner@gmail.com>
# Description: Secret Squirrel Slackbot
#
import asyncio
import importlib
import json
import pathlib
import slack

commands = []

def load_modules():
    modules_path = pathlib.Path("modules/")
    for module in modules_path.iterdir():
        if module.is_dir():
            continue
        if str(module.name).startswith("mod_"):
            module_name = module.name
            module_name = module_name.split(".")[0]
            print("Loading module", "modules."+module_name)
            m = importlib.import_module("modules."+module_name, "modules.subpkg")
            if not m is None:
                cmds = m.get_commands()
                #print("[DEBUG]", cmds)
                if not cmds is None:
                    commands.append({"module": m, "command_list": cmds})
        else:
            print("Skipping", module)
    importlib.invalidate_caches()

def test_modules():
    for m in commands:
        #print("[DEBUG]", m)
        for c in m["command_list"]:
            #print("[DEBUG]", c)
            r = c["callback"]([c["command"]])
            print("[DEBUG] test_modules()    [+] module says", r)

def bot_callback(message):
    try:
        m = json.loads(message)
    except Exception as e:
        print("[!] bot_callback() Unable to unmarshall json", e)
        print("[!]     ", message)
        return
    if m["type"] == "message":
        print("T:", m["team"], "C:", m["channel"], "U:", m["user"])
        print(m["text"])
    else:
        print(m)

def test_slack():
    if slack.connect(bot_callback) == False:
        print("[!] test_slack() Error connecting to Slack")

def main():
#   load_modules()
#   test_modules()
#   test_slack()
    if slack.connect(bot_callback) == False:
        print("[!] main() Error connecting to Slack")
    print("Terminated.")

if __name__ == "__main__":
    main()
