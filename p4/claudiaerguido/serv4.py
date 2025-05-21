import socket
import sys

if len(sys.argv) != 2:
    print("Uso: python3 cli4.py /ruta/del/socket")
    sys.exit(1)

socket_path = sys.argv[1]

cliente = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

try:
    cliente.connect(socket_path)

    path_fichero = input("Introduce la ruta del fichero que quieres leer (o 'exit' para cerrar servidor): ").strip()

    cliente.sendall(path_fichero.encode())
    respuesta = cliente.recv(4096).decode()

    print(f"\nRespuesta del servidor:\n{respuesta}")

finally:
    cliente.close()