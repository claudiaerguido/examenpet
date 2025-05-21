import os
import time 

fifo_path='/tmp/fifo_grupo5'

if not os.path.exists(fifo_path):
    print(f"No hay tuberia con ese{fifo_path}")
    exit(1)

with open(fifo_path,'w') as fifo:
    fifo.write("Dame la fecha y hora") 

with open(fifo_path,'r') as fifo: 
    respuesta= fifo.read() 

print(f"La fecha y la hora son:{respuesta}")
