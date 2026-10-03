#!/bin/bash
# Wrapper para llama-cli con librerías correctas
export LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"
exec /usr/local/bin/llama-cli "$@"
