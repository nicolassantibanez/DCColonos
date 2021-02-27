from threading import Lock


class LOGICA:

    
    log_in_lock = Lock()

    lista_jugadores_lock = Lock()

    partida_lock = Lock()

    def __init__(self):
        self.partida_en_progreso = False
        self.lista_jugadores_partida = []

    
    def manejar_mensaje(self, mensaje, lista_jugadores, jugador=None):
        
        try:
            comando = mensaje["accion"]
        except KeyError:
            return []
        
        lista_respuesta = []

        if comando == "log_in":
            username = mensaje["username"]
            self.log_in_lock.acquire()
            if self.validar_username(username, lista_jugadores):
                jugador.username = username
                respuesta = {
                    "accion": "log_in_accepted",
                    "username": username
                }
            self.log_in_lock.release()
            lista = ["individual", respuesta]
            lista_respuesta.append(lista)
        
        elif comando == "comenzar partida":
            self.comenzar_partida(lista_jugadores, lista_respuesta) 
        return lista_respuesta

    def validar_username(self, username, lista_jugadores):
        
        self.lista_jugadores_lock.acquire()
        for jugador in lista_jugadores:
            if jugador.username == username:
                self.lista_jugadores_lock.release()
                return False
        
        self.lista_jugadores_lock.release()
        return True

    def comenzar_partida(self, lista_jugadores, lista_respuesta):

        self.partida_lock.acquire()

        if self.partida_en_progreso:
            return
        
        for i in lista_jugadores:
            if i.username is None:
                self.partida_lock.release()
                return
        
        self.inicializar_jugadores(lista_jugadores)
        self.partida_en_progreso = True
        respuesta = {
            "accion": "empezar",
        }
        lista = ["empezar", respuesta]
        lista_respuesta.append(lista)
        self.partida_lock.release()

    def inicializar_jugadores(self, lista_jugadores):
        
        for jugador in lista_jugadores:
            jugador.puntos = 0
    
    