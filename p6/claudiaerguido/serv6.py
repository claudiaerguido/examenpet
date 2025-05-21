import sys
import socket 
import os

if len(sys.argv)!= 2: 
    print("Uso: introduce make servidor /ruta/")
    sys.exit(1)

socket_path= sys.argv(1) 

if os.path.exists(socket_path):
    os.remove(socket_path)

server_socket=socket.socket(socket.PF_INET,socket.SOCK_STREAM)
server_socket.bind(socket_path)
server_socket.listen() 

print(f"Servidor escuchando en el puerto:{socket_path}")

try: 
    while True: 
        conn,adre=server_socket.accept()
        with conn: 
            print("Cliente conectado")
            data=conn.recv(1028).decode('utf-8').strip()
        try: 
            with open(data,'r') as fd:
                contenido=fd.read()
        except Exception as e:
            print(f"Error siguiente excepción:{e}")
        conn.sendall(contenido.encode())
        conn.close()
finally: 
    server_socket.close()
    os.remove(socket_path)