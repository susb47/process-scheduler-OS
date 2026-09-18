class RRScheduler:
    def __init__(self):
        self.current_time = 0
        self.time_quantum = 4 # predefined
        self.total_waiting_time = 0
        self.total_turnaround_time = 0
#Disclaimer the following formulas wont match with class formulas for waiting time and Turnarounnd time    

    def schedule(self, processes):
        if not processes:
            return "No processes to schedule"  # Return a message if there are no processes
        
        # Initializing variables
        remaining_burst_time = [process.burst_time for process in processes]
        waiting_times = [0] * len(processes)
        last_execution_time = [0] * len(processes)  # Tracks the last time each process was executed
        
        scheduling_output = "Process ID\t\tArrival Time\t\tBurst Time\t\tWaiting Time\t\tTurnaround Time\n"
        
        while True:
            done = True
            for i, process in enumerate(processes):
                # Check if there is remaining burst time for the process
                if remaining_burst_time[i] > 0:
                    done = False  # Process still needs CPU time
                    
                    # Calculate waiting time
                    waiting_times[i] += max(0, self.current_time - last_execution_time[i])

                    if remaining_burst_time[i] > self.time_quantum:
                        # Process uses the full time quantum
                        self.current_time += self.time_quantum
                        remaining_burst_time[i] -= self.time_quantum
                    else:
                        # Process finishes its execution
                        self.current_time += remaining_burst_time[i]
                        remaining_burst_time[i] = 0
                        process_turnaround_time = self.current_time - process.arrival_time
                        self.total_turnaround_time += process_turnaround_time
                        
                        # Add process details to the scheduling output
                        scheduling_output += f"{process.name}\t\t{process.arrival_time}\t\t{process.burst_time}\t\t{waiting_times[i]}\t\t{process_turnaround_time}\n"
                    
                    # Update the last execution time for the process
                    last_execution_time[i] = self.current_time
            
            if done:
                break
        
        # Calculate total and average waiting/turnaround times
        self.total_waiting_time = sum(waiting_times)
        avg_waiting_time = self.total_waiting_time / len(processes)
        avg_turnaround_time = self.total_turnaround_time / len(processes)
        
        scheduling_output += f"\nAverage Waiting Time: {avg_waiting_time}\n"
        scheduling_output += f"Average Turnaround Time: {avg_turnaround_time}\n"

        return scheduling_output
    
    
    def get_process_schedule(self):
        return self.process_schedule
