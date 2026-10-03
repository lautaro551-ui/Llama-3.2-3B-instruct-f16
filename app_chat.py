#!/usr/bin/env python3
"""
Chat Local con Llama.cpp - Versión con llama-cpp-python
Sin dependencias externas, usa directamente llama-cpp-python
"""

import os
import json
from llama_cpp import Llama

class SimpleChat:
    def __init__(self):
        self.model_path = os.environ.get("MODEL_PATH", "models/Llama-3.2-3B-Instruct-f16(1).gguf")
        self.history_file = "chat.json"
        self.max_history = 2
        self.conversation = []
        self._load_history()
        self._load_model()
    
    def _load_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.conversation = data.get("messages", [])
        except Exception as e:
            self.conversation = []
    
    def _load_model(self):
        """Cargar modelo con llama-cpp-python"""
        try:
            print(f"Cargando modelo: {self.model_path}")
            self.model = Llama(
                model_path=self.model_path,
                n_ctx=2048,
                n_threads=8,
                n_gpu_layers=0  # Usar CPU
            )
            print("✅ Modelo cargado correctamente")
        except Exception as e:
            print(f"Error cargando modelo: {e}")
            self.model = None
    
    def _build_prompt(self, user_message: str) -> str:
        history_text = ""
        if len(self.conversation) > 0:
            history_text = "\n\nHistorial (últimas 2):\n"
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
    
    def query_model(self, prompt: str) -> str:
        """Consultar modelo con llama-cpp-python"""
        try:
            if self.model is None:
                return "Error: modelo no cargado"
            
            response = self.model(
                prompt=prompt,
                max_tokens=150,
                temperature=0.7,
                stop=["\n\n", "\nUsuario:"]
            )
            
            output = response.get("choices", [{}])[0].get("text", "").strip()
            
            # Limpiar prompt si está incluido
            if prompt in output:
                output = output.replace(prompt, "").strip()
            
            return output
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def ask(self, question: str) -> str:
        self.conversation.append({"role": "user", "content": question})
        
        prompt = self._build_prompt(question)
        response = self.query_model(prompt)
        
        self.conversation.append({"role": "assistant", "content": response})
        self._save_history()
        
        return response
    
    def _save_history(self):
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump({"messages": self.conversation}, f, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando: {e}")
    
    def clear_history(self):
        self.conversation = []
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
        print("Historial limpiado.")

def main():
    print("✨ ¡Bienvenido a tu Chat Local con llama-cpp-python!")
    print("Sin dependencias externas\n")
    
    chat = SimpleChat()
    
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
