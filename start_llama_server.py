#!/usr/bin/env python3
"""Server simple para mantener llama-cli listo usando pipes"""

import os
import sys
import subprocess
import threading
import time
import json
import tempfile
from http.server import HTTPServer, BaseHTTPRequestHandler

MODEL_PATH = os.environ.get("MODEL_PATH", "models/SmolLM2.Q4_K_M.gguf")
PORT = int(os.environ.get("SERVER_PORT", 8080))

class LlamaHandler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Silenciar logs
    
    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "model": MODEL_PATH}).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_POST(self):
        if self.path == '/completion':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            
            try:
                data = json.loads(body)
                prompt = data.get('prompt', '')
                n_predict = data.get('n_predict', 150)
                temperature = data.get('temperature', 0.7)
                
                # Crear un archivo temporal con el prompt
                with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
                    f.write(prompt)
                    temp_file = f.name
                
                try:
                    # Ejecutar llama-cli con el archivo
                    process = subprocess.Popen(
                        ['llama-cli',
                         '-m', MODEL_PATH,
                         '-n', str(n_predict),
                         '--temp', str(temperature),
                         '-f', temp_file],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True
                    )
                    
                    # Enviar una línea vacía para salir del modo interactivo
                    stdout, stderr = process.communicate(input='\n', timeout=60)
                    
                    output = stdout + stderr
                    
                    # Limpiar la salida de llama-cli
                    # Eliminar los comandos disponibles y la UI
                    if 'available commands:' in output:
                        output = output.split('available commands:')[0].strip()
                    if 'build      :' in output:
                        output = output.split('build      :')[0].strip()
                    if prompt in output:
                        output = output.replace(prompt, '').strip()
                    
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"content": output}).encode())
                    
                finally:
                    os.unlink(temp_file)
                    
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            self.send_response(404)
            self.end_headers()

def main():
    print(f"🚀 Iniciando Llama Server en puerto {PORT}")
    print(f"📄 Modelo: {MODEL_PATH}")
    print("💡 Este servidor mantiene llama-cli listo para responder")
    print()
    
    server = HTTPServer(('0.0.0.0', PORT), LlamaHandler)
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n👋 Server detenido")
        server.shutdown()

if __name__ == "__main__":
    main()