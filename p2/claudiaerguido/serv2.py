import os

pipe_name = '/tmp/mypipe'
if os.path.exists(pipe_name):
    os.remove(pipe_name)

print("Servidor esperando...")
os.mkfifo(pipe_name)


while True: 
    with open(pipe_name,'r') as pipe: 
        path = pipe.readline().strip()
        if path == " ":
            print("No se ha recibido nada")
            
        print("Servidor esperando solicitudes")
        
        try: 
            with open(path,'r') as fichero: 
                contenido= fichero.read() 
        except Exception as e: 
            contenido = f"Fallo al abrir fichero: {e}"
    with open(pipe_name,'w') as pipe:   
        pipe.write(contenido)
    break; 

print("Servidor terminado")

