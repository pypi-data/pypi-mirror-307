# cpu_scheduler/algorithms.py

def fcfs(processes):
    """First-Come, First-Served Scheduling Algorithm"""
    processes.sort(key=lambda x: x['arrival_time'])  # Sort by arrival time
    time = 0
    schedule = []

    for process in processes:
        if time < process['arrival_time']:
            time = process['arrival_time']
        process['start_time'] = time
        process['completion_time'] = time + process['burst_time']
        time += process['burst_time']
        schedule.append(process)
    
    return schedule




def sjf(processes):
    """Shortest Job First Scheduling Algorithm (Non-Preemptive)"""
    processes.sort(key=lambda x: (x['arrival_time'], x['burst_time']))
    time = 0
    schedule = []
    waiting_list = []

    while processes or waiting_list:
        # Add all available processes to waiting list
        while processes and processes[0]['arrival_time'] <= time:
            waiting_list.append(processes.pop(0))
        
        if waiting_list:
            # Select process with the shortest burst time
            waiting_list.sort(key=lambda x: x['burst_time'])
            process = waiting_list.pop(0)
            process['start_time'] = time
            process['completion_time'] = time + process['burst_time']
            time += process['burst_time']
            schedule.append(process)
        else:
            time = processes[0]['arrival_time']

    return schedule






def round_robin(processes, quantum):
    """Round Robin Scheduling Algorithm"""
    time = 0
    queue = processes[:]
    schedule = []

    while queue:
        process = queue.pop(0)
        if 'remaining_time' not in process:
            process['remaining_time'] = process['burst_time']

        if process['remaining_time'] > quantum:
            time += quantum
            process['remaining_time'] -= quantum
            queue.append(process)
        else:
            time += process['remaining_time']
            process['completion_time'] = time
            process['remaining_time'] = 0

        schedule.append({'process_id': process['process_id'], 'current_time': time})

    return schedule





def priority_scheduling(processes):
    """Priority Scheduling Algorithm (Non-Preemptive)"""
    processes.sort(key=lambda x: (x['arrival_time'], x['priority']))
    time = 0
    schedule = []
    waiting_list = []

    while processes or waiting_list:
        while processes and processes[0]['arrival_time'] <= time:
            waiting_list.append(processes.pop(0))

        if waiting_list:
            waiting_list.sort(key=lambda x: x['priority'])  # Sort by priority
            process = waiting_list.pop(0)
            process['start_time'] = time
            process['completion_time'] = time + process['burst_time']
            time += process['burst_time']
            schedule.append(process)
        else:
            time = processes[0]['arrival_time']

    return schedule
