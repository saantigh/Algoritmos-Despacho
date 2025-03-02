def sjf_intervals(processes):
    """
    Simula el algoritmo Shortest Job First (no preemptivo) y retorna:
      - intervals: diccionario con {pid: [(inicio, fin)]} (cada proceso se ejecuta en un único intervalo)
      - turnaround: diccionario con {pid: turnaround_time}, donde turnaround_time = finish - arrival
      - waiting: diccionario con {pid: waiting_time}, donde waiting_time = turnaround - burst

    Parámetros:
      processes: lista de diccionarios, cada uno con:
          'id': str, por ejemplo "P1"
          'arrival': float, tiempo de llegada
          'burst': float, tiempo de ráfaga
    """
    # Creamos una copia para no modificar la lista original
    not_executed = processes.copy()  
    n = len(not_executed)
    
    intervals = {}
    tiempos_de_sistema = {}
    tiempos_de_espera = {}

    t = 0.0  # Tiempo de simulación

    # Ordenamos inicialmente por tiempo de llegada y, en caso de empate, por burst
    not_executed.sort(key=lambda p: (p['arrival'], p['burst']))

    while not_executed:
        # Obtener los procesos que han llegado (arrival <= t)
        ready = [p for p in not_executed if p['arrival'] <= t]
        if not ready:
            # Si no hay procesos listos, avanzamos t al siguiente arrival
            t = min(p['arrival'] for p in not_executed)
            ready = [p for p in not_executed if p['arrival'] <= t]
        # Seleccionar el proceso con el burst más corto de los listos
        current = min(ready, key=lambda p: p['burst'])
        start_time = t
        finish_time = t + current['burst']
        t = finish_time  # actualiza el tiempo

        # Registrar el intervalo de ejecución para el proceso actual
        intervals[current['id']] = [(start_time, finish_time)]
        # Calcular turnaround y waiting
        tiempos_de_sistema[current['id']] = finish_time - current['arrival']
        tiempos_de_espera[current['id']] = tiempos_de_sistema[current['id']] - current['burst']

        # Remover el proceso ya ejecutado
        not_executed.remove(current)
    
    return intervals, tiempos_de_sistema, tiempos_de_espera


# ------------------ Ejemplo de uso ------------------
if __name__ == "__main__":
    processes = [
        {"id": "P1", "arrival": 0, "burst": 6},
        {"id": "P2", "arrival": 1, "burst": 4},
        {"id": "P3", "arrival": 2, "burst": 2},
        {"id": "P4", "arrival": 3, "burst": 3},
    ]
    intervals, turnaround, waiting = sjf_intervals(processes)
    print("Intervalos:", intervals)
    print("Turnaround:", turnaround)
    print("Waiting:", waiting)
    
    promedio_tiempo_sistema = sum(turnaround.values()) / len(turnaround)
    promedio_tiempo_espera = sum(waiting.values()) / len(waiting)
    print("Promedio Turnaround:", promedio_tiempo_sistema)
    print("Promedio Waiting:", promedio_tiempo_espera)

