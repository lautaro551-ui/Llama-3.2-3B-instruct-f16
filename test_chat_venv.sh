#!/bin/bash
cd /home/Lautaro/Downloads/llama.cpp
bash -c 'source venv/bin/activate && timeout 60 python3 app_chat.py' 2>&1 | head -30
