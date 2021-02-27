import json
import socket
import threading
from random import randint, choice

from mapa import crear_mapa
from jugadores import crear_lista_jugadores
from logica import LOGICA


class SERVIDOR:

    lista_nombres_lock = threading.Lock()

    def __init__(self, host, port, dict_mapa, lista_nombres, cantidad_jugadores, log_activado=True):

        self.host = host
        self.port = port
        self.dict_mapa = dict_mapa
        self.log_activado = log_activado
        self.cantidad_jugadores = cantidad_jugadores
        self.activos = 0
        self.jugadores_activos = []
        self.jugadores_activos_nombre = []
        self.se_envio_cantidad = False

        self.lista_nombres = lista_nombres
        self.lista_jugadores = crear_lista_jugadores(self.lista_nombres)

        self.logica = LOGICA()
        self.mapa = self.creacion_mapa()

        self.log("Iniciando servidor...")


        self.socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_server.bind((self.host, self.port))


        self.socket_server.listen()

        thread = threading.Thread(target=self.aceptar_clientes, daemon=True)
        thread.start()

    def aceptar_clientes(self):
        while True:
            nombre_aleatorio = choice(self.lista_nombres)
            self.lista_nombres.remove(nombre_aleatorio)
            socket_cliente, address = self.socket_server.accept()
            jugador = None
            self.lista_nombres_lock.acquire()
            for jugador in self.lista_jugadores:
                if jugador.socket_cliente is None:
                    jugador.username = nombre_aleatorio
                    jugador.socket_cliente = socket_cliente
                    jugador.address = address
                    self.activos += 1
                    break
            self.jugadores_activos.append(jugador)
            self.jugadores_activos_nombre.append(jugador.username)
            self.lista_nombres_lock.release()
            
            if jugador is not None and not self.logica.partida_en_progreso:
                thread_cliente = threading.Thread(target=self.escuchar_cliente, args=(jugador,), daemon=True)
                self.log(f"Se ha conectado el jugador {jugador.username} con id: {jugador.id_jugador} ")
                thread_cliente.start()
                self.enviar_a_todos({"c_jugadores": self.cantidad_jugadores})
                self.enviar_a_todos({"usernames": self.jugadores_activos_nombre})

                if self.activos == self.cantidad_jugadores:
                    l = {"accion": "comenzar partida"}
                    self.log("La partida está por comenzar...")
                    lista_de_respuesta = self.logica.manejar_mensaje(l, self.jugadores_activos)
                    self.enviar_lista_respuestas(jugador, lista_de_respuesta)
            else:
                self.log(f"No se pudo ingresar al cliente {address}")
            
    def escuchar_cliente(self, jugador):

        try:
            while True:
                mensaje = self.recibir(jugador.socket_cliente)
                lista_respuestas = self.logica.manejar_mensaje(mensaje, jugador, self.lista_jugadores) 
                self.enviar_lista_respuestas(jugador, lista_respuestas)

        except ConnectionResetError:
            self.log(f"Error: conexión con {jugador.username} fue reseteada.")

    def enviar_lista_respuestas(self, jugador, lista_respuestas):
        
        for lista in lista_respuestas:
            mensaje = lista[1]
            if lista[0] == "empezar":
                self.enviar_a_todos(mensaje)
            
            elif lista[0] == "individual":
                self.enviar(mensaje, jugador.socket_cliente)
            
    
    def enviar(self, mensaje, socket_cliente):

        bytes_mensaje = self.codificar_mensaje(mensaje)

        largo_mensaje_bytes = (len(bytes_mensaje).to_bytes(4, byteorder="big"))
        socket_cliente.sendall(largo_mensaje_bytes + bytes_mensaje)

    
    def enviar_a_todos(self, mensaje):

        for jugador in self.lista_jugadores:
            try:
                if jugador.socket_cliente is not None:
                    
                    self.enviar(mensaje, jugador.socket_cliente)
            except ConnectionError:
                self.eliminar_cliente(jugador)

    def eliminar_cliente(self, jugador):
        self.lista_nombres_lock.acquire()

        self.log(f"Borrando socket del cliente {jugador}.")
        
        jugador.socket_cliente.close()
        jugador.socket_cliente = None
        jugador.address = None
        jugador.puntos = 0
        self.lista_nombres_lock.release()

    def recibir(self, socket_cliente):
        
        largo_mensaje_bytes = socket_cliente.recv(4)
        largo_mensaje = int.from_bytes(largo_mensaje_bytes, byteorder="big")

        bytes_mensajes = bytearray()
        while len(bytes_mensajes) < largo_mensaje:
            tamano_chunk = min(largo_mensaje - len(bytes_mensajes), 60)
            bytes_mensajes += socket_cliente.recv(tamano_chunk)
        
        mensaje = self.decodificar(bytes_mensajes)
        return mensaje

    def decodificar(self, bytes_mensaje):
        
        try:
            mensaje = json.loads(bytes_mensaje)
            return mensaje
        except json.JSONDecodeError:
            print("No se pudo decodificar el mensaje")
            return b""

    def codificar_mensaje(self, mensaje):

        try:
            json_mensaje = json.dumps(mensaje)
            bytes_mensaje = json_mensaje.encode()

            return bytes_mensaje
        
        except json.JSONDecodeError:
            print("No se pudo codificar el mensaje")
            return b""

    def creacion_mapa(self):
        
        self.creando_mapa = crear_mapa(self.dict_mapa)
        return self.creando_mapa

    def log(self, mensaje):

        if self.log_activado:
            print(mensaje)







#como logica y server tiene la misma lista de jugadores (?)