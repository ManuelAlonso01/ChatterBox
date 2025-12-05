import socket
import threading

IP = "192.168.1.62"
PUERTO = 5000

class Cliente:
    def __init__(self, sock, addr, username):
        self.sock = sock
        self.addr = addr
        self.username = username

clientes = []

def recibir_bytes(sock, tamaño):
    data = b""
    while len(data) < tamaño:
        chunk = sock.recv(min(4096, tamaño - len(data)))
        if not chunk:
            break
        data += chunk
    return data

def manejar_cliente(c):
    print(f"[+] Cliente conectado: {c.username} desde {c.addr}")

    try:
        while True:
            header = c.sock.recv(1024)
            if not header:
                break

            header = header.decode()

            if header.startswith("IMG:"):
                tamaño = int(header.split(":", 1)[1])


                # Recibimos la imagen completa
                data = recibir_bytes(c.sock, tamaño)

                print(f"[IMG] Imagen recibida de {c.username}, reenviando...")

                # Reenviamos a todos menos al emisor
                for cli in clientes:
                    if cli != c:
                        cli.sock.send(f"IMG:{tamaño}".encode())
                        cli.sock.sendall(data)

                continue

            # Texto normal
            mensaje = f"{c.username}:{header}"
            print(mensaje)

            for cli in clientes:
                if cli != c:
                    cli.sock.send(mensaje.encode())

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

while True:
    sock, addr = server.accept()
    username = sock.recv(1024).decode()

    cliente = Cliente(sock, addr, username)
    clientes.append(cliente)

    threading.Thread(target=manejar_cliente, args=(cliente,), daemon=True).start()
