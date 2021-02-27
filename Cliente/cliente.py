import json
import threading
import socket

from interfaz import Controlador

class CLIENTE:

    def __init__(self, host, port):

        self.host = host
        self.port = port
    
        #Inicializar Gui
        self.controlador = Controlador(self)

        self.socket_cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # Conectarse con el servidor
            self.socket_cliente.connect((self.host, self.port))
            self.conectado = True

            # Escuchar los mensajes del servidor
            thread = threading.Thread(
                target=self.escuchar_servidor,
                daemon=True
            )
            thread.start()
            self.controlador.mostrar_login()
        except ConnectionRefusedError:
            print(f"No se pudo conectar a {self.host}:{self.port}")
            self.socket_cliente.close()

    def escuchar_servidor(self):

        try:
            while self.conectado:
                mensaje = self.recibir()
                print("Mensaje recibido, mensaje", mensaje)
                self.controlador.manejar_mensaje(mensaje)

        except ConnectionResetError:
            print("Error de conexion con el servidor")
        
        finally:
            self.socket_cliente.close()

    def enviar(self, mensaje):
        
        try:
            bytes_mensaje = self.codificar_mensaje(mensaje)
            largo_mensaje_bytes = len(bytes_mensaje).to_bytes(4, byteorder= "big")

            self.socket_cliente.sendall(largo_mensaje_bytes + bytes_mensaje)

        except ConnectionError:
            self.socket_cliente.close()
        pass

    def recibir(self):

        largo_mensaje_bytes = self.socket_cliente.recv(4)
        
        largo_mensaje = int.from_bytes(largo_mensaje_bytes, byteorder="big")
        # Recibir mensaje
        bytes_mensaje = bytearray()
        while len(bytes_mensaje) < largo_mensaje:
            tamano_chunk = min(largo_mensaje - len(bytes_mensaje), 60)
            bytes_mensaje += self.socket_cliente.recv(tamano_chunk)
            
        # Decodificar mensaje
        mensaje = self.decodificar_mensaje(bytes_mensaje)
        return mensaje

    def codificar_mensaje(self, mensaje):

        try:
            json_mensaje = json.dumps(mensaje)
            bytes_mensaje = json_mensaje.encode()
            return bytes_mensaje
        except json.JSONDecodeError:
            print("Error al codificar mensaje")
            return ""

    
    def decodificar_mensaje(self, mensaje):

        try:
            msj = json.loads(mensaje)
            return msj
        
        except json.JSONDecodeError:
            print("Error al decodificar mensaje")
            return dict()