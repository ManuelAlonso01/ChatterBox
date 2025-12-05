import socket
import threading

# Configuración del servidor
IP = "192.168.1.55"  # Debe coincidir con el IP en tu script de cliente
PUERTO = 8000    # Debe coincidir con el PUERTO en tu script de cliente
FORMATO = 'utf-8'

# Lista para guardar los clientes conectados (socket, username)
clientes = []
# Bloqueo para manejar el acceso concurrente a la lista de clientes
lock = threading.Lock()

def broadcast(mensaje, cliente_emisor):
    """
    Envía un mensaje a todos los clientes conectados,
    excepto al cliente que lo envió.
    """
    with lock:
        for cliente, username in clientes:
            # No enviar el mensaje de vuelta al cliente que lo envió.
            # (Aunque tu cliente.py ya maneja no imprimir su propio mensaje, 
            # esta es una buena práctica de servidor).
            if cliente != cliente_emisor:
                try:
                    cliente.send(mensaje)
                except:
                    # Si falla el envío, asumimos que el cliente está desconectado
                    remover_cliente(cliente)

def remover_cliente(cliente):
    """
    Remueve un cliente de la lista global de clientes.
    """
    with lock:
        if (cliente, username) in clientes:
            clientes.remove((cliente, username))
            print(f"Cliente desconectado: {username}")
            # Notificar al resto del chat
            mensaje_desconexion = f"SERVIDOR:{username} ha abandonado el chat.".encode(FORMATO)
            broadcast(mensaje_desconexion, cliente)
            cliente.close()

def manejar_cliente(cliente, address):
    """
    Maneja la comunicación con un cliente específico en un hilo.
    """
    print(f"Nueva conexión: {address}")
    username = "Desconocido"
    
    try:
        # 1. Recibir el nombre de usuario del cliente (es lo primero que envía)
        username_bytes = cliente.recv(1024)
        if not username_bytes:
            print(f"El cliente en {address} no envió el nombre de usuario.")
            cliente.close()
            return
            
        username = username_bytes.decode(FORMATO)
        print(f"Nombre de usuario de {address}: {username}")

        # 2. Agregar el cliente a la lista global
        with lock:
            clientes.append((cliente, username))
        
        # 3. Notificar al resto del chat que un usuario se unió
        mensaje_conexion = f"SERVIDOR:{username} se ha unido al chat.".encode(FORMATO)
        broadcast(mensaje_conexion, cliente)

        # 4. Bucle principal para recibir mensajes
        while True:
            mensaje = cliente.recv(1024).decode(FORMATO)
            
            if not mensaje:
                # Cliente se ha desconectado o cerró la conexión
                break
            
            # 5. Lógica de manejo de comandos
            if mensaje.startswith("img"):
                # El cliente envió un comando /img. 
                # Tu cliente envía 'img', luego espera 4 bytes, y luego envía la ruta.
                # Aquí enviamos la respuesta de 4 bytes para que el cliente proceda.
                cliente.send("ACK!".encode(FORMATO))
                
                # Recibimos la ruta del archivo que el cliente intentó enviar.
                # Nota: Este servidor solo maneja el anuncio, no la transferencia del archivo.
                ruta_img_bytes = cliente.recv(1024)
                if ruta_img_bytes:
                    ruta_img = ruta_img_bytes.decode(FORMATO)
                    mensaje_img = f"{username}:(IMAGEN) Ha compartido la ruta: {ruta_img}".encode(FORMATO)
                    print(f"IMG de {username}: {ruta_img}")
                    broadcast(mensaje_img, cliente)
                
            else:
                # Es un mensaje de chat normal
                mensaje_chat = f"{username}:{mensaje}".encode(FORMATO)
                print(f"{username}: {mensaje}")
                broadcast(mensaje_chat, cliente)

    except Exception as e:
        print(f"Error en el manejo de {username} ({address}): {e}")

    finally:
        # Se rompió el bucle o hubo una excepción, remover al cliente
        remover_cliente(cliente)

def iniciar_servidor():
    """
    Configura e inicia el servidor principal.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permite reusar la misma dirección (IP y puerto) rápidamente
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    server.bind((IP, PUERTO))
    server.listen()
    print(f"Servidor escuchando en {IP}:{PUERTO}")
    
    while True:
        # Bloquea y espera una nueva conexión
        cliente_socket, address = server.accept()
        
        # Crea un nuevo hilo para manejar al cliente y vuelve a esperar otro cliente
        hilo_cliente = threading.Thread(target=manejar_cliente, args=(cliente_socket, address))
        hilo_cliente.start()
        # Muestra el número actual de hilos activos (conexiones activas + principal)
        print(f"Clientes activos: {threading.active_count() - 1}")

if __name__ == '__main__':
    iniciar_servidor()