#!/usr/bin/env python3
"""
Chat Local con Server - Sin errores de timeout
Usa llama.cpp server que mantiene el modelo cargado
"""

import os
import json
import requests
import time

class ServerChat:
    def __init__(self, server_url="http://localhost:8080"):
        self.server_url = server_url
        self.history_file = "chat_server.json"
        self.max_history = 2
        self.conversation = []
        self._load_history()
    
    def _load_history(self):
        """Cargar historial"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.conversation = data.get("messages", [])
        except:
            self.conversation = []
    
    def _save_history(self):
        """Guardar historial"""
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump({"messages": self.conversation}, f, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando: {e}")
    
    def _build_prompt(self, user_message: str) -> str:
        """Construir prompt con historial"""
        history_text = ""
        if len(self.conversation) > 0:
            history_text = "\n\nConversación reciente (últimas 2 preguntas):\n"
            for msg in self.conversation[-self.max_history:]:
                role = msg.get("role", "")
                content = msg.get("content", "")
                if role == "user":
                    history_text += f"Usuario: {content}\n"
                elif role == "assistant":
                    history_text += f"Computadora: {content}\n"
        
        prompt = f"""Eres un asistente de IA amable y humanizado.
Responde en español, de forma natural y breve (máximo 3-4 líneas).

{history_text}

Usuario: {user_message}

Computadora:"""
        
        return prompt
    
    def query_server(self, prompt: str) -> str:
        """Consultar server de llama.cpp"""
        try:
            response = requests.post(
                f"{self.server_url}/completion",
                json={
                    "prompt": prompt,
                    "n_predict": 200,
                    "temperature": 0.7,
                    "stop": ["\n\n", "\nUsuario:"]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return data.get("content", "").strip()
            else:
                return "Error al conectar con el server."
                
        except Exception as e:
            return f"Error: {str(e)}"
    
    def ask(self, question: str) -> str:
        """Enviar pregunta al server"""
        self.conversation.append({"role": "user", "content": question})
        
        prompt = self._build_prompt(question)
        response = self.query_server(prompt)
        
        self.conversation.append({"role": "assistant", "content": response})
        self._save_history()
        
        return response
    
    def clear_history(self):
        """Limpiar historial"""
        self.conversation = []
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
        print("Historial limpiado.")

def main():
    """Función principal"""
    # Verificar si el server está disponible
    try:
        requests.get("http://localhost:8080/health", timeout=5)
        print("✅ Server de Llama.cpp conectado")
    except:
        print("⚠️  Server no encontrado en http://localhost:8080")
        print("Inicia primero con: ./start_server.sh")
        return
    
    print("✨ ¡Bienvenido a tu Chat con Server!")
    print("Modelo cargado permanentemente - sin tiempos de espera\n")
    
    chat = ServerChat()
    
    while True:
        try:
            user_input = input("👤 Usuario: ").strip()
            
            if not user_input:
                continue
            
            if user_input.startswith("/"):
                command = user_input[1:].lower().strip()
                
                if command in ["quit", "exit", "q"]:
                    print("\n👋 ¡Hasta luego!\n")
                    break
                elif command in ["clear", "c"]:
                    chat.clear_history()
                    print("\n✓ Historial limpiado\n")
                elif command in ["help", "h"]:
                    print("Comandos: /clear, /quit, /help")
                else:
                    print(f"Comando: /{command}")
                continue
            
            response = chat.ask(user_input)
            print(f"\n🤖 Computadora: {response}\n")
            
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!\n")
            break
        except EOFError:
            print("\n\n👋 ¡Hasta luego!\n")
            break

if __name__ == "__main__":
    main()