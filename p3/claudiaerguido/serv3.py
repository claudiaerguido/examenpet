import os 
import time 

fifo_path='/tmp/fifo_grupo5'

if os.path.exists(fifo_path):
    os.remove(fifo_path)

os.mkfifo(fifo_path)
print("Esperando solicitudes...")

with open(fifo_path,'r') as fifo:
    solicitud=fifo.readline().split()

    if solicitud != 0:
        print(f"Servidor ha recibido una solicitud {solicitud}")

fecha_hora=time.strftime("%Y-%m-%d %H:%M:%S")

with open(fifo_path,'w') as fifo: 
    fifo.write(f"Fecha y hora actuales:{fecha_hora}")

print("Servidor terminado")