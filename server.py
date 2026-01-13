import socket
import threading

IP = "0.0.0.0"
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
            header_raw = c.sock.recv(1024)
            if not header_raw: break
            header = header_raw.decode().strip()

            # Comprobar si es un archivo (buscando el ":")
            if ":" in header and header.split(":")[0] in ["IMG", "AUDIO", "VIDEO"]:
                tipo, tamaño = header.split(":")
                tamaño = int(tamaño)
                data = recibir_bytes(c.sock, tamaño)

                for cli in clientes:
                    if cli != c:
                        cli.sock.sendall(header_raw) # Reenviamos el header exacto
                        cli.sock.sendall(data)
                continue

            # Texto normal
            for cli in clientes:
                if cli != c:
                    mensaje = f"{c.username}:{header}"
                    cli.sock.send(mensaje.encode().ljust(1024, b" "))
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
