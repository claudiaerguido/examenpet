import os
import socket

# Definir el tamaño máximo del fragmento
MAX_FRAGMENT_SIZE = 1024  # tamaño más pequeño que 65507 bytes, ajustable

def servidor():
    # Crear socket UDP
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('0.0.0.0', 5008))  # Escuchar en el puerto 5008

    print("[SERVIDOR] Servidor UDP iniciado en puerto 5008...")

    while True:
        data, addr = sock.recvfrom(1024)
        file_path = data.decode('utf-8')
        
        print(f"[SERVIDOR] Petición recibida del cliente: {addr} para el archivo: {file_path}")
        
        if os.path.exists(file_path) and os.path.isfile(file_path):
            with open(file_path, 'rb') as f:
                file_data = f.read()

            file_size = len(file_data)
            print(f"[SERVIDOR] Archivo encontrado. Enviando {file_size // MAX_FRAGMENT_SIZE + 1} fragmentos.")

            # Dividir el archivo en fragmentos más pequeños
            num_fragments = (file_size // MAX_FRAGMENT_SIZE) + 1
            for i in range(num_fragments):
                fragment = file_data[i * MAX_FRAGMENT_SIZE: (i + 1) * MAX_FRAGMENT_SIZE]
                try:
                    print(f"[SERVIDOR] Enviando fragmento {i + 1} de {num_fragments} con tamaño {len(fragment)} bytes.")
                    sock.sendto(fragment, addr)  # Enviar fragmento
                except Exception as e:
                    print(f"[SERVIDOR] Error al enviar el fragmento: {e}")
                    break

            print("[SERVIDOR] Transferencia completada.")
        else:
            error_message = "Error: El archivo no existe o no se puede abrir."
            sock.sendto(error_message.encode(), addr)
            print(f"[SERVIDOR] {error_message}")

def main():
    servidor()

if __name__ == '__main__':
    main()

