import os
import json
from random import choice, randint



class NODO:

    def __init__(self, nodo_id):

        self.nodo_id = nodo_id
        self.ocupado = False
        self.nombre_usuario = None
        self.vecinos = []

    def agregar_vecino(self, nodo):
        self.vecinos.append(nodo)

    def __repr__(self):
        texto = f"[{self.nodo_id}]"
        if len(self.vecinos) > 0:
            textos_vecinos = [f"[{vecino.nodo_id}]" for vecino in self.vecinos]
            texto += " -> " + ", ".join(textos_vecinos)
        return texto


class HEXAGONO:

    def __init__(self, hexagono_id, numero_ficha, materia_prima):

        self.hexagono_id = hexagono_id
        self.numero_ficha = numero_ficha
        self.materia_prima = materia_prima
        self.nodos_asociados = []
    
    def agregar_nodo(self, nodo):
        self.nodos_asociados.append(nodo)


class MAPA:

    def __init__(self, hexagonos, dimensiones):

        self.mapa = hexagonos
        self.dimensiones = dimensiones
    

def crear_mapa(dict_mapa):

    lista_con_nodos = []
    lista_con_hexagonos = []
    nodos = dict_mapa["nodos"]
    hexagonos = dict_mapa["hexagonos"]

    #Se crea cada nodo
    for nodo in nodos:
        nuevo_nodo = NODO(nodo)
        lista_con_nodos.append(nuevo_nodo)
        
    #Se agregan los vecinos al nodo correspondiente
    for nodo in lista_con_nodos:
        vecinos = nodos[str(nodo.nodo_id)]
            
        for numero in vecinos:
            for nodo_vecino in lista_con_nodos:
                if nodo_vecino.nodo_id == numero:
                    nodo.agregar_vecino(nodo_vecino)
            
    #Se instancia cada hexagono con sus respectivos nodos
    recursos = ["Madera", "Ladrillo", "Trigo"]
    cantidad_recursos = [[4, 3 ,3], [3, 4, 3], [3, 3, 4]]
    uso_madera = 0
    uso_ladrillo = 0
    uso_trigo = 0
    numeros_usados = []
    opcion_recursos = choice(cantidad_recursos)
    for hexagono_id in hexagonos:
        while True:
            numero_ficha = randint(randint(2, 6), randint(8, 12))
            if numero_ficha not in numeros_usados or len(numeros_usados) > 10:
                break
                
        materia_prima = choice(recursos)
        if materia_prima == "Madera":
            uso_madera += 1
        elif materia_prima == "Ladrillo":
            uso_ladrillo += 1
        elif materia_prima == "Trigo":
            uso_trigo += 1
        
        if uso_madera == opcion_recursos[0]:
            recursos.remove("Madera")
            uso_madera += 1
        elif uso_ladrillo == opcion_recursos[1]:
            recursos.remove("Ladrillo")
            uso_ladrillo += 1
        elif uso_trigo == opcion_recursos[2]:
            recursos.remove("Trigo")
            uso_trigo += 1
        if numero_ficha not in numeros_usados:
            nuevo_hexagono = HEXAGONO(hexagono_id, numero_ficha, materia_prima)
            nodos_id_hexagonos = hexagonos[str(hexagono_id)]
            for numero in nodos_id_hexagonos:
                for nodo in lista_con_nodos:
                    if numero == nodo.nodo_id:
                        nuevo_hexagono.agregar_nodo(nodo)
                
            lista_con_hexagonos.append(nuevo_hexagono)
            numeros_usados.append(numero_ficha)

    #Creamos el mapa
    dict_hexagonos = {}
    dimensiones = dict_mapa["dimensiones_mapa"]
    dict_hexagonos["hexagonos"] = (lista_con_hexagonos[0], lista_con_hexagonos[1],\
        lista_con_hexagonos[2], lista_con_hexagonos[3], lista_con_hexagonos[4], \
        lista_con_hexagonos[5], lista_con_hexagonos[6], lista_con_hexagonos[7], \
        lista_con_hexagonos[8], lista_con_hexagonos[9])

    mapa = MAPA(dict_hexagonos, dimensiones)

    return mapa