import os 

pipe_name= '/tmp/mypipe'
if not os.path.exists(pipe_name): 
    print("La tuberia no existe")
    exit(1)

path= input("Introduce la ruta del fichero que quieres leer:")

with open(pipe_name,'w') as pipe:
    pipe.write(path + '\n')

with open(pipe_name,'r') as pipe: 
    respuesta= pipe.read() 

print(f"El contenido del fichero es{respuesta}")
