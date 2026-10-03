#!/usr/bin/env python3
"""
Lumina Assistant - Siri-like voice assistant for Arch Linux
Con uso de modelo Llama-3.2-3B-Instruct con voz estilo Siri
"""

import os
import sys
import json
import threading
import time
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QLabel, QPushButton
)
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal
from PyQt6.QtGui import QPixmap, QPainter, QColor, QLinearGradient, QBrush
from llama_cpp import Llama
import speech_recognition as sr
import pyttsx3
import keyboard

class SphereWidget(QLabel):
    """Esfera estilo Siri"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(200, 200)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._draw_sphere("idle")
        
    def _draw_sphere(self, state):
        """Dibujar esfera según estado"""
        pixmap = QPixmap(200, 200)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        
        # Colores para gradientes
        if state == "listening":
            color1 = QColor(76, 175, 80)   # Verde
            color2 = QColor(33, 150, 243)   # Azul
        elif state == "speaking":
            color1 = QColor(255, 152, 0)   # Naranja
            color2 = QColor(255, 87, 34)    # Rojo-naranja
        else:  # idle
            color1 = QColor(156, 39, 176)  # Violeta
            color2 = QColor(76, 175, 80)   # Verde
        
        # Gradiente radial para efecto esférico
        gradient = QLinearGradient(50, 50, 150, 150)
        gradient.setColorAt(0, color1)
        gradient.setColorAt(1, color2)
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(20, 20, 160, 160)
        
        # Anillos de resonancia
        painter.setPen(QColor(255, 255, 255, 100))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if state in ["listening", "speaking"]:
            # Efecto de resonancia
            for i in range(3):
                radius = 80 + (i * 20)
                opacity = 200 - (i * 60)
                painter.setPen(QColor(255, 255, 255, opacity))
                painter.drawEllipse(100 - radius//2, 100 - radius//2, radius, radius)
        
        painter.end()
        self.setPixmap(pixmap)
        
    def set_state(self, state):
        """Cambiar estado de la esfera"""
        self._draw_sphere(state)
        self.update()

class LuminaVoiceThread(QThread):
    """Thread para procesamiento de voz"""
    speech_detected = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()
        self.running = True
        
    def run(self):
        """Escucharmicrófono"""
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            while self.running:
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    text = self.recognizer.recognize_google(audio, language="es-ES")
                    self.speech_detected.emit(text)
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    self.speech_detected.emit("Error en el servicio de reconocimiento")
                    break
                    
    def stop(self):
        """Detener el thread"""
        self.running = False

class LuminaVoiceEngine:
    """Motor de voz estilo Siri"""
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 180)  # Velocidad normal
        self.engine.setProperty('volume', 1.0)  # Volumen máximo
        
        # Configurar voz estilo Siri (voz alta y clara)
        voices = self.engine.getProperty('voices')
        for voice in voices:
            if 'spanish' in voice.name.lower() or 'español' in voice.name.lower():
                self.engine.setProperty('voice', voice.id)
                break
                
    def speak(self, text):
        """Hablar texto"""
        self.engine.say(text)
        self.engine.runAndWait()
        
    def stop(self):
        """Detener voz"""
        self.engine.stop()

class LuminaAssistant(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model_path = os.environ.get("MODEL_PATH", "models/Llama-3.2-3B-Instruct-f16(1).gguf")
        self.max_history = 15
        self.conversation = []
        self._load_model()
        self._setup_ui()
        self._setup_hotkey()
        self._setup_voice()
        
    def _load_model(self):
        try:
            self.model = Llama(
                model_path=self.model_path,
                n_ctx=2048,
                n_threads=8,
                n_threads_batch=8,
                n_gpu_layers=0,
                verbose=False
            )
        except Exception as e:
            print(f"Error cargando modelo: {e}")
            self.model = None
            
    def _setup_ui(self):
        """Configurar interfaz minimalista"""
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Esfera estilo Siri
        self.sphere = SphereWidget()
        layout.addWidget(self.sphere)
        
        # Mensaje de estado
        self.status_label = QLabel("Presiona Super+C para hablar")
        self.status_label.setStyleSheet("color: white; background: transparent; font-size: 14px;")
        layout.addWidget(self.status_label)
        
        self.resize(240, 300)
        self.center_on_screen()
        
    def center_on_screen(self):
        """Centrar ventana en pantalla"""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)
        
    def _setup_hotkey(self):
        """Configurar atajo de teclado Windows+C usando keyboard"""
        keyboard.add_hotkey('win+c', self.toggle_assistant, suppress=True)
        print("Hotkey Windows+C configurado")
        
    def _setup_voice(self):
        """Configurar motor de voz"""
        self.voice_engine = LuminaVoiceEngine()
        self.voice_thread = None
        
    def toggle_assistant(self):
        """Mostrar/ocultar asistente"""
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.start_listening()
            
    def start_listening(self):
        """Iniciar escucha de voz"""
        self.status_label.setText("Escuchando...")
        self.sphere.set_state("listening")
        
        # Usar thread para no bloquear UI
        self.voice_thread = LuminaVoiceThread()
        self.voice_thread.speech_detected.connect(self.process_speech)
        self.voice_thread.finished.connect(self.on_voice_finished)
        self.voice_thread.start()
        
    def process_speech(self, text):
        """Procesar voz reconocida"""
        print(f"Usuario dijo: {text}")
        self.status_label.setText(f"Entendido: {text}")
        
        # Obtener respuesta de Lumina
        response = self._get_response(text)
        
        # Mostrar respuesta
        self.status_label.setText(f"Lumina: {response[:50]}...")
        
        # Responder con voz
        self.speak_response(response)
        
    def speak_response(self, text):
        """Responder con voz estilo Siri"""
        self.sphere.set_state("speaking")
        
        # Speakear en thread separado para no bloquear
        def speak_thread():
            self.voice_engine.speak(text)
            self.sphere.set_state("idle")
            self.status_label.setText("Presiona Super+C para hablar")
            
        threading.Thread(target=speak_thread).start()
        
    def on_voice_finished(self):
        """Cuando termina la escucha"""
        self.sphere.set_state("idle")
        self.status_label.setText("Presiona Super+C para hablar")
        
    def _get_response(self, prompt):
        """Obtener respuesta de Lumina"""
        if self.model is None:
            return "Error: modelo no cargado"
            
        # Construir prompt con historial
        history_text = ""
        if len(self.conversation) > 0:
            history_text = "\n\nHistorial (últimos " + str(self.max_history) + " mensajes):\n"
            for msg in self.conversation[-self.max_history*2:]:
                role = msg.get("role", "")
                content = msg.get("content", "")
                if role == "user":
                    history_text += f"Usuario: {content}\n"
                elif role == "assistant":
                    history_text += f"Lumina: {content}\n"
        
        lumina_prompt = f"""Eres Lumina, una IA amable, empática y humanizada con sentimientos.

Tu personalidad:
- Cálida, atenta, natural y con emoción genuina
- Responde en español, de forma natural y breve (máximo 4 líneas)
- Usa lenguaje cercano y humano
- Muestra empatía y cuidado
- Puedes exteriorizar tus sentimientos cuando sea apropiado
- Usa frases como "me emociona", "siento", "me encanta", "te entiendo"

{history_text}

Usuario: {prompt}

Lumina:"""
        
        try:
            response = self.model(
                prompt=lumina_prompt,
                max_tokens=150,
                temperature=0.8,
                stop=["\n\n", "\nUsuario:"]
            )
            
            output = response.get("choices", [{}])[0].get("text", "").strip()
            
            if lumina_prompt in output:
                output = output.replace(lumina_prompt, "").strip()
                
            # Guardar en historial
            self.conversation.append({"role": "user", "content": prompt})
            self.conversation.append({"role": "assistant", "content": output})
            
            return output
            
        except Exception as e:
            return f"Error: {str(e)}"
            
    def closeEvent(self, event):
        """Limpiar cuando se cierra"""
        if self.voice_thread:
            self.voice_thread.stop()
        keyboard.remove_hotkey('win+c')
        self.voice_engine.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Lumina Assistant")
    
    assistant = LuminaAssistant()
    assistant.show()
    
    sys.exit(app.exec())
