# 🤖 Capacidades del Sistema RAG Local

## 📋 Resumen

Este sistema es un **RAG (Retrieval-Augmented Generation) local** que te permite:

1. **Cargar documentos** (PDF, texto, Word)
2. **Preguntarle sobre el contenido** usando tu modelo SmolLM2
3. **Responder en base al texto leído**

## ✨ Capacidades Principales

### 1. Carga de Archivos

**Soportados:**
- 📄 PDF (extrae todo el texto)
- 📝 TXT (archivos de texto plano)
- 📄 DOCX (documentos de Word)

**Qué hace con cada archivo:**
1. Extrae el texto del archivo
2. Crea un índice de palabras clave
3. Guarda el contenido original en la base de datos

### 2. Búsqueda Inteligente

**Cómo funciona:**
- Divide el texto en palabras clave
- Busca coincidencias con tu pregunta
- Recupera los fragmentos más relevantes
- Usa tu modelo SmolLM2 para generar una respuesta coherente

**Ejemplo:**
```
Pregunta: "¿Qué dice el documento sobre IA?"
→ Busca palabras como "IA", "inteligencia", "artificial"
→ Recupera párrafos relevantes
→ Usa SmolLM2 para sintetizar la respuesta
```

### 3. Generación con LLM Local

**Modelo:** SmolLM2.Q4_K_M (4-bit quantizado)

**Características:**
- 100% local (no usa internet)
- Sin costos por uso
- Privacidad total (tus datos nunca salen de tu máquina)
- Respuestas rápidas (dependiendo de tu CPU)

## 🎯 Casos de Uso

### Caso 1: Análisis de Documentos Técnicos

```
Carga: Manual de usuario, especificaciones técnicas
Pregunta: "¿Cómo configuro X?"
Respuesta: Extracción de instrucciones relevantes
```

### Caso 2: Análisis de Contratos

```
Carga: Contratos, términos y condiciones
Pregunta: "¿Qué dice sobre la privacidad de datos?"
Respuesta: Puntos clave del contrato relacionados
```

### Caso 3: Investigación de Textos

```
Carga: Artículos, informes, notas
Pregunta: "¿Cuáles son los temas principales?"
Respuesta: Resumen basado en el contenido leído
```

### Caso 4: Chat con Tus Archivos

```
Carga: Varios documentos relacionados
Pregunta: "Conecta las ideas de estos documentos"
Respuesta: Síntesis entre múltiples fuentes
```

## 🛠️ Características Técnicas

### Backend
- **Framework:** FastAPI (Python)
- **Base de datos:** SQLite (ligera, sin servidor)
- **LLM:** llama-cli con SmolLM2

### Interfaz
- **Frontend:** HTML/CSS/JS vanilla
- **Estilo:** Minimalista técnico (azul medianoche/negro)
- **Responsive:** Funciona en móvil y escritorio

### Optimizaciones
- **Sin OCR:** No procesa imágenes (ahorra RAM)
- **Keyword matching:** Más rápido que embeddings pesados
- **Chunking:** Divide texto en fragmentos manejables

## ⚡ Limitaciones Actuales

1. **No procesa imágenes** (solo texto extraído de PDFs)
2. **Requiere modelo local** (SmolLM2 o similar)
3. **Memoria:** SmolLM2 usa ~2-4GB RAM
4. **Velocidad:** Depende de tu CPU

## 📈 Para Mejorar

Futuras versiones podrían incluir:
- ✅ OCR para procesar imágenes
- ✅ Embeddings semánticos más precisos
- ✅ Chat histórico y conversacional
- ✅ Exportación de resultados

## 🚀 ¿Cómo Usarlo?

1. Iniciar servidor: `source venv_rag/bin/activate.fish && python3 main_cli.py`
2. Abrir: http://localhost:8000
3. Subir archivos PDF/TXT/DOCX
4. Preguntar sobre el contenido
5. Recibir respuestas basadas en tus documentos

## 🔐 Privacidad

- TUS datos están en TU computadora
- Nada se sube a la nube
- Todo procesado localmente
- Sin tracking ni cookies
