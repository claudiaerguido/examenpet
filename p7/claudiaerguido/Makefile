IP ?= 127.0.0.1
PUERTO ?= 4000

all:
	@echo "Uso:"
	@echo "  make servidor              # Lanza el servidor en el puerto 4000"
	@echo "  make cliente IP=... PUERTO=...  # Lanza el cliente con la IP y puerto del servidor"

servidor:
	python3 serv7.py

cliente:
	python3 cli7.py $(IP) $(PUERTO)

clean:
	@echo "Nada que limpiar en esta práctica."
