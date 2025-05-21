#!/usr/bin/env python3
"""
cli7.py - Cliente de chat simple usando select()
Uso: python3 cli7.py <host> <puerto>
"""

import socket
import select
import sys

BUFFER_SIZE = 1024  # Tamaño máximo de mensaje

def main():
    if len(sys.argv) != 3:
        print(f"Uso: {sys.argv[0]} <host> <puerto>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])

    # 1. Crear socket y conectar
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((host, port))
    except Exception as e:
        print(f"❌ Error al conectar: {e}")
        sys.exit(1)

    # 2. Pedir nick
    nick = input("🧑 Tu nick: ").strip()
    if not nick:
        print("❌ El nick no puede estar vacío.")
        sock.close()
        sys.exit(1)

    # 3. Enviar nick al servidor
    sock.sendall((nick + "\n").encode())

    # 4. Esperar respuesta
    respuesta = sock.recv(BUFFER_SIZE).decode()
    if respuesta.startswith("ERROR"):
        print(respuesta.strip())
        sock.close()
        sys.exit(1)

    print("✅ Conectado al chat. Escribe mensajes o /quit para salir.")

    # 5. Bucle de entrada/salida con select
    while True:
        # Espera hasta que haya algo en stdin o en el socket
        read_ready, _, _ = select.select([sys.stdin, sock], [], [])

        for fuente in read_ready:
            if fuente is sock:
                # Mensaje del servidor
                datos = sock.recv(BUFFER_SIZE)
                if not datos:
                    print("⚠️ El servidor cerró la conexión.")
                    sock.close()
                    sys.exit(0)
                print(datos.decode(), end='')

            else:
                # Entrada por teclado
                linea = sys.stdin.readline()
                if not linea:
                    print("👋 Desconectando...")
                    sock.close()
                    sys.exit(0)

                linea = linea.rstrip("\n")
                if linea == "/quit":
                    print("👋 Saliendo del chat...")
                    sock.close()
                    sys.exit(0)

                sock.sendall((linea + "\n").encode())

if __name__ == "__main__":
    main()
