#!/bin/bash
export SLACK_API_KEY=$(cat /home/orion/secretsquirrel2/apikey.txt)
while true
do
	DATE=$(date --iso-8601)
	touch ~/$DATE-log.txt
	/usr/bin/python3 /home/orion/secretsquirrel2/cracksquirrel.py >> ~/$DATE-log.txt
	sleep 3
done
