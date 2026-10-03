#!/bin/bash
echo "🚀 Iniciando Llama Server..."
echo "Este server mantiene llama-cli listo para responder sin demora"
echo ""

# Verificar si hay un server corriendo
if curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "✅ Server ya corriendo en http://localhost:8080"
    curl -s http://localhost:8080/health | python3 -m json.tool
else
    echo "⚠️  Iniciando server en http://localhost:8080..."
    python3 start_llama_server.py &
    SERVER_PID=$!
    echo "✅ Server iniciado (PID: $SERVER_PID)"
    echo ""
    echo "Esperando a que esté listo..."
    sleep 2
    
    # Verificar que esté listo
    if curl -s http://localhost:8080/health > /dev/null 2>&1; then
        echo "✅ Server listo!"
        curl -s http://localhost:8080/health | python3 -m json.tool
        echo ""
        echo "💡 Ahora ejecuta: python3 app_chat_server.py"
    else
        echo "❌ Error iniciando server"
    fi
fi
