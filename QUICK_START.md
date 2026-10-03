# 🚀 Inicio Rápido - Chat Local con Llama.cpp

## Pasos

### 1. Iniciar el server (en una terminal)
```bash
./start_server.sh
```

### 2. Iniciar el chat (en otra terminal)
```bash
python3 app_chat_server.py
```

## Características

- ✅ Sin errores de timeout
- ✅ Salida limpia: solo "👤 Usuario:" y "🤖 Computadora:"
- ✅ Historial de últimas 2 preguntas
- ✅ Respuestas en español

## Comandos

| Comando | Descripción |
|---------|-------------|
| `/clear` | Limpiar historial |
| `/quit` | Salir |

## Cambiar de modelo

Para usar un modelo más avanzado:

1. Descarga un modelo GGUF de Hugging Face (ej: SmolLM2-1.7B, Mistral-7B)
2. Colócalo en `models/`
3. Inicia el server con el nuevo modelo:
```bash
MODEL_PATH="models/tu_modelo.gguf" ./start_server.sh
```
