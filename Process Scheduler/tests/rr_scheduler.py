class RRScheduler:
    def __init__(self):
        self.current_time = 0
        self.time_quantum = 4  # Predefined time quantum
        self.total_waiting_time = 0
        self.total_turnaround_time = 0
        self.process_schedule = []  # Stores (start_time, end_time, process_name) for Gantt chart

    def schedule(self, processes):
        if not processes:
            return "No processes to schedule"  # Return a message if there are no processes

        # Initializing variables
        remaining_burst_time = [process.burst_time for process in processes]
        waiting_times = [0] * len(processes)
        last_execution_time = [process.arrival_time for process in processes]  # Tracks the last time each process was executed

        scheduling_output = "Process ID\t\tArrival Time\t\tBurst Time\t\tWaiting Time\t\tTurnaround Time\n"

        while True:
            done = True
            for i, process in enumerate(processes):
                # Check if there is remaining burst time for the process
                if remaining_burst_time[i] > 0:
                    done = False  # Process still needs CPU time

                    # Calculate waiting time
                    waiting_times[i] += max(0, self.current_time - last_execution_time[i])

                    start_time = self.current_time

                    if remaining_burst_time[i] > self.time_quantum:
                        # Process uses the full time quantum
                        self.current_time += self.time_quantum
                        remaining_burst_time[i] -= self.time_quantum
                    else:
                        # Process finishes its execution
                        self.current_time += remaining_burst_time[i]
                        remaining_burst_time[i] = 0

                        # Calculate turnaround time
                        turnaround_time = self.current_time - process.arrival_time
                        self.total_turnaround_time += turnaround_time

                        # Update scheduling output
                        scheduling_output += f"{process.name}\t\t{process.arrival_time}\t\t{process.burst_time}\t\t{waiting_times[i]}\t\t{turnaround_time}\n"

                    # Record process schedule for Gantt chart
                    end_time = self.current_time
                    self.process_schedule.append((start_time, end_time, process.name))

                    # Update the last execution time for the process
                    last_execution_time[i] = self.current_time

            if done:
                break

        # Calculate total and average waiting/turnaround times
        self.total_waiting_time = sum(waiting_times)
        avg_waiting_time = self.total_waiting_time / len(processes)
        avg_turnaround_time = self.total_turnaround_time / len(processes)

        scheduling_output += f"\nAverage Waiting Time: {avg_waiting_time:.2f}\n"
        scheduling_output += f"Average Turnaround Time: {avg_turnaround_time:.2f}\n"

        return scheduling_output

    def get_process_schedule(self):
        # Ensure compatibility with the code using the process_schedule attribute
        return self.process_schedule
