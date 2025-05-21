import socket
import os
from datetime import datetime

# Cambiar el nombre del proceso
try:
    import setproctitle
    setproctitle.setproctitle("serv5")
except ImportError:
    pass

# Configuración desde variables de entorno
PORT = int(os.getenv("PORT", 9009))  # Personalizable
HOST = os.getenv("HOST", "127.0.0.1")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((HOST, PORT))

print(f"[Servidor] Escuchando en {HOST}:{PORT} (UDP)")

try:
    while True:
        data, addr = sock.recvfrom(1024)
        print(f"[Servidor] Petición recibida de {addr}")
        fecha_hora = datetime.now().isoformat()
        sock.sendto(fecha_hora.encode(), addr)
except KeyboardInterrupt:
    print("\n[Servidor] Cerrando servidor UDP.")
finally:
    sock.close()

