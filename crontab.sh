#!/bin/bash

echo "* * * * * /usr/bin/python3 $PWD/timemachine.py --config=$PWD/config.dat --storePath=$PWD/ >> $PWD/timemachine.log 2>&1" | crontab