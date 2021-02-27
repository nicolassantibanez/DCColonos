import json
import os
from server import SERVIDOR

ruta_deserializacion_mapa = os.path.join("grafo.json")
ruta_deserializacion_parametros = os.path.join("parametros.json")

def deserializacion(ruta):

    with open(ruta, "rb") as archivo:
        return json.load(archivo)

dict_mapa = deserializacion(ruta_deserializacion_mapa)
parametros = deserializacion(ruta_deserializacion_parametros)

if __name__ == "__main__":
    HOST = parametros["host"]
    PORT = parametros["port"]
    lista_nombres = parametros["jugadores"]
    cantidad_jugadores = parametros["CANTIDAD_JUGADORES_PARTIDA"]

    SERVIDOR = SERVIDOR(HOST, PORT, dict_mapa, lista_nombres, cantidad_jugadores)

    try:
        while True:
            input("Presione Ctrl+C para cerrar el servidor...")
    except KeyboardInterrupt:
        print("Cerrando servidor...")