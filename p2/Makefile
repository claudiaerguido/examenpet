# Makefile para compilar y ejecutar cli2.py y serv2.py

# Regla para compilar el servidor
serv2: serv2.py
	python3 serv2.py

# Regla para compilar el cliente
cli2: cli2.py
	python3 cli2.py

# Regla para ejecutar el servidor
run_serv: serv2
	python3 serv2.py

# Regla para ejecutar el cliente
run_cli: cli2
	python3 cli2.py

# Limpiar (por si se necesita borrar archivos temporales)
clean:
	rm -f fifo_cli2serv fifo_serv2cli


all:
	@echo "Compilación y ejecución de la práctica"

clean:
	@echo "Limpiando..."
