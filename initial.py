import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from DesignWindows.ventana_principal import Ui_MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()        # Crea la ventana principal
    ui = Ui_MainWindow()              # Instancia la interfaz generada
    ui.setupUi(MainWindow)            # Configura la UI en la ventana principal
    MainWindow.show()
    sys.exit(app.exec())
