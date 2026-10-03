#!/bin/bash
# Probar chat con una pregunta
echo 'hola' > /tmp/test_chat_input.txt
echo '/quit' >> /tmp/test_chat_input.txt

echo "Probando chat..."

# Crear script expect para la interacción
expect << 'EOF' > /tmp/test_output.txt 2>&1
spawn python3 app_chat.py
expect "Usuario:"
send "hola\r"
expect "Computadora:"
send "/quit\r"
expect eof
EOF

cat /tmp/test_output.txt
