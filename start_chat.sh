#!/bin/bash

echo "🚀 Iniciando Chat Local con Llama.cpp..."

# Verificar si llama-cli está disponible
if command -v llama-cli &> /dev/null; then
    echo "✅ llama-cli encontrado"
elif [ -f "llama.cpp/main" ]; then
    echo "⚠️  Usando llama.cpp/main directamente"
    export LLAMA_CLI_CMD="./llama.cpp/main"
else
    echo "⚠️  llama-cli no encontrado en PATH"
    echo "   Compila llama.cpp o instálalo:"
    echo "   cd llama.cpp && make -j"
fi

# Verificar modelo
if [ -f "models/SmolLM2.Q4_K_M.gguf" ]; then
    echo "✅ Modelo SmolLM2.Q4_K_M.gguf encontrado"
elif [ -f "models/*.gguf" ]; then
    echo "✅ Modelo encontrado:"
    ls -la models/*.gguf | head -1
else
    echo "⚠️  No se encontró ningún modelo GGUF en models/"
    echo "   Descarga un modelo compatible (GGUF) y colócalo en models/"
fi

# Verificar archivo de docs
if [ -f "uploaded_docs.txt" ]; then
    echo "📄 Documentos cargados: uploaded_docs.txt ($(wc -c < uploaded_docs.txt) bytes)"
else
    echo "📝 No hay documentos cargados (opcional)"
    echo "   Crea 'uploaded_docs.txt' para agregar contexto"
fi

echo ""
echo "================================"
echo "🤖 Inicia el chat con: python3 app_chat.py"
echo "================================"
echo ""
