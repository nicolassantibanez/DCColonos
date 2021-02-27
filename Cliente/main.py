import sys
import os
import json

from PyQt5.QtWidgets import QApplication
from cliente import CLIENTE

ruta_parametros = os.path.join("parametros.json")

def deserializacion(ruta):
    
    with open(ruta, "rb") as archivo:
        return json.load(archivo)

parametros = deserializacion(ruta_parametros)

if __name__ == "__main__":

    host = parametros["host"]
    port = parametros["puerto"]

    App = QApplication([])
    Cliente = CLIENTE(host, port)

    ret = App.exec_()
    sys.exit(ret)