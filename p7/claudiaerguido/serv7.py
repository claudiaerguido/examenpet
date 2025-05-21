#!/usr/bin/env python3
"""
serv7.py - Servidor de chat simple usando select()
Uso: python3 serv7.py
"""

import socket
import select
import signal
import sys

# Configuración del servidor
HOST = '0.0.0.0'     # Acepta conexiones desde cualquier IP
PORT = 4000          # Puerto en el que escucha
BACKLOG = 5          # Nº máximo de conexiones pendientes
BUFFER_SIZE = 1024   # Tamaño máximo de los mensajes

# Datos globales
clients = []         # Lista con todos los sockets conectados
nicknames = {}       # Diccionario: socket ➝ nick

# Enviamos un mensaje a todos los clientes menos a uno (si se quiere excluir)
def broadcast_message(message: bytes, exclude_sock=None):
    for sock in list(clients):
        if sock is exclude_sock or sock is listen_sock:
            continue
        try:
            sock.sendall(message)
        except:
            disconnect_client(sock)

# Cierra y elimina un cliente
def disconnect_client(sock: socket.socket):
    nick = nicknames.get(sock)
    if nick:
        msg = f"* {nick} se ha desconectado\n".encode()
        broadcast_message(msg, exclude_sock=sock)
        del nicknames[sock]

    if sock in clients:
        clients.remove(sock)
    try:
        sock.close()
    except:
        pass

# Ctrl+C → cerrar todo limpio
def handle_shutdown(signum, frame):
    msg = b"* SERVIDOR detenido, bye\n"
    for sock in list(clients):
        if sock is not listen_sock:
            try:
                sock.sendall(msg)
                sock.close()
            except:
                pass
    listen_sock.close()
    sys.exit(0)

# Función principal
def main():
    global listen_sock

    # Configura Ctrl+C para cerrar bien
    signal.signal(signal.SIGINT, handle_shutdown)

    # Crea el socket principal (escucha)
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_sock.bind((HOST, PORT))
    listen_sock.listen(BACKLOG)

    print(f"[+] Servidor escuchando en {HOST}:{PORT}")
    clients.append(listen_sock)  # lo añadimos a la lista para monitorizar

    # Bucle principal
    while True:
        read_ready, _, _ = select.select(clients, [], [])

        for sock in read_ready:
            if sock is listen_sock:
                # Nueva conexión
                conn, addr = listen_sock.accept()
                print(f"[+] Conexión desde {addr}")

                # Recibir nick
                data = conn.recv(BUFFER_SIZE)
                if not data:
                    conn.close()
                    continue
                nick = data.decode().strip()

                # Validar nick
                if nick in nicknames.values():
                    conn.sendall(b"ERROR: nick en uso\n")
                    conn.close()
                    continue

                # Aceptar y registrar
                conn.sendall(b"OK\n")
                clients.append(conn)
                nicknames[conn] = nick

                welcome_msg = f"* {nick} se ha conectado\n".encode()
                broadcast_message(welcome_msg, exclude_sock=conn)

            else:
                # Datos de un cliente
                try:
                    data = sock.recv(BUFFER_SIZE)
                except:
                    disconnect_client(sock)
                    continue

                if not data:
                    disconnect_client(sock)
                    continue

                # Reenviar mensaje con el nick
                nick = nicknames.get(sock, "?")
                text = data.decode()
                full_msg = f"{nick}: {text}".encode()
                broadcast_message(full_msg)

# Lanzamos el servidor
if __name__ == '__main__':
    main()
