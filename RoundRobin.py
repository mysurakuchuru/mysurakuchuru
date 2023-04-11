
import sys

# process class to store process information
class Process:
    def __init__(self, pid, arrival_time, service_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.service_time = service_time
        self.completion_time = 0
        self.waiting_time = 0

# function to read process file and return a list of processes
def read_process_file(file_path):
    processes = []
    with open(file_path, 'r') as file:
        for line in file:
            data = line.strip().split()
            pid = int(data[0])
            arrival_time = int(data[1])
            service_time = int(data[2])
            processes.append(Process(pid, arrival_time, service_time))
    return processes

# main function to simulate round robin scheduling
def round_robin_scheduling(processes, time_quantum):
    clock = 0
    ready_queue = []
    current_process = None
    context_switches = 0
    
    # loop until all processes have completed execution
    while True:
        # check if there are any new processes that have arrived
        for process in processes:
            if process.arrival_time == clock:
                ready_queue.append(process)
        
        # check if the CPU is idle
        if current_process is None:
            if len(ready_queue) > 0:
                current_process = ready_queue.pop(0)
                context_switches += 1
                current_process.waiting_time += clock - current_process.arrival_time
                if current_process.service_time <= time_quantum:
                    clock += current_process.service_time
                    current_process.completion_time = clock
                    current_process.service_time = 0
                else:
                    clock += time_quantum
                    current_process.service_time -= time_quantum
                    ready_queue.append(current_process)
                    current_process = None
            else:
                clock += 1
        else:
            # execute current process for time quantum
            if current_process.service_time <= time_quantum:
                clock += current_process.service_time
                current_process.completion_time = clock
                current_process.service_time = 0
                current_process = None
            else:
                clock += time_quantum
                current_process.service_time -= time_quantum
                ready_queue.append(current_process)
                current_process = None
            context_switches += 1
        
        # check if all processes have completed execution
        completed_processes = [p for p in processes if p.service_time == 0]
        if len(completed_processes) == len(processes):
            break
    
    # calculate performance evaluation criteria
    cpu_utilization = sum([p.service_time for p in processes]) / clock
    throughput = len(processes) / clock
    avg_waiting_time = sum([p.waiting_time for p in processes]) / len(processes)
    avg_turnaround_time = sum([p.completion_time - p.arrival_time for p in processes]) / len(processes)
    
    # print performance evaluation criteria
    print("CPU Utilization: {:.2f}%".format(cpu_utilization * 100))
    print("Throughput: {:.2f} processes per unit time".format(throughput))
    print("Average Waiting Time: {:.2f} units of time".format(avg_waiting_time))
    print("Average Turnaround Time: {:.2f} units of time".format(avg_turnaround_time))
    print("Context Switches")
