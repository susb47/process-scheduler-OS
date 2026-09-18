from collections import deque


class RRSchedulerplot:
    def __init__(self):
        self.schedule_log = []  # Store (process_name, start_time, duration)

    def schedule(self, processes, time_quantum=2):
        # Sort processes by arrival time
        processes = sorted(processes, key=lambda p: p.arrival_time)

        # Create a queue for Round Robin
        queue = deque()
        time = 0
        output = []

        # Add processes to the queue as they arrive
        remaining_bursts = {p.name: p.burst_time for p in processes}
        arrival_index = 0

        while queue or arrival_index < len(processes):
            # Add newly arrived processes to the queue
            while arrival_index < len(processes) and processes[arrival_index].arrival_time <= time:
                queue.append(processes[arrival_index])
                arrival_index += 1

            if queue:
                # Get the next process from the queue
                current_process = queue.popleft()

                # Determine execution time
                execution_time = min(time_quantum, remaining_bursts[current_process.name])
                self.schedule_log.append((current_process.name, time, execution_time))

                # Simulate execution
                remaining_bursts[current_process.name] -= execution_time
                time += execution_time

                # Add process back to the queue if it's not finished
                if remaining_bursts[current_process.name] > 0:
                    # Add any newly arrived processes to the queue
                    while arrival_index < len(processes) and processes[arrival_index].arrival_time <= time:
                        queue.append(processes[arrival_index])
                        arrival_index += 1
                    queue.append(current_process)

                # Turnaround and waiting time updates
                output.append(
                    f"Process {current_process.name}: Start={time - execution_time}, Duration={execution_time}"
                )
            else:
                # If the queue is empty, move to the next process's arrival time
                time = processes[arrival_index].arrival_time

        return "\n".join(output)
        

    def get_schedule_log(self):
        return self.schedule_log
