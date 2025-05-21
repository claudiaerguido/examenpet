import socket
import os

# Configuración del servidor
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5008
BUFFER_SIZE = 1024  # Tamaño de buffer para recibir fragmentos

def cliente():
    # Crear socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)  # Configurar timeout para evitar quedarse esperando indefinidamente

    print("[CLIENTE] Cliente UDP iniciado...")

    file_path = input("Ruta del archivo a consultar: ")

    # Enviar la petición al servidor
    sock.sendto(file_path.encode(), (SERVER_HOST, SERVER_PORT))

    # Recibir el archivo fragmentado
    fragmentos = []
    while True:
        try:
            fragmento, addr = sock.recvfrom(BUFFER_SIZE)
            if not fragmento:  # Si no se recibe más fragmento, terminar
                break
            print(f"[CLIENTE] Recibido fragmento de {len(fragmento)} bytes.")
            fragmentos.append(fragmento)
        except socket.timeout:
            print("[CLIENTE] Timeout alcanzado. Terminando recepción.")
            break

    # Guardar los fragmentos recibidos en un archivo
    if fragmentos:
        with open('archivo_recibido', 'wb') as f:
            for fragmento in fragmentos:
                f.write(fragmento)
        print("[CLIENTE] Archivo recibido completamente.")
    else:
        print("[CLIENTE] No se recibió respuesta del servidor.")

if __name__ == '__main__':
    cliente()

