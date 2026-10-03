#!/bin/bash
echo "Instalando regla udev para keyboard..."
echo 'KERNEL=="event*", GROUP="input", MODE="0660"' | sudo tee /etc/udev/rules.d/99-keyboard.rules

echo "Agregando usuario al grupo input..."
sudo usermod -a -G input $USER

echo "Recargando reglas udev..."
sudo udevadm control --reload-rules
sudo udevadm trigger

echo "✅ Configuración completa. Reinicia sesión o el sistema para aplicar los cambios."