# ChatterBox

**ChatterBox** es una aplicación de chat simple basada en la arquitectura cliente-servidor, implementada en Python. Permite la comunicación en tiempo real entre múltiples usuarios a través de una conexión de red local (o remota si se configura).

## 📋 Características

- **Arquitectura Cliente-Servidor:** Un servidor central gestiona las conexiones y retransmite los mensajes.
- **Comunicación en Tiempo Real:** Envío y recepción de mensajes instantáneos.
- **Soporte Multi-usuario:** Capacidad para conectar varios clientes simultáneamente.
- **Interfaz de Consola:** Ligera y fácil de ejecutar desde la terminal.

## 🚀 Requisitos Previos

Para ejecutar este proyecto, necesitas tener instalado:

- [Python 3.x](https://www.python.org/downloads/)

## 🛠️ Instalación y Configuración

1. **Clonar el repositorio:**

   ```bash
   git clone [https://github.com/ManuelAlonso01/ChatterBox.git](https://github.com/ManuelAlonso01/ChatterBox.git)
   cd ChatterBox
   ```

## 💻 Uso
1. ### Configuracion ###
   Primero, debes configurar la direccion IP y el puerto en los archivos de ```server.py``` y ```cliente.py```.

2. ### Iniciar el Servidor ###
   Dentro de la carpeta del proyecto, ejecuta el comando:
   ```bash
   python server.py
   ```
   o en linux:
   ```bash
   python3 server.py
   ```
3. ### Iniciar Cliente ###
   Si quieres ejecutar un cliente en la misma computadora, solo abre una nueva terminal, navega hasta la carpeta del proyecto y ejecuta:
   ```bash
   python cliente.py
   ```
   o en linux:
   ```bash
   python3 cliente.py
   ```
   Solo asegurate de que el script ```cliente.py``` tenga el mismo **puerto** y la misma direccion **IP** que el servidor.

   #### Nota ####
   Para ejecutar un cliente desde una maquina diferente solo clona el repositorio, configura la IP y el puerto del script ```cliente.py``` y se conectara automaticamente        al     servidor. Es importante aclarar que ambas maquinas deben permanecer dentro de la misma red wifi.

4. ### Enviar Mensajes e Imagenes ###
   Para enviar un mensaje, solo escribe lo que quieras enviar y apreta enter, para enviar imagenes usa el comando ```/img``` seguido de la ruta de la imagen. ej:
   ```bash
   /img imagen.png
   ```
   
    

