#!/bin/bash
echo "start msg_receiver_app"
cd /home/rabbit/flurry/src/
exec python rabbit_receiver.py
