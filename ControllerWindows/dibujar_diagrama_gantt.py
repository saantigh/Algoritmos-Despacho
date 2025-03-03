import matplotlib.pyplot as plt
import random

def dibujar_gantt(intervals, titulo="Diagrama de Gantt"):
    """
    Dibuja un diagrama de Gantt a partir de un diccionario de intervalos.
    
    Parámetros:
    -----------
    intervals : dict
        Un diccionario con la forma:
          {
            "P1": [(0,3), (5,7)],
            "P2": [(3,5), (9,10)],
            "P3": [(7,9), (10,12)]
          }
        donde cada proceso (p. ej. "P1") tiene una lista de intervalos (inicio, fin).
    titulo : str
        Título que se mostrará en la parte superior del diagrama.
    """
    # Crear la figura y ejes
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Obtener la lista de procesos en algún orden (por ejemplo, orden alfabético)
    # Si quieres mostrar P1 arriba y P3 abajo, invierte el orden después.
    pids = sorted(intervals.keys())
    
    # Generar colores para cada proceso (opcional)
    # Puedes usar un colormap o colores fijos.
    # Aquí usamos una lista de colores y repetimos si hay más procesos que colores.
    color_list = [
        "#f94144","#f3722c","#f8961e","#f9c74f","#90be6d",
        "#43aa8b","#577590","#277da1","#4d908e","#b5179e"
    ]
    
    # Dibujar cada proceso en una línea (barh)
    # El valor 'i' define la posición vertical, y (start, end) define la barra horizontal
    for i, pid in enumerate(pids):
        intervals_pid = intervals[pid]
        # Elegir un color distinto para cada proceso
        color = color_list[i % len(color_list)]
        
        for (start, end) in intervals_pid:
            ax.barh(
                y=i, 
                width=(end - start), 
                left=start, 
                height=0.4, 
                color=color, 
                edgecolor="black", 
                align='center'
            )
    
    # Configurar eje Y: poner los nombres de procesos en la posición [0,1,2,...]
    ax.set_yticks(range(len(pids)))
    ax.set_yticklabels(pids)
    
    
    # Etiquetas y título
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Procesos")
    ax.set_title(titulo)
    
    # Ajustar márgenes para que se vea mejor
    plt.tight_layout()
    
    # Mostrar la gráfica
    plt.show()
