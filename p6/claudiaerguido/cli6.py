import os 
import sys
import socket 

if len(sys.argv)!=2:
    print("Uso: introduce make cliente /ruta/")
    sys.exit(1)
socket_path=sys.argv(1)

if os.path.exists(socket_path):
    os.remove(socket_path)
cliente=socket.socket(socket.PF_INET,socket.SOCK_DGRAM)


try: 
    cliente.connect(socket_path)
    path_fichero=input("Introduce la ruta del fichero:")
    cliente.sendall(path_fichero.encode())
    respuesta= cliente.recv(4028).decode()
    print(f"Respuesta del servidor:{respuesta}")
finally: 
    cliente.close() 

