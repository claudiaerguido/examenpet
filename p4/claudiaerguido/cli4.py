import os
import socket
import sys

if len(sys.argv) != 2:
    print("Uso: python3 serv4.py /ruta/del/socket")
    sys.exit(1)

socket_path = sys.argv[1]

if os.path.exists(socket_path):
    os.remove(socket_path)

server_socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_socket.bind(socket_path)
server_socket.listen()

print(f"Servidor escuchando en {socket_path}...")

try:
    while True:
        conn, _ = server_socket.accept()
        with conn:
            print("Cliente conectado")
            data = conn.recv(1024).decode('utf-8').strip()

            # Si se pide cerrar el servidor
            if data == "exit":
                conn.sendall("Servidor apagado.".encode('utf-8'))
                break

            try:
                with open(data, 'r') as fd:
                    contenido = fd.read()
            except Exception as e:
                contenido = f"Error al abrir fichero: {e}"

            conn.sendall(contenido.encode('utf-8'))

finally:
    server_socket.close()
    os.remove(socket_path)
    print("Servidor cerrado.")