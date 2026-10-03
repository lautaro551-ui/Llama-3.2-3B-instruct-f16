#!/usr/bin/env python3
"""
AI Assistant Chat - Interfaz moderna con PyQt6
Diseño minimalista con degradado rosa-salmón y fondo azul oscuro
"""

import os
import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QFrame, QScrollArea,
    QMenu
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QPainter, QColor, QLinearGradient, QBrush, QIcon
from llama_cpp import Llama

class AvatarWidget(QLabel):
    """Widget de avatar circular con degradado rosa-salmón"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(50, 50)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._draw_gradient()
        
    def _draw_gradient(self):
        """Dibujar degradado rosa-salmón en el avatar"""
        pixmap = QPixmap(50, 50)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        gradient = QLinearGradient(0, 0, 50, 50)
        gradient.setColorAt(0, QColor(255, 0, 127))   # Rosa fucsia
        gradient.setColorAt(1, QColor(255, 106, 85))  # Salmón
        
        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(0, 0, 50, 50, 25, 25)
        
        # Dibujar icono de robot
        painter.setPen(QColor(255, 255, 255))
        painter.setFont(self.font())
        painter.drawText(10, 15, 30, 20, Qt.AlignmentFlag.AlignCenter, "🤖")
        
        painter.end()
        self.setPixmap(pixmap)

class MessageBubble(QFrame):
    """Burbuja de mensaje con estilo moderno"""
    def __init__(self, text, is_user=False, parent=None):
        super().__init__(parent)
        self.setObjectName("messageBubble")
        self.setStyleSheet("""
            QFrame {
                background-color: #232D3F;
                border-radius: 12px;
                padding: 12px 16px;
                color: #B0BAC9;
                font-size: 13px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.text_label = QLabel(text)
        self.text_label.setWordWrap(True)
        self.text_label.setStyleSheet("color: #B0BAC9; background: transparent;")
        self.text_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        
        layout.addWidget(self.text_label)
        
        if is_user:
            self.setStyleSheet("""
                QFrame {
                    background-color: #2C3649;
                    border-radius: 12px;
                    padding: 12px 16px;
                }
            """)

class AIChatApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.model_path = os.environ.get("MODEL_PATH", "models/Llama-3.2-3B-Instruct-f16(1).gguf")
        self.history_file = "chat_graphic.json"
        self.max_history = 2
        self.conversation = []
        self._load_history()
        self._load_model()
        self._setup_ui()
        
    def _load_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.conversation = data.get("messages", [])
        except Exception as e:
            self.conversation = []
            
    def _load_model(self):
        try:
            self.model = Llama(
                model_path=self.model_path,
                n_ctx=2048,
                n_threads=8,
                n_gpu_layers=0,
                verbose=False
            )
        except Exception as e:
            print(f"Error cargando modelo: {e}")
            self.model = None
            
    def _setup_ui(self):
        # Estilo global
        self.setStyleSheet("""
            QMainWindow {
                background-color: #181E2B;
            }
            QLineEdit {
                background-color: rgba(255, 0, 127, 0.1);
                border: 2px solid rgba(255, 0, 127, 0.3);
                border-radius: 12px;
                padding: 12px;
                color: #B0BAC9;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid rgba(255, 0, 127, 0.6);
                background-color: rgba(255, 0, 127, 0.15);
            }
            QPushButton {
                background-color: #232D3F;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                color: #FF6A55;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2C3649;
            }
            QPushButton:pressed {
                background-color: #181E2B;
            }
        """)
        
        # Configurar ventana principal
        self.setWindowTitle("AI Assistant Chat")
        self.setGeometry(100, 100, 900, 700)
        self.setMinimumSize(600, 500)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Header
        header = self._create_header()
        main_layout.addWidget(header)
        
        # Área de chat
        chat_container = QWidget()
        chat_layout = QVBoxLayout(chat_container)
        chat_layout.setContentsMargins(15, 15, 15, 15)
        
        self.chat_scroll_area = QScrollArea()
        self.chat_scroll_area.setWidgetResizable(True)
        self.chat_scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.chat_scroll_area.setStyleSheet("border: none; background: transparent;")
        
        self.chat_content = QWidget()
        self.chat_content_layout = QVBoxLayout(self.chat_content)
        self.chat_content_layout.setContentsMargins(0, 0, 0, 0)
        self.chat_content_layout.setSpacing(15)
        self.chat_content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        self.chat_scroll_area.setWidget(self.chat_content)
        chat_layout.addWidget(self.chat_scroll_area)
        main_layout.addWidget(chat_container)
        
        # Footer (Input)
        footer = self._create_footer()
        main_layout.addWidget(footer)
        
        # Cargar mensajes previos
        self._load_previous_messages()
        
    def _create_header(self):
        header = QFrame()
        header.setObjectName("header")
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, 
                    stop:0 #FF007F, stop:1 #FF6A55);
                min-height: 60px;
            }
        """)
        
        layout = QHBoxLayout(header)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(15)
        
        # Botón regresar
        back_btn = QPushButton("<")
        back_btn.setObjectName("backBtn")
        back_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                font-size: 20px;
                font-weight: bold;
                padding: 5px;
                min-width: 40px;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.2);
                border-radius: 5px;
            }
        """)
        back_btn.clicked.connect(self.close)
        layout.addWidget(back_btn)
        
        # Título
        title = QLabel("AI Assistant Chat")
        title.setStyleSheet("color: white; font-size: 18px; font-weight: bold; background: transparent;")
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Botón de menú
        menu_btn = QPushButton("☰")
        menu_btn.setObjectName("menuBtn")
        menu_btn.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: white;
                font-size: 20px;
                padding: 5px;
                min-width: 40px;
            }
            QPushButton:hover {
                background: rgba(255,255,255,0.2);
                border-radius: 5px;
            }
        """)
        
        menu = QMenu()
        menu.addAction("Limpiar chat", self._clear_chat)
        menu.addAction("Salir", self.close)
        menu_btn.setMenu(menu)
        
        layout.addWidget(menu_btn)
        
        return header
        
    def _create_footer(self):
        footer = QFrame()
        footer.setObjectName("footer")
        footer.setStyleSheet("""
            QFrame {
                background-color: #181E2B;
                min-height: 70px;
                border-top: 1px solid rgba(255, 0, 127, 0.2);
            }
        """)
        
        layout = QHBoxLayout(footer)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)
        
        # Campo de input
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Escribe un mensaje...")
        self.input_field.returnPressed.connect(self._send_message)
        layout.addWidget(self.input_field)
        
        # Botón de enviar
        send_btn = QPushButton("📩")
        send_btn.setToolTip("Enviar mensaje")
        send_btn.clicked.connect(self._send_message)
        layout.addWidget(send_btn)
        
        return footer
        
    def _load_previous_messages(self):
        """Cargar mensajes previos del historial"""
        for msg in self.conversation:
            self._add_message(msg["role"], msg["content"], save=False)
            
    def _add_message(self, role, text, save=True):
        """Agregar mensaje a la interfaz"""
        bubble = MessageBubble(text, is_user=(role == "user"))
        bubble_layout = QVBoxLayout()
        bubble_layout.setContentsMargins(0, 0, 0, 0)
        
        # Avatar y etiqueta
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        if role == "user":
            # Usuario a la derecha
            avatar = AvatarWidget()
            label = QLabel("Tú")
            label.setStyleSheet("color: #B0BAC9; font-size: 12px; background: transparent;")
            
            content_layout.addStretch()
            content_layout.addWidget(bubble)
            content_layout.addWidget(label)
            content_layout.addWidget(avatar)
            content_layout.setSpacing(10)
            
            bubble_layout.addStretch()
            bubble_layout.addWidget(content_widget)
            
        else:
            # Lumina a la izquierda
            avatar = AvatarWidget()
            label = QLabel("Lumina")
            label.setStyleSheet("color: #D8B4FF; font-size: 12px; background: transparent;")
            
            content_layout.addWidget(avatar)
            content_layout.addWidget(label)
            content_layout.addWidget(bubble)
            content_layout.setSpacing(10)
            
                        bubble_layout.addWidget(content_widget)
            
        else:
            # Lumina a la izquierda
            avatar = AvatarWidget()
            label = QLabel("Lumina")
            label.setStyleSheet("color: #D8B4FF; font-size: 12px; background: transparent;")
            
            content_layout.addWidget(avatar)
            content_layout.addWidget(label)
            content_layout.addWidget(bubble)
            content_layout.setSpacing(10)
            
            bubble_layout.addWidget(content_widget)
            
        self.chat_content_layout.addLayout(bubble_layout)
        
        if save:
            self.conversation.append({"role": role, "content": text})
            self._save_history()
            
        self.chat_scroll_area.verticalScrollBar().setValue(
            self.chat_scroll_area.verticalScrollBar().maximum()
        )
        
    def _send_message(self):
        text = self.input_field.text().strip()
        if not text:
            return
            
        self.input_field.clear()
        
        # Agregar mensaje del usuario
        self._add_message("user", text)
        
        # Obtener respuesta de la IA
        self._get_response(text)
        
    def _get_response(self, prompt):
        """Obtener respuesta de la IA"""
        if self.model is None:
            self._add_message("assistant", "Error: modelo no cargado")
            return
            
        # Construir prompt con historial
        history_text = ""
        if len(self.conversation) > 0:
            history_text = "\n\nHistorial (últimas 2):\n"
            for msg in self.conversation[-self.max_history*2:]:
                role = msg.get("role", "")
                content = msg.get("content", "")
                if role == "user":
                    history_text += f"Usuario: {content}\n"
                elif role == "assistant":
                    history_text += f"Computadora: {content}\n"
        
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
                prompt=full_prompt,
                max_tokens=150,
                temperature=0.7,
                stop=["\n\n", "\nUsuario:"]
            )
            
            output = response.get("choices", [{}])[0].get("text", "").strip()
            
            if lumina_prompt in output:
                output = output.replace(lumina_prompt, "").strip()
                
            self._add_message("assistant", output)
            
        except Exception as e:
            self._add_message("assistant", f"Error: {str(e)}")
            
    def _save_history(self):
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump({"messages": self.conversation}, f, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando: {e}")
            
    def _clear_chat(self):
        """Limpiar chat y historial"""
        self.conversation = []
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
        
        # Limpiar interfaz
        while self.chat_content_layout.count():
            child = self.chat_content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("AI Assistant Chat")
    
    window = AIChatApp()
    window.show()
    
    sys.exit(app.exec())
