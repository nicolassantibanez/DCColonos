from threading import Lock

class JUGADOR:

    id_ = 0

    def __init__(self, username):
        self.id_jugador = JUGADOR.id_
        self.username = username
        JUGADOR.id_ += 1

        self.puntos = 0

        self.socket_cliente = None
        self.address = None


def crear_lista_jugadores(lista_nombres):

    lista_jugadores = []
    for nombre in lista_nombres:
        jugador = JUGADOR(nombre)
        lista_jugadores.append(jugador)
    
    return lista_jugadores