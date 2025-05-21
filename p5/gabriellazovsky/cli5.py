import socket
import os

# Cambiar el nombre del proceso
try:
    import setproctitle
    setproctitle.setproctitle("cli5")
except ImportError:
    pass

# Configuración desde entorno
PORT = int(os.getenv("PORT", 9009))
HOST = os.getenv("HOST", "127.0.0.1")

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)

try:
    sock.sendto(b"hora", (HOST, PORT))
    data, _ = sock.recvfrom(1024)
    print("[Cliente] Fecha y hora recibidas:", data.decode())
except socket.timeout:
    print("[Cliente] Error: El servidor no respondió.")
finally:
    sock.close()

