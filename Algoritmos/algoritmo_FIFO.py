# Algoritmos/algoritmo_fifo.py

def fifo_intervals(processes):
    """
    Simula el algoritmo FIFO y retorna:
      - intervals: diccionario donde la clave es el id del proceso y el valor es una lista
                   de tuplas [(inicio, fin)] (cada proceso se ejecuta en un único intervalo).
      - turnaround: diccionario con el tiempo de sistema (turnaround) para cada proceso.
      - waiting: diccionario con el tiempo de espera para cada proceso.
    
    Parámetros:
      processes: lista de diccionarios, cada uno con:
                 - 'id': str, ej. "P1"
                 - 'arrival': float, tiempo de llegada
                 - 'burst': float, tiempo de ráfaga
    """
    # Ordena los procesos por tiempo de llegada (si hay empate, se mantiene el orden original)
    processes.sort(key=lambda p: p['arrival'])
    
    intervals = {}
    turnaround = {}
    waiting = {}
    
    t = 0.0  # Tiempo de simulación
    for p in processes:
        # Si el CPU está inactivo hasta que llega el proceso, avanzamos el tiempo
        if t < p['arrival']:
            t = p['arrival']
        start_time = t
        finish_time = t + p['burst']
        t = finish_time  # Actualizamos el tiempo de simulación
        
        # Guardamos el intervalo de ejecución (único para FIFO)
        intervals[p['id']] = [(start_time, finish_time)]
        
        # Turnaround = tiempo de finalización - tiempo de llegada
        turnaround[p['id']] = finish_time - p['arrival']
        # Waiting = turnaround - burst
        waiting[p['id']] = turnaround[p['id']] - p['burst']
    
    return intervals, turnaround, waiting


# Ejemplo de uso:
if __name__ == "__main__":
    processes = [
        {"id": "P1", "arrival": 0, "burst": 6},
        {"id": "P2", "arrival": 1, "burst": 4},
        {"id": "P3", "arrival": 2, "burst": 2},
        {"id": "P4", "arrival": 3, "burst": 3},
    ]
    intervals, turnaround, waiting = fifo_intervals(processes)
    print("Intervalos generados:", intervals)
    print("Turnaround:", turnaround)
    print("Espera:", waiting)
    
    promedio_turnaround = sum(turnaround.values()) / len(turnaround)
    promedio_waiting = sum(waiting.values()) / len(waiting)
    print("Promedio Tiempo de sistema:", promedio_turnaround)
    print("Promedio Tiempo de espera:", promedio_waiting)
