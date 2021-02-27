from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import pyqtSignal
import sys

window_name, base_class = uic.loadUiType("Menu_principal.ui")

class VentanaPrincipal(window_name, base_class):

    def __init__(self):
        super().__init__()
        self.setGeometry(200, 50, 1503, 973)
        self.setupUi(self)





if __name__ == "__main__":
    app = QApplication([])
    
    ventana = VentanaPrincipal()
    ventana.show()

    sys.exit(app.exec_())
