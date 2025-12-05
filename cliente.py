import socket
import threading

IP = "192.168.1.62"
PUERTO = 5000

def recibir_mensajes(client, username):
    while True:
        try:
            header = client.recv(1024).decode()
            if header.startswith("IMG:"):
                tamaño = int(header.split(":", 1)[1])
                data = recibir_bytes(client, tamaño)
                guardar_img(data)
                print("Llego una imagen")
                continue
            autor, texto = header.split(":", 1)
            if autor == username:
                print(f"Tu: {texto}")
            else:
                print(f"{autor}:{texto}")
        except:
            print("Desconectado del servidor")
            client.close()
            break
        
def enviar_mensajes(client):
    while True:
        mensaje = input("> ")
        if mensaje.startswith("/img"):
            ruta = mensaje.split(" ", 1)[1]
            enviar_imagen(client, ruta)
        else:
            client.send(mensaje.encode())


    
def enviar_imagen(client, ruta):
    with open(ruta, "rb") as f:
        data = f.read()
    header = f"IMG:{len(data)}"
    client.send(header.encode())
    client.sendall(data)
    print("Imagen enviada")
    
def recibir_bytes(client, tamaño):
    chunks = []
    while tamaño > 0:
        bloque = client.recv(min(4096, tamaño))
        if not bloque:
            break
        chunks.append(bloque)
        tamaño -= len(bloque)
    return b"".join(chunks)
        
def guardar_img(data):
    with open("imagen_recibida.jpg", "wb") as file:
        file.write(data)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PUERTO))
print("Conectado al servidor")

# Mandamos el nombre de usuario
username = input("Nombre de usuario: ")
client.send(username.encode())

enviar = threading.Thread(target=enviar_mensajes, args=(client,))
recibir = threading.Thread(target=recibir_mensajes, args=(client, username))
enviar.start()
recibir.start()
    
