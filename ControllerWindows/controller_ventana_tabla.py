# ControllerWindows/controller_ventana_tabla.py

from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem,QMessageBox
from PyQt5.QtCore import Qt
from DesignWindows.ventana_tabla import Ui_MainWindow as Ui_VentanaTabla
from Algoritmos import algoritmo_round_robin

class ControllerVentanaTabla(QMainWindow):
    def __init__(self, num_procesos):
        super().__init__()
        self.num_procesos = num_procesos
        self.ui = Ui_VentanaTabla()
        self.ui.setupUi(self)
        self.setupTable()
        self.setupVisibility()
        self.connectSignals()

    def setupTable(self):
        """
        Configura la tabla:
         - Se establecen 'num_procesos' filas.
         - Se asignan los encabezados verticales como 'P1', 'P2', …, 'Pn'.
         - Las celdas de las dos columnas (Ráfaga y Tiempo de llegada) quedan vacías y editables.
        """
        # La tabla tiene 2 columnas ya definida en el diseño.
        self.ui.tabla_procesos.setRowCount(self.num_procesos)
        # Establecemos los encabezados verticales (IDs) usando setVerticalHeaderLabels
        headers = [f"P{i+1}" for i in range(self.num_procesos)]
        self.ui.tabla_procesos.setVerticalHeaderLabels(headers)
        # (Opcional) Si deseas inicializar las celdas de las columnas, puedes hacerlo:
        for i in range(self.num_procesos):
            # Columna 0: Ráfaga (editable)
            self.ui.tabla_procesos.setItem(i, 0, QTableWidgetItem(""))
            # Columna 1: Tiempo de llegada (editable)
            self.ui.tabla_procesos.setItem(i, 1, QTableWidgetItem(""))

    def setupVisibility(self):
        """
        Inicialmente se ocultan los widgets relacionados con el Quantum.
        Además, se deshabilita el botón SIMULAR.
        """
        self.ui.subtitulo_quantum.setVisible(False)
        self.ui.seleccionador_quantum.setVisible(False)
        self.ui.boton_seleccionar_quantum.setVisible(False)
        self.ui.boton_simular.setEnabled(False)

    def connectSignals(self):
        """
        Conecta los eventos de los botones:
         - BOTÓN VOLVER: vuelve a la ventana principal.
         - BOTÓN SELECCIONAR ALGORITMO: gestiona la selección del algoritmo.
         - BOTÓN SELECCIONAR QUANTUM: para Round Robin, habilita SIMULAR si el quantum es válido.
         - BOTÓN SIMULAR: Verifica que todo esté correcto en la tabla antes de enviar los datos a los algoritmos
        """
        self.ui.boton_volver.clicked.connect(self.volver)
        self.ui.boton_seleccionar_algoritmo.clicked.connect(self.seleccionarAlgoritmo)
        self.ui.boton_seleccionar_quantum.clicked.connect(self.seleccionarQuantum)
        self.ui.boton_simular.clicked.connect(self.simular)

    def volver(self):
        """
        Cierra la ventana actual y vuelve a abrir la ventana principal.
        """
        from ControllerWindows.controller_ventana_principal import ControllerVentanaPrincipal
        self.ventana_principal = ControllerVentanaPrincipal()
        self.ventana_principal.show()
        self.close()

    def seleccionarAlgoritmo(self):
        """
        Al hacer clic en 'SELECCIONAR' para el algoritmo:
          - Si se elige FIFO o SJF: habilita directamente el botón SIMULAR.
          - Si se elige ROUND ROBIN: muestra los widgets de quantum y deja deshabilitado SIMULAR hasta seleccionar un quantum.
        """
        alg = self.ui.seleccionador_algoritmo.currentText().strip().upper()
        if alg in ["FIFO", "SJF"]:
            self.ui.boton_simular.setEnabled(True)
            # Asegúrate de ocultar los widgets de quantum si se mostraron anteriormente.
            self.ui.subtitulo_quantum.setVisible(False)
            self.ui.seleccionador_quantum.setVisible(False)
            self.ui.boton_seleccionar_quantum.setVisible(False)
        elif alg == "ROUND ROBIN":
            self.ui.subtitulo_quantum.setVisible(True)
            self.ui.seleccionador_quantum.setVisible(True)
            self.ui.boton_seleccionar_quantum.setVisible(True)
            self.ui.boton_simular.setEnabled(False)
        else:
            self.ui.boton_simular.setEnabled(False)

    def seleccionarQuantum(self):
        """
        Al hacer clic en 'SELECCIONAR' para el quantum, se verifica que el valor
        seleccionado sea válido y se habilita el botón SIMULAR.
        """
        quantum_str = self.ui.seleccionador_quantum.currentText()
        try:
            quantum = int(quantum_str)
            if quantum >= 1:
                self.ui.boton_simular.setEnabled(True)
            else:
                self.ui.boton_simular.setEnabled(False)
        except ValueError:
            self.ui.boton_simular.setEnabled(False)

    def simular(self):
        # Primero, valida que todas las celdas de la tabla estén llenas.
        num_filas = self.ui.tabla_procesos.rowCount()
        processes = []
        
        for i in range(num_filas):
            # Suponiendo que la primera columna es 'Ráfaga' y la segunda es 'Tiempo de llegada'
            item_burst = self.ui.tabla_procesos.item(i, 0)
            item_arrival = self.ui.tabla_procesos.item(i, 1)
            if item_burst is None or item_arrival is None or item_burst.text().strip() == "" or item_arrival.text().strip() == "":
                QMessageBox.warning(self, "Error", f"Falta llenar datos en la fila {i+1}.")
                return
            try:
                burst = float(item_burst.text().strip())
                arrival = float(item_arrival.text().strip())
            except ValueError:
                QMessageBox.warning(self, "Error", f"Los valores de la fila {i+1} deben ser numéricos.")
                return
            
            processes.append({
                "id": f"P{i+1}",
                "burst": burst,
                "arrival": arrival
            })
        
        # Lee el algoritmo seleccionado
        algoritmo = self.ui.seleccionador_algoritmo.currentText().strip().upper()
        
        if algoritmo in ["FIFO", "SJF"]:
            # Por ejemplo, si tienes funciones FIFO o SJF, las llamarías aquí.
            # Supongamos que para FIFO tienes una función fifo_intervals(processes)
            intervals = None  # Aquí llamarías a la función correspondiente.
            # Ejemplo:
            # intervals = fifo_intervals(processes)
            # O para SJF:
            # intervals = sjf_intervals(processes)
            # Luego, habilitas o llamas al método para graficar el diagrama.
            pass
        elif algoritmo == "ROUND ROBIN":
            # Obtén el quantum del widget (por ejemplo, un QComboBox o QSpinBox)
            try:
                quantum = int(self.ui.seleccionador_quantum.currentText().strip())
            except ValueError:
                QMessageBox.warning(self, "Error", "El quantum debe ser un número entero válido.")
                return
            # Llama a la función que simula Round Robin, que debe devolver los intervalos
            intervals,tiempo_sistema,tiempo_espera = algoritmo_round_robin.round_robin_variant(processes, quantum)
        else:
            QMessageBox.warning(self, "Error", "Algoritmo no reconocido.")
            return

        # Aquí podrías, por ejemplo, almacenar 'intervals' en una variable global
        # o pasarla a la función que genera el diagrama de Gantt.
        # Por ejemplo:
        self.intervalos = intervals
        # Y luego, abrir la ventana del diagrama o llamar a la función para graficarlo.
        # self.mostrarDiagramaGantt(intervals)
        print("Intervalos generados:", intervals)
        print("Tiempo de espera:",tiempo_espera)
        print("Tiempo sistema:",tiempo_sistema)
