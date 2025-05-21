# 🧱 Documento de Arquitectura – Práctica 7

## 1. Descripción general

Este proyecto implementa un sistema de chat cliente-servidor utilizando sockets TCP de Internet (`AF_INET`, `SOCK_STREAM`) y la función `select()` para gestionar múltiples clientes sin usar hilos.  
El servidor permite que varios clientes se conecten de forma simultánea, cada uno con un identificador único (nick), y retransmite los mensajes que cada uno envía al resto.

---

## 2. Componentes principales

### 2.1 Servidor (`serv7.py`)

- Crea un socket TCP que escucha conexiones entrantes en el puerto 4000.
- Usa `select.select()` para gestionar múltiples clientes en paralelo.
- Mantiene una lista de sockets activos (`clients`) y un diccionario de nicks (`nicknames`).
- Valida que los nicks sean únicos y rechaza conexiones duplicadas.
- Reenvía los mensajes a todos los demás clientes usando `broadcast_message()`.
- Permite cierre controlado con `Ctrl+C`, enviando aviso a todos los clientes antes de apagar el servidor.

### 2.2 Cliente (`cli7.py`)

- Se conecta al servidor con IP y puerto configurables desde la línea de comandos.
- Solicita al usuario un nick único que es enviado al servidor.
- Usa `select.select()` para escuchar al mismo tiempo mensajes del servidor y entrada por teclado.
- Envía los mensajes escritos por el usuario y muestra en pantalla los mensajes recibidos.
- Permite desconectarse escribiendo `/quit` o pulsando `Ctrl+D`.
- Gestiona desconexiones del servidor y errores de forma limpia.

---

## 3. Tecnologías utilizadas

- Lenguaje: Python 3
- Sockets TCP/IP (`socket.AF_INET`, `socket.SOCK_STREAM`)
- Multiplexación de entrada/salida: `select.select()`
- Manejo de señales: `signal.signal()` para `SIGINT`
- Codificación de mensajes: UTF-8

---

## 4. Protocolo de comunicación

1. El cliente se conecta al servidor y envía su nick.
2. El servidor valida el nick:
   - Si está repetido ➝ envía `"ERROR: nick en uso"` y cierra.
   - Si es válido ➝ envía `"OK"` y lo añade al chat.
3. El cliente entra en el chat y empieza a enviar mensajes.
4. El servidor reenvía todos los mensajes a los demás clientes con el formato `nick: mensaje`.
5. Si el cliente escribe `/quit` o `Ctrl+D` ➝ se desconecta.
6. Si el servidor se apaga (`Ctrl+C`) ➝ envía `* SERVIDOR detenido, bye` a todos y cierra.

---

## 5. Gestión de errores y desconexiones

- Clientes con nicks duplicados son rechazados automáticamente.
- Si un cliente se desconecta o el `recv()` falla, el servidor lo elimina y notifica al resto.
- Si el servidor se cierra con `Ctrl+C`, avisa a todos los clientes antes de cerrar conexiones.
- Todo está protegido con bloques `try/except` para evitar errores no controlados.

---

## 6. Posibilidades de mejora

- Añadir interfaz gráfica (Tkinter, curses o web).
- Añadir historial persistente de mensajes.
- Cifrar las comunicaciones con SSL.
- Añadir comandos `/users`, `/whisper`, `/rename`, `/kick`, etc.
- Registrar eventos del servidor en un archivo de log.