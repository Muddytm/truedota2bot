#!/bin/bash

pid="pid.pid"
kill "$(<"$pid")"
python run.py &
echo $! > pid.pid
