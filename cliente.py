import socket
import threading
import platform
import os

IP = "IP del SERVIDOR"
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
            if ":" in header:
                prefijo, contenido = header.split(":", 1)
                if prefijo in ["IMG", "AUDIO", "VIDEO"]:
                    tamaño = int(contenido)
                    data = recibir_bytes(client, tamaño)
                    nombre_archivo = guardar_archivo(data, prefijo.lower())
                    print(f"Llego un {prefijo}")
                    abrir_imagen_segun_so(nombre_archivo)
                    continue
                else:
                    print(f"{prefijo}: {contenido}")
        except:
            print("Desconectado del servidor")
            client.close()
            break
        
def enviar_mensajes(client):
    while True:
        mensaje = input("> ")
        if mensaje.startswith(("/img ", "/audio ", "/video ")):
            partes = mensaje.split(" ", 1)
            tipo = partes[0][1:].upper() # Convierte /img a IMG
            enviar_archivo(client, partes[1], tipo)
        else:
            client.sendall(mensaje.encode().ljust(1024, b" "))


    
def enviar_archivo(client, ruta, tipo):
    with open(ruta, "rb") as f:
        data = f.read()
    header = f"{tipo}:{len(data)}".encode().ljust(1024, b" ")
    client.sendall(header)
    client.sendall(data)
    print("ARCHIVO ENVIADO")
    
def recibir_bytes(client, tamaño):
    chunks = []
    while tamaño > 0:
        bloque = client.recv(min(4096, tamaño))
        if not bloque:
            break
        chunks.append(bloque)
        tamaño -= len(bloque)
    return b"".join(chunks)
        

        
def guardar_archivo(data, tipo):
    extensiones = {"img": "jpg", "audio": "wav", "video": "avi"}
    nombre = f"recibido_{tipo}.{extensiones[tipo]}"
    with open(nombre, "wb") as file:
        file.write(data)
    return nombre
    

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
    
