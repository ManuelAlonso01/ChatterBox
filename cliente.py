import socket
import threading
import platform
import os

IP = "192.168.x.xx"
PUERTO = 5000

def abrir_imagen_segun_so(ruta):
    sistema = platform.system()
    if sistema == "Windows":
        os.system(f"start {ruta}")
    elif sistema == "Linux":
        os.system(f"xdg-open {ruta}")
    else: # Mac
        os.system(f"open {ruta}")

def recibir_mensajes(client, username):
    while True:
        try:
            header_raw = client.recv(1024)
            header = header_raw.decode().strip()
            if header.startswith("IMG:"):
                tamaño = int(header.split(":", 1)[1])
                data = recibir_bytes(client, tamaño)
                guardar_img(data)
                print("Llego una imagen")
                abrir_imagen_segun_so("imagen_recibida.jpg")
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
            header = mensaje.encode().ljust(1024, b" ")
            client.sendall(header)


    
def enviar_imagen(client, ruta):
    with open(ruta, "rb") as f:
        data = f.read()
    header = f"IMG:{len(data)}".encode().ljust(1024, b" ")
    client.sendall(header)
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
    

