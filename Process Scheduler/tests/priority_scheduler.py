class PriorityScheduler:
    def __init__(self):
        self.current_time = 0
        self.total_waiting_time = 0
        self.total_turnaround_time = 0
        self.process_schedule = []  # To store (start_time, end_time, process_name)

    def schedule(self, processes):
        if not processes:
            return "No processes to schedule"  # Return a message if there are no processes

        # Sort processes initially by arrival time (to process them in order of arrival)
        processes.sort(key=lambda x: x.arrival_time)
        completed_processes = []  # To track completed processes
        
        scheduling_output = "Process ID\tArrival Time\tPriority\tBurst Time\tWaiting Time\tTurnaround Time\n"
        
        while len(completed_processes) < len(processes):
            # Get processes that have arrived by the current time
            ready_queue = [p for p in processes if p.arrival_time <= self.current_time and p not in completed_processes]
            
            if not ready_queue:
                # If no process is ready, increment the current time to the next process arrival
                self.current_time = min(p.arrival_time for p in processes if p not in completed_processes)
                continue

            # Select the process with the highest priority (lowest priority value)
            highest_priority_process = min(ready_queue, key=lambda p: p.priority)

            # Calculate times
            start_time = self.current_time
            waiting_time = start_time - highest_priority_process.arrival_time
            self.total_waiting_time += waiting_time

            turnaround_time = waiting_time + highest_priority_process.burst_time
            self.total_turnaround_time += turnaround_time

            # Update the schedule and current time
            end_time = start_time + highest_priority_process.burst_time
            self.process_schedule.append((start_time, end_time, highest_priority_process.name))
            self.current_time = end_time

            # Add the completed process to the completed list
            completed_processes.append(highest_priority_process)

            # Update output
            scheduling_output += f"{highest_priority_process.name}\t\t{highest_priority_process.arrival_time}\t\t{highest_priority_process.priority}\t\t{highest_priority_process.burst_time}\t\t{waiting_time}\t\t{turnaround_time}\n"

        # Calculate average times
        avg_waiting_time = self.total_waiting_time / len(processes)
        avg_turnaround_time = self.total_turnaround_time / len(processes)

        scheduling_output += f"\nAverage Waiting Time: {avg_waiting_time:.2f}\n"
        scheduling_output += f"Average Turnaround Time: {avg_turnaround_time:.2f}\n"
        
        return scheduling_output,
    
    
    def get_process_schedule(self):
        return self.process_schedule
        

    
