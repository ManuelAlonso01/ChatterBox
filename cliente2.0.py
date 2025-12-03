import socket
import threading

IP = "192.168.1.62"
PUERTO = 5000

def recibir_mensajes(client, username):
    while True:
        try:
            mensaje = client.recv(1024).decode()  
            if mensaje.startswith("IMG:"):
                tamaño = int(mensaje.split(":")[1])
                client.send(b"OK")
                recibir_imagen(mensaje, tamaño)
                print("Imagen recibida.")
                continue
            if mensaje:
                autor, texto = mensaje.split(":", 1)
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
        mensaje = input("")
        if "imagen" in mensaje.lower():
            enviar_imagen(client)
        client.send(mensaje.encode())

def enviar_imagen(client):
    imagen = input("Ingrese la ruta de la imagen: ")
    with open(imagen, "rb") as f:
        datos = f.read()
    tamaño = len(datos)
    client.send(f"IMG:{tamaño}".encode())
    client.recv(4)
    client.sendall(datos)

def recibir_imagen(client, tamaño):
    with open("imagen_recibida.png", "wb") as f:
        while tamaño > 0:
            chunks = client.recv(min(4096, tamaño))
            if not chunks:
                break
            f.write(chunks)
            tamaño -= len(chunks)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((IP, PUERTO))
print("Conectado al servidor")

# Mandamos el nombre de usuario
username = input("Nombre de usuario: ")
client.send(username.encode())

enviar = threading.Thread(target=enviar_mensajes, args=(client,))
recivir = threading.Thread(target=recibir_mensajes, args=(client, username))
enviar.start()
recivir.start()
    