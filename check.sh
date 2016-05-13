#!/bin/bash

python run.py &
echo $! > pid.pid
