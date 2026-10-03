# 🚀 Inicio Rápido - Chat Local con Llama.cpp

## 3 Pasos para comenzar

### 1️⃣ Asegúrate de tener llama.cpp y un modelo

```bash
# Compilar llama.cpp (si no está compilado)
cd llama.cpp
make clean && make -j

# Verificar que llama-cli esté disponible
./llama-cli --help
```

### 2️⃣ Descarga un modelo GGUF

Descarga SmolLM2 o cualquier modelo compatible GGUF y colócalo en `models/`:

```bash
mkdir -p models
# Copia tu modelo aquí, ej: models/SmolLM2.Q4_K_M.gguf
```

### 3️⃣ Inicia el chat

```bash
python3 app_chat.py
```

## 📝 Ejemplo de uso

```
✨ ¡Bienvenido a tu Chat Local con Llama.cpp!

👤 Usuario: ¿Qué es la programación?
🤖 Asistente: La programación es el proceso de crear instrucciones...

👤 Usuario: ¿Puedes explicar Python?
🤖 Asistente: Python es un lenguaje de programación conocido por...

👤 Usuario: /clear
✓ Historial limpiado
```

## ⚡ Comandos rápidos

| Comando | Acción |
|---------|--------|
| `/help` | Mostrar ayuda |
| `/clear` | Limpiar historial |
| `/quit` | Salir |
| `/docs` | Ver documentos |

## 📚 Para más info

Ver `CHAT_README.md` para documentación completa.
