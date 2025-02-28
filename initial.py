import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from DesignWindows.ventana_principal import Ui_MainWindow  # Asegúrate de que el nombre coincida con tu archivo generado



class MyApp(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

# Inicializar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())