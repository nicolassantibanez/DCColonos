from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal
import sys

window_name, base_class = uic.loadUiType("Sala_de_espera.ui")

class SalaDeEspera(window_name, base_class):


    senal_actualizar = pyqtSignal(dict)
    close_window_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.nombres_puestos = []
        self.labels_creados = []
        self.layout_nombres
    
    def agregar_label(self, lista_nombres):
        for label in self.labels_creados:
            label.setText(f"{lista_nombres[0]}")
            lista_nombres.pop(0)
            if len(lista_nombres) == 0:
                break

    def crear_label(self, c_jugadores):
        self.labels_creados = []
        for i in reversed(range(self.layout_nombres.count())): 
            self.layout_nombres.itemAt(i).widget().setParent(None)

        for _ in range(0, c_jugadores):
            nuevo_label = QLabel("Esperando...", self)
            nuevo_label.setFont(QFont("Arial", 12))
            nuevo_label.setStyleSheet("color: yellow")
            self.layout_nombres.addWidget(nuevo_label)
            self.labels_creados.append(nuevo_label)

    def showEvent(self, event):
        dict_ = {
            "comando" : "request_jugadores"
        }
        self.senal_actualizar.emit(dict_)
        super().showEvent(event)

    def closeEvent(self, event):
        self.close_window_signal.emit(True)
        super().closeEvent(event)


        

    
if __name__ == "__main__":
    app = QApplication([])
    
    sala_espera = SalaDeEspera()
    sala_espera.show()

    sala_espera.agregar_label("jaime")
    sala_espera.agregar_label("juan")
    sys.exit(app.exec_())
