#!/bin/bash
echo "🔍 Verificando Llama.cpp server..."
echo ""

# Verificar si el server está corriendo
if curl -s http://localhost:8080/health > /dev/null 2>&1; then
    echo "✅ Server CORRIENDO en http://localhost:8080"
    
    # Verificar modelo cargado
    echo ""
    echo "ℹ️  Verificando modelo..."
    curl -s http://localhost:8080/health | grep -o '"model":"[^"]*"' || echo "Modelo cargado: unknown"
else
    echo "❌ Server NO encontrado"
    echo ""
    echo "Inicia con: ./start_server.sh"
    echo ""
    echo "O ejecuta directamente el server manualmente:"
    echo "./llama.cpp/server -m models/SmolLM2.Q4_K_M.gguf --port 8080"
fi
