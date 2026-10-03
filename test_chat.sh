#!/bin/bash
echo "Testing chat..."
echo "hola, ¿cómo estás?" | python3 app_chat_server.py &
#sleep 2
#curl -s http://localhost:8080/completion -X POST -H 'Content-Type: application/json' -d '{"prompt": "hola, ¿cómo estás?", "n_predict": 50}'
