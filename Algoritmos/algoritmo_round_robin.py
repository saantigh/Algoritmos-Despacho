def round_robin_variant(processes, quantum):
    """
    Round Robin 'variante':
      - Cuando un proceso termina su time slice en t,
        PRIMERO se añaden los procesos que llegan en t,
        LUEGO se re-inserta el proceso saliente (si no terminó).
      - Devuelve:
         intervals: {pid: [(inicio, fin), ...]}
         turnaround: {pid: tiempo_de_retorno}
         waiting: {pid: tiempo_de_espera}
    """

    # 1) Inicializar
    for idx, p in enumerate(processes):
        p['remaining'] = p['burst']
        p['completed'] = False
        p['index'] = idx  # para romper empates si arrival es el mismo

    # Ordenar por arrival e index para orden estable
    processes.sort(key=lambda x: (x['arrival'], x['index']))

    intervals = {p['id']: [] for p in processes}
    turnaround = {}
    waiting = {}

    t = 0.0
    queue = []
    i = 0
    n = len(processes)

    def add_arrivals_up_to(time):
        nonlocal i
        # Inserta procesos que llegan en o antes de 'time'
        while i < n and processes[i]['arrival'] <= time:
            queue.append(processes[i])
            i += 1

    # Añadir los que llegan en t=0
    add_arrivals_up_to(t)

    while queue or i < n:
        if not queue:
            # si la cola está vacía, saltar al próximo arrival
            t = processes[i]['arrival']
            add_arrivals_up_to(t)

        # Tomar el primer proceso de la cola
        current = queue.pop(0)
        if current['completed']:
            continue

        start_time = t
        run_time = min(quantum, current['remaining'])
        t += run_time
        current['remaining'] -= run_time

        # Registrar intervalo
        intervals[current['id']].append((start_time, t))

        # Guardar temporalmente el proceso saliente (si no ha terminado)
        temp = None
        if current['remaining'] > 0:
            temp = current

        # AHORA añadimos primero los que llegaron hasta 't'
        add_arrivals_up_to(t)

        # LUEGO reinsertamos 'temp' (el proceso saliente) si no terminó
        if temp:
            queue.append(temp)

        # Si terminó, marcamos completed
        if current['remaining'] == 0:
            current['completed'] = True

    # 4) Calcular tiempos de retorno y de espera
    for p in processes:
        pid = p['id']
        completion_time = intervals[pid][-1][1]
        t_turnaround = completion_time - p['arrival']
        t_waiting = t_turnaround - p['burst']
        turnaround[pid] = t_turnaround
        waiting[pid] = t_waiting

    return intervals, turnaround, waiting

# ---------------- EJEMPLO ----------------
if __name__ == "__main__":
    processes = [
        {"id": "P1", "arrival": 0, "burst": 6},
        {"id": "P2", "arrival": 1, "burst": 4},
        {"id": "P3", "arrival": 2, "burst": 2},
        {"id": "P4", "arrival": 3, "burst": 3},
    ]
    quantum = 2

    intervals, turnaround, waiting = round_robin_variant(processes, quantum)
    print("Intervalos generados:", intervals)
    print("Turnaround:", turnaround)
    print("Waiting:", waiting)
