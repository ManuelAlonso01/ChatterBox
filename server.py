import socket
import threading

IP = "192.168.x.x"
PUERTO = 5000

class Cliente:
    def __init__(self, sock, addr, username):
        self.sock = sock
        self.addr = addr
        self.username = username

clientes = []

def recibir_bytes(sock, tamaño):
    chunks = []
    while tamaño > 0:
        bloque = sock.recv(min(4096, tamaño))
        if not bloque:
            break
        chunks.append(bloque)
        tamaño -= len(bloque)
    return b"".join(chunks)

def manejar_cliente(c):
    print(f"[+] Cliente conectado: {c.username} desde {c.addr}")

    try:
        while True:
            # El header tiene la siguiente forma: username:mensaje o en caso de una recibir
            # una imagen IMG:ruta
            header_raw = c.sock.recv(1024)
            header = header_raw.decode().strip()
            # Revisamos que no este vacio
            if not header:
                break

            # Si es una imagen calculamos el tamaño
            if header.startswith("IMG:"):
                tamaño = int(header.split(":", 1)[1])


                # Recibimos la imagen completa
                data = recibir_bytes(c.sock, tamaño)

                print(f"[IMG] Imagen recibida de {c.username}, reenviando...")

                # Reenviamos a todos menos al emisor
                for cli in clientes:
                    if cli != c:
                        # Primero avisamos que lo que mandamos es una imagen
                        cli.sock.send(f"IMG:{tamaño}".encode().ljust(1024, b" "))
                        # Luego procedemos a mandarla
                        cli.sock.sendall(data)

                continue

            # Texto normal
            mensaje = f"{c.username}:{header}"
            print(mensaje)

            # Enviamos el mensaje a todos los clientes menos al emisor
            for cliente in clientes:
                if cliente != c:
                    cliente.sock.send(mensaje.encode())
                    
    # Si hay un error con algun cliente lo printeamos
    # y con finally lo desconectamos
    except Exception as e:
        print(f"Error con {c.username}: {e}")

    finally:
        if c in clientes:
            clientes.remove(c)
        c.sock.close()
        print(f"[-] {c.username} desconectado")

# Servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((IP, PUERTO))
server.listen(5)
print("[SERVIDOR] Esperando conexiones...")

# Bucle principal para manejar a los clientes
while True:
    sock, addr = server.accept()
    # Recibimos el nombre de usuario
    username = sock.recv(1024).decode()
    # Creamos el objeto
    cliente = Cliente(sock, addr, username)
    # Lo agregamos a la lista de clientes
    clientes.append(cliente)
    # Cada cliente se maneja con un hilo propio
    threading.Thread(target=manejar_cliente, args=(cliente,), daemon=True).start()
