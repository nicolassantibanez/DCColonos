
from time import sleep

from PyQt5.QtCore import pyqtSignal, QObject, QTimer

from sala_de_espera import SalaDeEspera
from ventana_principal import VentanaPrincipal
#from popups import PopupCrewmate, PopupExpulsar, PopupFinal

class Controlador(QObject):


    senal_actualizar_nombres = pyqtSignal(list)
    senal_crear_labels = pyqtSignal(int)
    senal_comenzar_partida = pyqtSignal()


    def __init__(self, parent):
        super().__init__()

        self.username = None
        
        self.partida_terminada = False

        self.sala_de_espera = SalaDeEspera()
        self.ventana_principal = VentanaPrincipal()


        #Conexiones
        self.senal_actualizar_nombres.connect(self.sala_de_espera.agregar_label)
        self.sala_de_espera.senal_actualizar.connect(parent.enviar)

        self.senal_crear_labels.connect(self.sala_de_espera.crear_label)
        
        self.senal_comenzar_partida.connect(self.mostrar_menu_principal)

    def mostrar_login(self):
        self.sala_de_espera.show()

    def mostrar_menu_principal(self):
        self.sala_de_espera.close()
        if not self.partida_terminada:
            self.ventana_principal.show()

    def manejar_mensaje(self, mensaje):
        lista_mensaje = mensaje.keys()
        for l in lista_mensaje:
            if l == "usernames":
                self.senal_actualizar_nombres.emit(mensaje["usernames"])

            elif l == "c_jugadores":
                self.senal_crear_labels.emit(mensaje["c_jugadores"])

            elif l == "accion":
                sleep(2)
                self.senal_comenzar_partida.emit()

        


        
        
