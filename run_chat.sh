#!/bin/bash
cd /home/Lautaro/Downloads/llama.cpp
bash -c 'source venv/bin/activate && timeout 120 python3 app_chat.py' 2>&1
